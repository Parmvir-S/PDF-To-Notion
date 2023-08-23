# PDF to Notion Automation Script


https://github.com/Parmvir-S/PDF-To-Notion/assets/70659748/fb0f0b68-761c-4dda-a228-c0c45508d4cf


## Overview

This Python automation script is designed to simplify the process of converting a PDF document into a series of images, uploading these images to Dropbox, and then inserting them with spaces in between on a newly created Notion page. The motivation behind this project was to save time and effort when preparing for lectures, where the user would typically take screenshots of each page of a PDF, insert them into Notion, and then add notes underneath each page. By automating this process, the user can focus more on the content of the lecture and less on the manual preparation of materials.

## Features

-   Converts each page of a PDF into images.
-   Uploads the images to Dropbox.
-   Generates shareable links for the images.
-   Creates a new Notion page with the PDF images and spaces in between for note-taking.

## How It Works

1.  The user provides the desired page title, the path to the PDF file, and a folder name for the images.
2.  The script converts each page of the PDF into images using the `pdftoppm` tool.
3.  The images are uploaded to Dropbox using the Dropbox API.
4.  Shareable links for the images are generated using Dropbox API and the links are adjusted to ensure they are accessible.
5.  A new Notion page is created with the provided title using the Notion API.
6.  The images and spaces are added to the Notion page, allowing for note-taking.

## Troubleshooting

While developing this project, a notable challenge was encountered when dealing with Notion's limitations on direct image uploads. Notion has restrictions on the number of blocks that can be added in a single API request. To overcome this limitation, the project integrates Dropbox. Instead of uploading the images directly to Notion, the images are uploaded to Dropbox, and shareable links are used to insert them into the Notion page. This approach ensures that the Notion page remains manageable and avoids potential issues related to block limitations.

## Conclusion

This project demonstrates the power of automation using Python to streamline repetitive tasks. By leveraging APIs from Notion and Dropbox, the script efficiently converts PDFs to images, uploads them to a cloud storage service, and integrates them seamlessly into Notion for note-taking. The motivation behind this project was to create a time-saving solution for preparing lecture materials, which could also be applied to various scenarios where image integration and organization are needed.

Feel free to adapt and modify the script to suit your specific use case!
