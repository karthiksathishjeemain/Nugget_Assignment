import os
import re
from uuid import uuid4
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from langchain_core.documents import Document
from dotenv import load_dotenv
load_dotenv()
def extract_title(content):
    """Extract title from content if available"""
    title_match = re.search(r'Title: (.*?)(?:\n|$)', content)
    if title_match:
        return title_match.group(1).strip()
    return "No Title"

def clean_content(content):
    """Clean content by removing redundant elements"""
 
    content = re.sub(r'^Title: .*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'^URL: .*$', '', content, flags=re.MULTILINE)
    
 
    content = re.sub(r'\* \* \*', '', content)
    
 
    content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)
    
    return content.strip()

def upload_structured_content():
 
    url = os.getenv("QDRANT_URL")
    api_key = os.getenv("QDRANT_API_KEY")
    collection_name = "website_content_2"
    
 
    print("Initializing embedding model...")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    
  
    print("Connecting to Qdrant...")
    client = QdrantClient(
        url=url,
        api_key=api_key,
    )
    

    collections = client.get_collections().collections
    collection_exists = any(collection.name == collection_name for collection in collections)
    
    if not collection_exists:
        print(f"Creating collection: {collection_name}")
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=768,  
                distance=Distance.COSINE
            )
        )
    

    vector_store = QdrantVectorStore(
        client=client,
        collection_name=collection_name,
        embedding=embeddings,
    )
   
    website_urls = []
    try:
        with open("websites.txt", "r") as file:
            website_urls = [line.strip() for line in file if line.strip()]
        print(f"Found {len(website_urls)} websites in websites.txt")
    except FileNotFoundError:
        print("Error: websites.txt not found")
        return

    structured_content_dir = "structured_content"
    if not os.path.exists(structured_content_dir):
        print(f"Error: {structured_content_dir} directory not found")
        return
    
    documents = []
    uuids = []
    
    for filename in os.listdir(structured_content_dir):
        if not filename.endswith(".txt"):
            continue
        
        file_path = os.path.join(structured_content_dir, filename)
        domain = filename.replace(".txt", "")
        
        print(f"Processing content for domain: {domain}")
  
        website_url = next((url for url in website_urls if domain in url), domain)
        
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
       
            sections = re.split(r'={80}\s*', content)
            
   
            for section in sections[1:]:
                if not section.strip():
                    continue
   
                section_match = re.search(r'SECTION: (.*?)(?:\n|$)', section)
                section_title = section_match.group(1).strip() if section_match else "Unknown Section"
                
    
                clean_section = clean_content(section)
                
                if len(clean_section.split()) < 10:  
                    continue
                
        
                title = extract_title(section) or section_title
           
                doc = Document(
                    page_content=clean_section,
                    metadata={
                        "source": website_url,
                        "domain": domain,
                        "title": title,
                        "section": section_title
                    }
                )
                
                documents.append(doc)
                uuids.append(str(uuid4()))
                
                if len(documents) % 10 == 0:
                    print(f"Processed {len(documents)} sections so far...")
        
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")
    
  
    if documents:
        print(f"Uploading {len(documents)} documents to Qdrant...")
        vector_store.add_documents(documents=documents, ids=uuids)
        print("Upload complete!")
    else:
        print("No documents to upload.")
   
    print("\nTesting search functionality...")
    query = "In which restaurant is burger available?"
    results = vector_store.similarity_search(query, k=2)
    
    print(f"\nSearch results for: '{query}'")
    for i, res in enumerate(results):
        print(f"\nResult {i+1}:")
        print(f"Title: {res.metadata.get('title', 'No Title')}")
        print(f"Source: {res.metadata.get('source', 'Unknown')}")
        print(f"Section: {res.metadata.get('section', 'Unknown')}")
        print("Content excerpt: " + res.page_content[:150] + "...")
def store():
    print("Starting content upload process...")
    upload_structured_content()
    print("Content upload process complete!")
if __name__ == "__main__":
    print("Starting content upload process...")
    upload_structured_content()
    print("Content upload process complete!")