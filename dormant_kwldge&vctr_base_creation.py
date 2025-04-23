# ***ALREADY RUN, NO RUN NEEDED***
# only for initial launch (ONE SINGLE LAUNCH)
# to use chatbot, run main program


# has read textbook text from local directory (segregated by chapters)
# embed text into vectors
# insert all textbook information (fields: title, text, vector) into kwldge&vctr_base.txt file
# main program (chatbot_main_program.py) read kwldge&vctr_base.txt file --> faster retrieval speed

import os
from PyPDF2 import PdfReader
import google.generativeai as genai
import regex as re
import nltk

nltk.download('stopwords')  # download NLTK stopwords
api_key = "AIzaSyAkssPj2hLfFKj-hdnL663Edf3LBq_zO38"
genai.configure(api_key=api_key)


def embed_text(content):
    # call gemini embedding model
    return genai.embed_content(model="models/text-embedding-004", content=content, task_type="retrieval_document")[
            "embedding"]
    # vector created --> a list of (-1 < float < 1)


def text_chomper(content):
    # function to break down lengthy text string from a file
    # to bypass gemini api's embedding request size limit (10000 bytes)
    text_list = []
    for char_idx in range(0, len(content), 5000):
        text_chunk = content[char_idx:char_idx + 5000]
        text_list.append(text_chunk)
    return text_list


# when launching, each chapters' PDFs are located in this directory
directory = 'C:/Users/Khoo Guo Hao/OneDrive/Desktop/Documents/Maths PDFs 2'

# read all files containing contents of all chapters in Maths and AddMaths (Form 4 & 5)
# 36 chapters in 4 textbooks
for file_name in os.listdir(directory):
    filePath = os.path.join(directory, file_name)

    with open(filePath, 'rb') as file:
        pdf_reader = PdfReader(file)
        text = ""

        for page_num in range(len(pdf_reader.pages)):
            # text in every object (page) is extracted
            text += pdf_reader.pages[page_num].extract_text()

        text = re.sub(r"\s+", " ", text)  # remove extra spaces
        text = re.sub(r"[^\w\s]", "", text)  # remove punctuations
        text = text.lower()  # convert text to all lowercase

        # Tokenize and remove stopwords
        stopwords = nltk.corpus.stopwords.words('english')  # stopwords list
        text_words = nltk.tokenize.word_tokenize(text)
        filtered_words = [word for word in text_words if word not in stopwords]  # remove stopwords

        text = " ".join(filtered_words)  # join all words together
        # remove blank lines
        # cut textbook in half --> more accurate similarity search
        halver = round(len(text) / 2)
        text1 = f"**Topic: {file_name}**{text[:halver]}"
        text2 = f"**Topic: {file_name}**{text[halver:]}"

    text_chunks = text_chomper(text1)
    # separate text into multiple chunks
    vector_list1 = []
    # embed text chunks individually
    for chunk in text_chunks:
        vector = embed_text(chunk)
        vector_list1.append(vector)

    text_chunks = text_chomper(text2)
    vector_list2 = []
    # embed text chunks individually
    for chunk in text_chunks:
        # embedding of one chunk of text
        vector = embed_text(chunk)
        vector_list2.append(vector)

    # vector lists is the combination of multiple chunks of text (which make up one chapter)
    # each chunk of text turns into embeddings of 768 dimensions during embedding process
    # hence, one vector list will have 768 x a of embedding dimensions, where a is the number of text chunk
    vector_list = 0
    # write data in text file
    # 1 record will be represented in 3 lines (3 fields)
    # 1st line: chapter name, 2nd line: chapter text, 3rd line: vector embedding
    with open("kwldge&vctr_base.txt", "w", encoding="utf-8") as file:
        file.write(file_name + "\n")
        file.write(text1 + "\n")
        file.write(str(vector_list1) + "\n")
        # 2nd half of textbook
        file.write(file_name + "\n")
        file.write(text2 + "\n")
        file.write(str(vector_list2) + "\n")





