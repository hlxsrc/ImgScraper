# Python script for scraping images from websites like www.google.com
# This script is intented to help in the creation of an image database

# Imports
import hashlib
import argparse
from PIL import Image
import io, os
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Receive arguments
ap = argparse.ArgumentParser()
ap.add_argument("-st", "--searchterm", required=True,
                help="Term to search")
ap.add_argument("-n", "--numofimages", required=True,
                help="number of images to retrieve")
ap.add_argument("-o", "--output", required=True,
                help="path to output directory")
args = vars(ap.parse_args())

# Search and download images
def search_and_download(search_term:str, number_images=5, target_path='./images'):
    
    target_folder = os.path.join(target_path,'_'.join(search_term.lower().split(' ')))

    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # Create Chrome Driver service
    s = Service(ChromeDriverManager().install())

    with webdriver.Chrome(service=s) as wd:
        res = fetch_image_urls(search_term, int(number_images), wd=wd, sleep_between_interactions=1)
        
    for elem in res:
        persist_image(target_folder,elem)

# Store images in path 
def persist_image(folder_path:str, url:str):

    try:
        image_content = requests.get(url, timeout=4).content

    except Exception as e:
        print(f"ERROR - Could not download {url} - {e}")

    try:
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert('RGB')
        file_path = os.path.join(folder_path,hashlib.sha1(image_content).hexdigest()[:10] + '.jpg')
        with open(file_path, 'wb') as f:
            image.save(f, "JPEG", quality=85)
        print(f"SUCCESS - saved {url} - as {file_path}")

    except Exception as e:
        print(f"ERROR - Could not save {url} - {e}")

# Search for a particular image
# Get image links
def fetch_image_urls(query:str, max_links_to_fetch:int, 
        wd:webdriver, sleep_between_interactions:int=1):

    # Function to scroll to end of page
    def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(sleep_between_interactions)    
    
    # Build the google query
    if query[0:4] == 'http':
        search_url = query
        # Load the page
        wd.get(search_url)
    else:
        # TODO: Remove "\" characters from url
        search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"
        # Load the page
        wd.get(search_url.format(q=query))

    # Load the page
    wd.get(search_url.format(q=query))

    image_urls = set()
    image_count = 0
    results_start = 0
    while image_count < max_links_to_fetch:
        scroll_to_end(wd)

        # Get all image thumbnail results
        thumbnail_results = wd.find_elements(By.CSS_SELECTOR, 'img.Q4LuWd')
        number_results = len(thumbnail_results)
        
        print(f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}")
        
        for img in thumbnail_results[results_start:number_results]:

            # Try to click every thumbnail 
            # such that we can get the real image behind it
            try:
                img.click()
                time.sleep(sleep_between_interactions)
            except Exception:
                continue

            # Extract image urls    
            actual_images = wd.find_elements(By.CSS_SELECTOR, 'img.n3VNCb')
            for actual_image in actual_images:
                if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                    image_urls.add(actual_image.get_attribute('src'))

            image_count = len(image_urls)

            if len(image_urls) >= max_links_to_fetch:
                print(f"Found: {len(image_urls)} image links, done!")
                break

        else:
            print("Found:", len(image_urls), "image links, there are no more links...")
            break

        # Move the result startpoint further down
        results_start = len(thumbnail_results)

    return image_urls

# Execute search and download
search_and_download(args["searchterm"],args["numofimages"],args["output"])

