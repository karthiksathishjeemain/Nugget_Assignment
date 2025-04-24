import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import time
import re
import html2text

def sanitize_filename(url):
    """Convert URL to a valid filename by replacing invalid characters"""
    parsed = urlparse(url)
    path = parsed.path
    
    filename = re.sub(r'[\\/*?:"<>|]', "_", path)
    filename = filename.replace("/", "__")
    
    if filename == "" or filename == "__":
        filename = "index"
    
    filename = filename.lstrip("_")
    if not filename.endswith(".txt"):
        filename += ".txt"
    
    return filename

def remove_extra_newlines(text):
    """Remove empty lines and excessive whitespace"""
    cleaned_text = re.sub(r'\n\s*\n', '\n', text)
    cleaned_text = '\n'.join(line.rstrip() for line in cleaned_text.splitlines())
    return cleaned_text

def extract_content(url):
    """Extract main content from a webpage"""
    try:
    
        time.sleep(0.5)
        
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
   
        if 'text/html' not in response.headers.get('Content-Type', ''):
            return f"[Non-HTML content: {response.headers.get('Content-Type', 'unknown')}]"
        soup = BeautifulSoup(response.text, "html.parser")
    
        for script in soup(["script", "style", "iframe", "nav", "footer"]):
            script.extract()
      
        main_content = None
        
        for container in ["main", "article", "div.content", "div.main", "#content", "#main"]:
            content_section = soup.select_one(container)
            if content_section:
                main_content = content_section
                break
   
        if not main_content:
            main_content = soup.body
   
        h = html2text.HTML2Text()
        h.ignore_links = False
        h.ignore_images = True
        
        title = soup.title.text if soup.title else "No Title"
       
        text_content = h.handle(str(main_content))
        full_content = f"Title: {title.strip()}\nURL: {url}\n\n{text_content}"
        
        cleaned_content = remove_extra_newlines(full_content)
        
        return cleaned_content
    
    except Exception as e:
        return f"Error extracting content: {str(e)}"

def process_href_files():

    href_dir = "href"
    if not os.path.exists(href_dir):
        print(f"Error: {href_dir} directory not found")
        return
    
    data_dir = "data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
   
    for filename in os.listdir(href_dir):
        if not filename.endswith(".txt"):
            continue
        
        file_path = os.path.join(href_dir, filename)
        domain = filename.replace(".txt", "")
        
        domain_dir = os.path.join(data_dir, domain)
        if not os.path.exists(domain_dir):
            os.makedirs(domain_dir)
        
        print(f"Processing URLs from {filename}...")
  
        with open(file_path, "r") as file:
            urls = [line.strip() for line in file if line.strip()]
        
   
        for i, url in enumerate(urls):
            try:
              
                output_filename = sanitize_filename(url)
                output_path = os.path.join(domain_dir, output_filename)
                
            
                if os.path.exists(output_path):
                    print(f"[{i+1}/{len(urls)}] Already processed: {url}")
                    continue
                
                print(f"[{i+1}/{len(urls)}] Extracting: {url}")
                
              
                content = extract_content(url)
                
            
                with open(output_path, "w", encoding="utf-8") as output_file:
                    output_file.write(content)
                
                print(f"Saved content to {output_path}")
                
            except Exception as e:
                print(f"Error processing {url}: {str(e)}")
        
        print(f"Completed processing {len(urls)} URLs from {filename}")
def data_collection():
    print("Starting content extraction...")
    process_href_files()
    print("Content extraction complete!")
if __name__ == "__main__":
    print("Starting content extraction...")
    process_href_files()
    print("Content extraction complete!")