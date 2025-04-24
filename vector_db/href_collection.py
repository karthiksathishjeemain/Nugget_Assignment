import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import time
from collections import deque

def normalize_url(url):
    """Remove fragments and trailing slashes for consistent URL comparison"""
    url = url.split('#')[0]  
    if url.endswith('/'):
        url = url[:-1]  
    return url

def crawl_website(starting_url, max_depth=2):
   
    href_dir = "href"
    if not os.path.exists(href_dir):
        os.makedirs(href_dir)
    
    
    parsed_url = urlparse(starting_url)
    domain = parsed_url.netloc
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    
  
    visited = set()
    
   
    queue = deque([(normalize_url(starting_url), 0)])  # (url, depth)
    
  
    all_links = [starting_url]
    
    while queue:
        current_url, depth = queue.popleft()
        
        if current_url in visited or depth > max_depth:
            continue
        
        visited.add(current_url)
        print(f"Crawling: {current_url} (Depth: {depth})")
        
        try:
           
            time.sleep(0.5)
            
        
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            response = requests.get(current_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            if 'text/html' not in response.headers.get('Content-Type', ''):
                continue
         
            soup = BeautifulSoup(response.text, "html.parser")
        
            for a_tag in soup.find_all("a", href=True):
                href = a_tag["href"].strip()
                
              
                if not href or href.startswith(('javascript:', 'mailto:', 'tel:')):
                    continue
                
                absolute_url = urljoin(current_url, href)
                normalized_url = normalize_url(absolute_url)
                
               #I am doing this because the crawled url contains image urls which cant't be scarped to get any content
                parsed_path = urlparse(absolute_url).path.lower()
                if (any(parsed_path.endswith(ext) or parsed_path.find(ext + '?') > -1 
                        for ext in ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp')) or
                    '.jpg' in parsed_path or '.jpeg' in parsed_path or '.png' in parsed_path or
                    'facebook.com' in absolute_url.lower() or 
                    'youtube.com' in absolute_url.lower() or
                    'youtu.be' in absolute_url.lower() or
                    'dropbox' in absolute_url.lower() and any(img in absolute_url.lower() 
                                                            for img in ('.jpg', '.jpeg', '.png', '.gif'))):
                    continue
                
             
                parsed_href = urlparse(absolute_url)
                if parsed_href.netloc == domain:
                    all_links.append(absolute_url)
                    if normalized_url not in visited:
                       
                        if depth < max_depth:
                            queue.append((normalized_url, depth + 1))
                else:
                  
                    all_links.append(absolute_url)
            
        except Exception as e:
            print(f"Error crawling {current_url}: {str(e)}")
    
   
    filename = os.path.join(href_dir, f"{domain}.txt")
    with open(filename, "w") as output_file:
        for link in sorted(set(all_links)): 
            output_file.write(f"{link}\n")
    
    print(f"Successfully crawled {domain} and saved {len(set(all_links))} unique links to {filename}")


def href_collection(): 
 with open("websites.txt", "r") as file:
    websites = file.read().splitlines()

 for website_url in websites:
    if website_url.strip():  
        crawl_website(website_url)