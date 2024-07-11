# PDF Summarizer

This script generates additional metadata to a PDF document.

Given with a url, the script analyzes the document and generates data for all the columns.

| url	| ocr	| description	| summary	| type	| subject	| locations	| agencies	| people|
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| https://www.courts.ca.gov/documents/lr-recidivism-reduction-fund-court-grant-program-ba2015.pdf|||||||||
| https://www.courts.ca.gov/documents/hwg_work-group-report.pdf|||||||||

## Install ollama
1. Download https://ollama.com/
2. Download a model: ollama pull llama3
3. Test in the terminal: ollama run llama3

## Install python
1. Set up pyenv and virtualenvwrapper: https://opensource.com/article/19/6/python-virtual-environments-mac
2. Create an environment for this project.
2. Go to this dir and run ```pip install -r requirements.txt --no-index```

## Preparing the spreadsheet
1. Copy template.csv and fill in the first column with links to PDFs accessible via the web.
2. The pdf-summarizer will fill in the other columns with generated content.

## Usage
```
python pdf-summarizer.py template.csv
```

## What's happening
1. The script loads the csv into Pandas DataFrame for easier manipulation of the rows.
2. It then parses the PDF file using PdfReader.

    a. TODO: Improve script to parse images inside PDF and perform an OCR, using Tesseract or similar.
3. Then it sends the data with a corresponding prompt to the local ollama.

    a. TODO: Remove the hard-coded prompts and make them configurable in the csv.

    b. TODO: Allow user to specify which model to use per column, ie use llama3 for short description, use gemma for grabbing topics.
4. Script saves the data to the csv file.