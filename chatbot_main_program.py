# kwldge&vctr_base.txt must be present to run main program
import google.generativeai as genai
import google.api_core.exceptions
import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import scrolledtext
import tkinter.font as tkfont

api_key = "CREATE-AN-API-KEY-YOURSELF-IN-GOOGLE-AI-STUDIO"
genai.configure(api_key=api_key)
# customize response configuration for optimized generation
config = genai.types.GenerationConfig(top_k=1, top_p=0.0, temperature=1.5, max_output_tokens=300)
# gemini LLM
model = genai.GenerativeModel("gemini-1.5-flash-latest")
chat = model.start_chat()


# create vector embedding
def embed_text(content):
    # call gemini embedding model
    try:
        return genai.embed_content(model="models/text-embedding-004", content=content, task_type="retrieval_document")[
            "embedding"]
    # vector created --> a list of (-1 < float < 1)
    except Exception as e:
        print(f"Error embedding content: {e}")
        return None


# create dataframe with 3 fields
df = pd.DataFrame(columns=["Title", "Text", "Embeddings"])

with (open("kwldge&vctr_base.txt", "r", encoding="utf-8") as file):
    lines = file.readlines()
    # 1 record has data in 3 fields
    for record in range(0, len(lines), 3):
        # field one: chapter name
        file_name = lines[record]
        # field two: chapter content
        text = lines[record + 1]
        # field three: content embedding
        embedding = lines[record + 2].replace("[", "").replace("]", "")
        embedding = embedding.replace("\n", "").replace(" ", "")
        vector_list = embedding.split(",")
        temporary_embeddings = []
        for item in vector_list:
            vector = float(item)
            # all dimensions of a chapter put together
            temporary_embeddings.append(vector)

        # following code is to separate the dimensions into groups of 768
        # to ensure it has the same dimensions as query's for successful similarity search
        embeddings = []
        nested_embeddings = []
        for item in range(0, len(temporary_embeddings)):
            if float(item / 768) in range(100):
                nested_embeddings = []
            nested_embeddings.append(temporary_embeddings[item])
            if len(nested_embeddings) == 768:
                embeddings.append(nested_embeddings)

        # inserting values in a new dataFrame row
        new_row = pd.DataFrame({"Title": [file_name], "Text": [text], "Embeddings": [embeddings]})
        # indexing according to previous rows
        df = pd.concat([df, new_row], ignore_index=True)


# retrieve most similar document
def most_similar_document(query):
    df["Similarity"] = df["Embeddings"].apply(lambda vectors: query_similarity_score(query, vectors))
    title = df.sort_values("Similarity", ascending=False).iloc[0]["Title"]
    text = df.sort_values("Similarity", ascending=False).iloc[0]["Text"]
    return title, text


# function to calculate similarity score
def query_similarity_score(query, vectors):
    query_embedding = embed_text(query)
    similarity_scores = [np.dot(query_embedding, vector) for vector in vectors]
    return max(similarity_scores)


# chat history record creation
chat_record = {"input": [], "response": []}

# prompt engineering to instruct LLM
instruction = (f"Only respond to mathematics-related questions, events or people. "
               f"Those also include like taxation and insurance."
               f"If they ask otherwise, respond with \"I will only respond to mathematics-related enquiries.\"\n"
               f"If you understand, respond \"Hello! How can I help you?\"\n"
               f"Only exception for above rule is when greeting user or having short small talks.")

understood = chat.send_message(instruction)
chat_record["input"].append(instruction)
chat_record["response"].append(understood.text)


