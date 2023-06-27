import argparse
import os
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

def download_image(image_url, save_path):
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(save_path, "wb") as file:
            file.write(response.content)
        print("Image downloaded:", save_path)
    else:
        print("Failed to download image:", save_path)

def is_image_extension(extension):
    allowed_extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]
    return extension.lower() in allowed_extensions

def process_page(url, save_path, max_depth, current_depth=0):
    if current_depth > max_depth:
        return

    if not url.startswith("http://") and not url.startswith("https://"):
        return
    
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        
        # Extract image URLs
        img_tags = soup.find_all("img")
        for img_tag in img_tags:
            if "src" not in img_tag.attrs:
                continue
            image_url = urljoin(url, img_tag["src"])
            extension = os.path.splitext(image_url)[1]
            if is_image_extension(extension):
                image_name = os.path.basename(urlparse(image_url).path)
                save_file_path = os.path.join(save_path, image_name)
                download_image(image_url, save_file_path)

        # Recursively process linked pages
        href_tags = soup.find_all("a", href=True)
        for href_tag in href_tags:
            link_url = urljoin(url, href_tag["href"])
            process_page(link_url, save_path, max_depth, current_depth + 1)
    else:
        print("Failed to fetch page:", url)
        print("Status code:", response.status_code)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A web spider program that downloads images recursively.")
    parser.add_argument("-r", action="store_true", help="Recursively download images.")
    parser.add_argument("-l", type=int, default=5, help="The maximum depth level for recursive download.")
    parser.add_argument("-p", "--path", default="./data/", help="The path where the downloaded files will be saved.")
    parser.add_argument("URL", help="The URL of the website to crawl.")

    args = parser.parse_args()

    url_to_crawl = args.URL
    download_recursively = args.r
    max_depth = args.l
    save_path = args.path
    current_depth = 0

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    if not download_recursively:
        current_depth = max_depth

    process_page(url_to_crawl, save_path, max_depth, current_depth)
