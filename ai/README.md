# PDF Summarizer

## Install Prerequisites
* ~~pip install git+https://github.com/dsdanielpark/Bard-API.git~~ DO NOT USE BARD.  IT WILL DISABLE YOUR ACCOUNT FOR HIJACKING THE SESSION.
* pip install pandas
* pip install PyPDF2
* pip install numpy
* pip install openai

## Set up the CSV
* Open the CSV in a text editor
* Disable wrapping
* Add this new line at the end of the file:

    ``url-to-the-pdf-file.pdf,,,``
* The columns correspond to url,pdf-to-text,summary-from-ai
* Save and close

## The process
1. The script opens the csv and checks for rows with no summary.
2. It downloads the pdf into the memory.
3. It converts the pdf to text.
4. Then asks ChatGPT to summarize the pdf text.

## Running it
1. Go to https://platform.openai.com/
2. Generate an API Key
2. Go to the terminal and run this to set environment variable

    ``export __CHATGPT_API_KEY=[YOUR-API-KEY]``
3. Run ``python pdf-summarizer.py``
