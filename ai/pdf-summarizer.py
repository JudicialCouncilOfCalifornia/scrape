from io import BytesIO
import requests
from PyPDF2 import PdfReader
import pandas as pd
from time import sleep
import openai
import os
import re
import sys
from Crypto.Cipher import AES
import ollama

filename = sys.argv[1]
# openai.api_key = os.environ['_CHATGPT_API_KEY']
HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Windows; Windows x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36'}
EOF_MARKER = b'%%EOF'

def reducewords(text, numofwords):
    text = re.sub(' +', ' ', text)
    text = text.replace('\r', '').replace('\n', '')
    return ' '.join(text.split()[:numofwords])

# def randomsleep():
#     sleeptime = random.uniform(2, 4)
#     print("SLEEPING FOR:", sleeptime, "seconds")
#     sleep(sleeptime)
#     print("SLEEP OVER.")

def fixpdf(pdf_file_on_mem):
    pdf_file_on_mem.write(EOF_MARKER)
    pdf_file_on_mem.seek(0)
    return pdf_file_on_mem

def grabfiletomemory(url):
    response = requests.get(url=url, headers=HEADERS, timeout=120)

    if (response.headers['Content-Type'] == "application/pdf"):
        return BytesIO(response.content)
    return False

def pdftotext(url):
    pdf_file_on_mem = grabfiletomemory(url)
    ocr = ''
    if (pdf_file_on_mem):
        pdf_file = PdfReader(pdf_file_on_mem)

        for page_number in range(len(pdf_file.pages)):   # use xrange in Py2
            page = pdf_file.pages[page_number]
            page_content = page.extract_text()
            ocr += page_content
    else:
        print("-- skipping")

    return ocr

def chatgpt(prompt, data, model="gpt-4-turbo"):
    response = openai.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt + ": \n\n" + data
            }
        ],
        temperature=0,
        max_tokens=1025,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].message.content.strip()

def llama(prompt, data, model='llama3'):
    response = ollama.chat(model, messages=[
        {
            'role': 'user',
            'content': prompt + ": \n\n" + data,
        },
    ])
    return response['message']['content']


pdfs = pd.read_csv(filename)

for i in pdfs.index:

    # if not pd.isnull(pdfs['ocr'][i]):

    try:
        ocr = pdfs['ocr'][i]
        print('*************')
        print('PROCESSING: ' + pdfs['url'][i])

        if pd.isnull(ocr):
            print('')
            print('------------')
            print('-- CONVERTING PDF to TEXT')
            pdfs.at[i, 'ocr'] = None
            pdfs.at[i, 'ocr'] = ocr = pdftotext(pdfs['url'][i]).strip()

        if ocr:
        #     # ocr = reducewords(ocr, 2000)

            if pd.isnull(pdfs['description'][i]):
                print('')
                print('------------')
                print('-- SHORT DESCRIPTION')
                answer = llama("Write a brief summary in three sentences or less about these data.", ocr)
                answer = answer.split("\n")
                answer = answer[-1]
                pdfs.at[i, 'description'] = None
                pdfs.at[i, 'description'] = answer if "Response Error" not in answer else None
                print(answer)

            if pd.isnull(pdfs['summary'][i]):
                print('')
                print('------------')
                print('-- SUMMARY')
                answer = llama("Summarize these data", ocr)
                answer = answer.split("\n")
                answer = answer[1:]
                answer = "\n".join(answer)
                pdfs.at[i, 'summary'] = None
                pdfs.at[i, 'summary'] = answer if "Response Error" not in answer else None
                print(answer)

            if pd.isnull(pdfs['type'][i]):
                print('-- TYPE')
                answer = llama("In one word, classify what type of document this is", pdfs['url'][i] + "\n" + ocr)
                # answer = answer.split("\n")
                # answer = answer[1:]
                # answer = "\n".join(answer)
                pdfs.at[i, 'type'] = None
                pdfs.at[i, 'type'] = answer if "Response Error" not in answer else None
                print(answer)

            if pd.isnull(pdfs['subject'][i]):
                print('')
                print('------------')
                print('-- SUBJECT')
                answer = llama("Extract subject matter tags related to law from these data. Separate the list by comma", ocr)
                answer = answer.split("\n")
                answer = answer[1:]
                answer = "\n".join(answer)
                pdfs.at[i, 'subject'] = None
                pdfs.at[i, 'subject'] = answer if "Response Error" not in answer else None
                print(answer)

            if pd.isnull(pdfs['locations'][i]):
                print('')
                print('------------')
                print('-- LOCATIONS')
                answer = llama("Extract locations from these data.  Separate by comma", ocr)
                # answer = answer.split("\n")
                # answer = answer[1:]
                # answer = "\n".join(answer)
                pdfs.at[i, 'locations'] = None
                pdfs.at[i, 'locations'] = answer if "Response Error" not in answer else None
                print(answer)

            if pd.isnull(pdfs['agencies'][i]):
                print('')
                print('------------')
                print('-- AGENCIES')
                answer = llama("Extract agencies and department from these data.  Separate by comma", ocr)
                # answer = answer.split("\n")
                # answer = answer[1:]
                # answer = "\n".join(answer)
                pdfs.at[i, 'agencies'] = None
                pdfs.at[i, 'agencies'] = answer if "Response Error" not in answer else None
                print(answer)

            if pd.isnull(pdfs['people'][i]):
                print('')
                print('------------')
                print('-- PEOPLE')
                answer = llama("Extract names of people from these data.  Separate by comma", ocr)
                # answer = answer.split("\n")
                # answer = answer[1:]
                # answer = "\n".join(answer)
                pdfs.at[i, 'people'] = None
                pdfs.at[i, 'people'] = answer if "Response Error" not in answer else None
                print(answer)

            pdfs.at[i, 'locations'] = pdfs['locations'][i].strip()
            pdfs.at[i, 'agencies'] = pdfs['agencies'][i].strip()
            pdfs.at[i, 'people'] = pdfs['people'][i].strip()
            pdfs.at[i, 'type'] = pdfs['type'][i].strip()
            pdfs.at[i, 'subject'] = pdfs['subject'][i].strip()

            # columns = ['locations', 'agencies', 'people', 'type', 'subject']
            # for c in columns:
            #     if not pd.isnull(pdfs[c][i]):
            #         answer = pdfs[c][i].split("\n")
            #         answer = answer[0]
            #         pdfs.at[i, c] = answer
            #         print(answer)

            if not pd.isnull(pdfs["agencies"][i]):
                search = ['none']
                for s in search:
                    if s in pdfs["agencies"][i].lower():
                        print(pdfs["agencies"][i])
                        pdfs.at[i, 'agencies'] = ''
                        continue

    except Exception as err:
        print('FAILED: ' + pdfs['url'][i])
        print(f"Unexpected {err=}, {type(err)=}")
        pass
        # fixed = fixpdf(pdf_file_on_mem)
        # pdfs.at[i, 'ocr'] = pdftotext(fixed)

pdfs.to_csv(filename, index=False, quotechar='"')
