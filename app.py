import requests
import json
import subprocess
import os
import base64
import dropbox
from dropbox.exceptions import AuthError, ApiError
import re
import config

main_page_id = os.environ.get("MAIN_PAGE_ID")
notion_token = os.environ.get("NOTION_TOKEN")
access_token = os.environ.get("DROPBOX_TOKEN")

def convertPDFtoImages(pdfPath, outputFolderName):
    pdf_file_path = pdfPath
    output_directory = "/home/parm/Documents/{name}".format(name=outputFolderName)

    # Create the output directory if it doesn't already exist
    os.makedirs(output_directory, exist_ok=True)
    subprocess.run(["pdftoppm", "-png", "-r", "300", pdf_file_path, os.path.join(output_directory, "page")])    
    return output_directory

def upload_images_to_dropbox(folder_path, destination_folder):
    try:
        dbx = dropbox.Dropbox(access_token)

        for file_name in os.listdir(folder_path):
            image_path = os.path.join(folder_path, file_name)
            if os.path.isfile(image_path):
                with open(image_path, 'rb') as file:
                    image_data = file.read()

                upload_path = f'/{destination_folder}/{file_name}'
                dbx.files_upload(image_data, upload_path)

        return "Images uploaded successfully to Dropbox"

    except dropbox.exceptions.AuthError as e:
        return f"Error authenticating Dropbox API: {e}"
    except Exception as e:
        return f"Error uploading images to Dropbox: {e}"

def get_dropbox_image_urls(folder_path):
    try:
        dbx = dropbox.Dropbox(access_token)
        image_urls = []

        # Get the list of files in the specified folder
        files = dbx.files_list_folder(folder_path).entries

        for file in files:
            if isinstance(file, dropbox.files.FileMetadata):
                # Create a shareable link for the file
                shared_link = dbx.sharing_create_shared_link_with_settings(file.path_display)

                # Get the direct URL of the shared link
                direct_url = shared_link.url.replace("www.dropbox", "dl.dropboxusercontent")

                image_urls.append(direct_url)

        # Sort the image URLs based on the page number
        image_urls.sort(key=lambda url: int(re.findall(r'page-(\d+)\.png', url)[0]))
        return image_urls

    except dropbox.exceptions.AuthError as e:
        print(f"Error authenticating Dropbox API: {e}")
        return None
    except dropbox.exceptions.ApiError as e:
        print(f"Error retrieving Dropbox file metadata: {e}")
        return None

def addImagesToNotionPage(page_id, dropbox_image_urls):
    # Create Notion blocks with images and spaces inbetween
    blocks = []
    for i, url in enumerate(dropbox_image_urls):
        image_block = {
            "object": "block",
            "type": "image",
            "image": {
                "type": "external",
                "external": {
                    "url": url
                }
            }
        }
        blocks.append(image_block)

        # Insert a space block between image blocks except the last one
        if i < len(dropbox_image_urls) - 1:
            space_block = {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": " ",
                                "link": None
                            }
                        }
                    ],
                    "color": "default"
                }
            }
            blocks.append(space_block)

    # Prepare the blocks with their respective index
    indexed_blocks = [{"block": block, "index": i} for i, block in enumerate(blocks)]

    # Sort the blocks based on index
    indexed_blocks.sort(key=lambda x: x["index"])

    # Extract the sorted blocks
    sorted_blocks = [block["block"] for block in indexed_blocks]

    # Update the Notion page with the sorted blocks
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"

    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    payload = {
        "children": sorted_blocks
    }

    response = requests.patch(url, json=payload, headers=headers)

def createNotionPage(page_title):
    url = "https://api.notion.com/v1/pages"

    payload = {
        "parent": {
            "page_id": main_page_id
        },
        "properties": {
            "title": [
                {
                    "text": {
                        "content": page_title
                    }
                }
            ]
        },
        "children": [],
        "icon": None,
        "cover": None
    }

    headers = {
        "accept": "application/json",
        "Notion-Version": "2022-06-28",
        "content-type": "application/json",
        "Authorization": f"Bearer {notion_token}"
    }

    response = requests.post(url, json=payload, headers=headers)
    response_data = json.loads(response.text)
    
    page_id = response_data['id']
    return page_id

page_title = input("Enter page name: ")
new_page_id = createNotionPage(page_title)
pdf_path = input("Enter pdf path: ")
output_folder = input("Enter folder name for images: ")
output_directory_name = convertPDFtoImages(pdf_path, output_folder)
upload_images_to_dropbox(output_directory_name, output_folder)
dropbox_urls = get_dropbox_image_urls("/" + output_folder)
addImagesToNotionPage(new_page_id, dropbox_urls)
print("DONE")
