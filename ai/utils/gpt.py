from io import BytesIO
import requests
from PyPDF2 import PdfReader
import pandas as pd
from bardapi import Bard
from numpy import random
from time import sleep
import openai
import os

openai.api_key = os.environ['_CHATGPT_API_KEY']
HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Windows; Windows x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36'}
EOF_MARKER = b'%%EOF'

class Gpt:

    def __init__(self, csv):
        self.csv = csv
        self.dataframe = pd.read_csv(csv)

    def get_df(self):
        return self.dataframe

    @staticmethod
    def isnull(frame):
        return pd.isnull(frame)

    def reducewords(text, numofwords):
        return ' '.join(text.split()[:numofwords])

    def randomsleep(self, ):
        sleeptime = random.uniform(2, 4)
        print("SLEEPING FOR:", sleeptime, "seconds")
        sleep(sleeptime)
        print("SLEEP OVER.")

    def fixpdf(self, pdf_file_on_mem):
        pdf_file_on_mem.write(EOF_MARKER)
        pdf_file_on_mem.seek(0)
        return pdf_file_on_mem

    def grabfiletomemory(self, url):
        response = requests.get(url=url, headers=HEADERS, timeout=120)
        return BytesIO(response.content)

    def pdftotext(self, url):
        pdf_file_on_mem = self.grabfiletomemory(url)
        pdf_file = PdfReader(pdf_file_on_mem)

        ocr = ''
        for page_number in range(len(pdf_file.pages)):   # use xrange in Py2
            page = pdf_file.pages[page_number]
            page_content = page.extract_text()
            ocr += page_content

        return ocr

    def bard(self, prompt):
        bard = Bard(timeout=30)
        return bard.get_answer(prompt)['content']

    def chatgpt(self, prompt, model="gpt-3.5-turbo"):
        response = openai.Completion.create(
          model="text-davinci-003",
          prompt=prompt,
          temperature=0.7,
          max_tokens=256,
          top_p=1,
          frequency_penalty=0,
          presence_penalty=0
        )

        message = response.choices[0].text.strip()
        return message