# GUI and response generation
# note: maximize GUI window for optimal UI
class MathChatbot:
    # constructor to create instance variable
    def __init__(self, root):
        # self: current object instance
        # root: referring GUI window instance
        self.root = root
        self.root.title("Mathematics Chatbot")
        font = tkfont.Font(size=14)
        font2 = tkfont.Font(size=17)

        self.chat_history = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=170, height=35)
        self.chat_history.grid(row=1, columnspan=2, padx=30, pady=20)

        self.user_input = tk.Entry(root, width=100, font=font)
        self.user_input.grid(row=3, column=0, padx=40, pady=15, sticky="ew")
        self.user_input.insert(0, '\U000025B6 Type your question here')
        self.user_input.config(fg='grey')
        self.user_input.bind('<FocusIn>', self.user_entry)
        self.user_input.bind('<FocusOut>', self.user_exit)
        self.user_input.bind("<Return>", self.send_message)

        self.send_button = tk.Button(root, text="Send", command=self.send_message)
        self.send_button.grid(row=3, column=1, padx=20, pady=10)
        self.chat_history.insert(tk.END, "Chatbot: Good day! Ask me anything about maths in KSSM syllabus! \U0001F44B")
        self.end_statement = tk.Label(root, text="\U000026A0 Chatbot will only reply to mathematics question            \U000026A0 Wait patiently for response          \U000026A0 Type \"end\" to end conversation")
        self.end_statement.grid(row=2, padx=0, pady=2)
        self.end_statement = tk.Label(root, text="\U00002795\U00002796\U00002716\U00002797 MATHEMATICS CHATBOT \U0001F4BB", font=font2)
        self.end_statement.grid(row=0, column=0, columnspan=1, padx=0, pady=2)

    # entry bar UI
    def user_entry(self, event):
        if self.user_input.get() == "\U000025B6 Type your question here":
            self.user_input.delete(0, tk.END)
            self.user_input.insert(0, '')
            self.user_input.config(fg="black")

    # entry bar UI
    def user_exit(self, event):
        if self.user_input.get() == "":
            self.user_input.insert(0, "\U000025B6 Type your question here")
            self.user_input.config(fg='grey')

    # augment response
    def send_message(self, event=None):
        # terminate program shortcut
        query = self.user_input.get()
        if query.lower() == "end":
            exit()

        self.chat_history.insert(tk.END, f"\n\nYou: {query}\n")
        chat_record["input"].append(query)
        self.user_input.delete(0, tk.END)
        # feedback to show that query is accepted
        self.chat_history.insert(tk.END, "\nProcessing...\U000023F3\n\n\n")
        self.chat_history.yview_moveto(1)
        self.root.update()

        # similarity matching
        title, text = most_similar_document(query+". If my previous question is mathematics-related, remember source")
        print(text)

        # augmentation and prompt engineering
        prompt = (f"Input:{query}\n\nThis is the past conversation of me (input) and you (response):\n[\n{chat_record}\n]"
                  f"\n\nMatch the input and response according to the index in the dictionary's list. "
                  f"Based on our past conversation, respond to my input accordingly."
                  f"\n\nGreet back and do casual talks if I initiate it, while ignoring the text below."
                  f"\n\nContext given:\n{text}\n\n"
                  f"The context given is your primary information source, "
                  f"so synthesise your understanding of the topic with the context, "
                  f"and produce a comprehensive response."
                  f"\n\nPrioritize the way of explaining a topic from the context."
                  f"\nYou MUST respond to mathematical questions with \"Source:{title}\" at the start of every response."
                  f"\n\nWhen responding, treat as if I did not tell you about the context."
                  f"\n\nIf context is irrelevant, ignore completely."
                  f"\n\nAfter that, check if your response aligns with our past conversation. "
                  f"If it does not make sense with past conversation, change it accordingly "
                  f"and don't include source as mentioned above."
                  f"\n\nOrganize your response neatly in paragraphs and bullet points.")

        # produce response
        try:
            response = chat.send_message(prompt)
            # only get text part of response
            response_text = response.text

        # handle occasional errors
        except genai.types.generation_types.StopCandidateException:
            response_text = "An error occurred. Try again"
        except google.api_core.exceptions.InternalServerError:
            response_text = "An error occurred. Try again"

        self.chat_history.insert(tk.END, f"\nChatbot:\n{response_text}\n\n")
        # save response in chat history
        chat_record["response"].append(response_text)
        self.chat_history.yview(tk.END)
        self.send_button.focus_set()


root = tk.Tk()
app = MathChatbot(root)
root.mainloop()
