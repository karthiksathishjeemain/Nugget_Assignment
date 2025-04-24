import os
import re


def count_content_lines(file_path):
    """Count the number of non-empty lines in a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = [line.strip() for line in file if line.strip()]
            return len(lines)
    except Exception as e:
        print(f"Error counting lines in {file_path}: {str(e)}")
        return 0

def remove_urls(text):
    """Remove URL lines and URL references from text"""
   
    text = re.sub(r'^URL: .*$', '', text, flags=re.MULTILINE)
    
    text = re.sub(r'https?://\S+', '', text)
    
    text = re.sub(r'\[([^\]]+)\]\(https?://[^)]+\)', r'\1', text)
    
    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
    
    return text

def merge_website_content():
   
    data_dir = "data"
    output_dir = "structured_content"
    
    if not os.path.exists(data_dir):
        print(f"Error: {data_dir} directory not found")
        return
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    for domain_folder in os.listdir(data_dir):
        domain_path = os.path.join(data_dir, domain_folder)
        
        if not os.path.isdir(domain_path):
            continue
            
        print(f"Processing domain: {domain_folder}")
        
        output_file_path = os.path.join(output_dir, f"{domain_folder}.txt")
        
        files_merged = 0
        files_skipped = 0
     
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(f"Merged content for {domain_folder}\n")
            output_file.write("=" * 80 + "\n\n")
         
            content_files = sorted([f for f in os.listdir(domain_path) if f.endswith('.txt')])
         
            for content_file in content_files:
                file_path = os.path.join(domain_path, content_file)
         
                line_count = count_content_lines(file_path)
                if line_count <= 3:
                    print(f"  Skipping {content_file} - insufficient content ({line_count} lines)")
                    files_skipped += 1
                    continue
                
      
                page_name = content_file.replace('.txt', '')
                page_name = page_name.replace('__', '/')
                if page_name == 'index':
                    page_name = "Home Page"
                
          
                output_file.write(f"SECTION: {page_name}\n")
                output_file.write("-" * 80 + "\n")
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as content_file:
                        content = content_file.read()
                    
                        cleaned_content = remove_urls(content)
                        
                        output_file.write(cleaned_content)
                        output_file.write("\n\n" + "=" * 80 + "\n\n")
                        files_merged += 1
                except Exception as e:
                    print(f"  Error reading {content_file}: {str(e)}")
        
        print(f"Completed {domain_folder}: Merged {files_merged} files, skipped {files_skipped} files")
        print(f"Output saved to {output_file_path}")
def data_cleaning():
    print("Starting content merging process...")
    merge_website_content()
    print("Content merging complete!")
if __name__ == "__main__":
    print("Starting content merging process...")
    merge_website_content()
    print("Content merging complete!")