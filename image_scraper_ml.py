# Usage: python image_scraper_ml.py -st <"QUERY"> -dp </path/to/chromedriver> -n <N> -o </path/to/output>

# Python script for scraping images from websites like www.google.com
# This script is just for learning purposes
# As seen on Towards Data Science

# Imports
import hashlib
import argparse
from PIL import Image
import io, os
import requests
import time
from selenium import webdriver

# Receive arguments
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-st", "--searchterm", required=True,
                help="Term to search")
ap.add_argument("-dp", "--driverpath", required=True,
                help="path to driver file")
ap.add_argument("-n", "--numofimages", required=True,
                help="number of images to retrieve")
ap.add_argument("-o", "--output", required=True,
                help="path to output directory")
args = vars(ap.parse_args())

# Search and download images
def search_and_download(search_term:str,driver_path:str,number_images=5,target_path='./images'):
    
    target_folder = os.path.join(target_path,'_'.join(search_term.lower().split(' ')))

    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    with webdriver.Chrome(executable_path=driver_path) as wd:
        res = fetch_image_urls(search_term, int(number_images), wd=wd, sleep_between_interactions=0.5)
        
    for elem in res:
        persist_image(target_folder,elem)

# Store images in path 
def persist_image(folder_path:str,url:str):
    try:
        image_content = requests.get(url).content

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
    def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(sleep_between_interactions)    
    
    # Build the mercado libre query
    search_url = "https://listado.mercadolibre.com.mx/{q}#D[A:{q}]"

    # Load the page
    wd.get(search_url.format(q=query))

    # Get links to publications
    urls = set()
    links = wd.find_elements_by_css_selector("a.ui-search-link")
    link_results = len(links)
    for link in links:
        if link.get_attribute('href') and 'http' in link.get_attribute('href') and 'auto.' in link.get_attribute('href'):
            urls.add(link.get_attribute('href'))

    # Create variables to store image urls
    image_urls = set()
    image_count = 0
    
    while image_count < max_links_to_fetch:
        scroll_to_end(wd)

        # Load page for each url
        for url in urls:

            # Load the page
            wd.get(url)

            # Extract image urls    
            actual_images = wd.find_elements_by_css_selector('img.ui-pdp-gallery__figure__image')
            for actual_image in actual_images:
                if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                    image_urls.add(actual_image.get_attribute('src'))

            image_count = len(image_urls)

            # Show number of collected images and go back to previous url
            print("Found:", len(image_urls), "image links, looking for more ...\n")
            time.sleep(5)
            wd.execute_script("window.history.go(-1)")

            # Break if number of images is bigger or equal to number of desired images
            if len(image_urls) >= max_links_to_fetch:
                print(f"Found: {len(image_urls)} image links, done!")
                break

    return image_urls

# Execute search and download
search_and_download(args["searchterm"],args["driverpath"],args["numofimages"],args["output"])
