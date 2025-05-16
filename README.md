# AI Chatbot with Gemini LLM - Overview
This Python project is an assignment for the Introduction to Artificial Intelligence (AI) module in semester 3 of my diploma program at APU. The development of this project is solely from my own contribution. However, credits to my teammates who contributed significantly in documentation, which include Kee Wen Yew, Joshua Liew Yi-Way, Colwyn Pang and Chang Hin Yew. Unlike my PPE management system project in my diploma semester 3, this project contains a simple graphical user interface for user interaction with the chatbot.

The development of the AI chatbot aims to become a virtual assistant that helps to resolve mathematical problems based on the contents of Form 4 and Form 5 syllabus of the KSSM mathematics subjects (Form 4 and Form 5 in other words, means higher-level secondary school education in Malaysia). These two subjects are Mathematics and Additional Mathematics. KSSM mathematics mainly focuses on five main areas of learning that are interconnected with each other: Numbers and Operations, Measurement and Geometry, Relation and Algebra, Statistics and Probability and Discrete Mathematics. This new syllabus mainly emphasizes on developing Higher Level Thinking Skills (KBAT) in students. This prompts the idea of this project. 
<br>
### Context: Why haven't you used chatbot development platforms / websites for this?
Initially, our team picked Botsonic, an online chatbot creating platform to develop our solution for the assignment. However, the free version of Botsonic has several limitations, such as limited source uploads, low customization, occasional inaccurate response or hallucinations, etc. Other chatbot development platforms echo similar issues. Besides, and ultimately, those platforms would lead to the creation of a rule-based chatbot, which my team finds pointless at the time due to our project scope (e.g., a help-and-support chatbot is suitable to be rule-based, but not for a chatbot that solves mathematical problems). 

Understanding our situation, our lecturer, Ts. Dr. Law Foong Li has suggested us to integrate Google's LLM - Gemini in a chatbot program developed using Python programming language. An online tutorial is provided for me to follow along and create the AI chatbot for my team's assignment. 

This technique allows our team to benefit from Gemini’s natural language processing (NLP) technology offered by Gemini. In addition, Python programming provides us freedom in developing and customizing a program that tailors to our project’s need. Most importantly, the retrieval augmented generation (RAG) technique is made possible because of Python’s comprehensive library. 
<br>
*Important: This repository is only intended solely for academic reference and personal learning. It should not be reused or resubmitted as original work under any circumstance. Unauthorized reproduction or misuse is strictly discouraged.*
<br>

# Project Design and Development Details (How The Program Works)
The design idea of the chatbot revolves around ensuring it responds to queries accurately using reliable information source. At initial launch, the chatbot should first greet users. Then users are allowed to type any input they want in English, which then prompts the chatbot to generate a response based on the context of the current KSSM syllabus. This is by extracting wordings and knowledge directly from the most reliable source in the syllabus - KSSM Mathematics and Additional Mathematics textbooks. Realizing this process involves creating a knowledge base for the chatbot to retrieve information from. If the query is similar enough to any data in the knowledge base, the data will be taken as a reference point for the chatbot to respond.

## Chatbot Development Process (Important for Setup)
### 1. Environment and Library Setup
Development tools and technologies (Python Interpreter & PyCharm) are first installed and set up. After that, relevant Python packages and libraries are installed from PyCharm’s setting. With the development environment ready, libraries are initially imported in the script.


### 2. API, LLM Model and Parameter Configuration
Our team created a unique Gemini Application Program Interface (API) key in Google’s AI Studio after logging in with a Google account.

With API key in hand, it can be configured in the development environment to start making API call for Gemini AI. Meanwhile, Gemini Flash 1.5 (latest version) was initialized as the LLM model that acts as the base of our chatbot.

*Note: And speaking of the API key, the API key used in the program could have expired by now. To test the program, you might need to create a new API key in Google's AI Studio, then replace the old key that can be found in **chatbot_main_program.py**.*

Once the model is specified, AI generated text responses can be produced. However, as prior discussions, our chatbot needs to respond to mathematical questions with respect to the KSSM syllabus. Hence, the retrieval augmented generation (RAG) methodology is applied for the chatbot. Methodologies such as tokenization, vectorization, and cosine similarity matching are required to implement RAG in our chatbot. The following procedures will clarify how they are achieved.


### 3. Knowledge Base and Vector Store Creation
In RAG, text preprocessing, including tokenization and vectorization are vital to convert human language into a machine-understandable format known as vectors (floating-point numbers). Therefore, our project utilizes text preprocessing technique to create a vector store that is suitable to carry out input similarity search. In essence, vector store is a data structure containing data in the form of vector embedding (floating point numbers).

In our project, all four mathematics textbooks are segregated into several PDF files, each file containing content of only one single chapter. These PDF files are initially stored in the local directory of file explorer. After pointing the program to retrieve these PDF files from the file location, PdfReader is used to convert the content read from PDF files into Python strings. The strings from each textbook chapter will be tokenized and embedded into vector embedding by employing embed_content(), a method within Gemini AI Python SDK. Lastly, all the data (file name, chapter content, and text embedding of all PDF files) are stored in a text file named **"kwldge&vctr_base.txt"**. Knowledge base creation is complete after all files in the directory have their texts and embeddings stored in the **kwldge&vctr_base.txt**.

The entire process of creating a knowledge base via use of text file will be conducted by running the **dormant_kwldge&vctr_base_creation.py** Python program. The program only requires a one-time execution for to enable initial launch. It is a separate Python file from the main program, **chatbot_main_program.py**. Since the knowledge base is already created by our team, **dormant_kwldge&vctr_base_creation.py** does not need to be run anymore. Attachment of the file is only for reference purpose. 


### 4. Cosine Similarity Search During Chat Session (chatbot_main_program.py)
With knowledge base in place, when the main program, **chatbot_main_program.py** is run, a vector store is created as a two-dimensional data frame by utilizing pandas library. Alike knowledge base, the vector store will also consist of 3 fields mentioned. The vector data from **kwldge&vctr_base.txt** will be retrieved and stored in the vector store, wating for similarity search.

After vector store setup completes, our program starts a chat session with the user by prompting for input and then responding to it. This forms a multi-turn chat. With RAG in mind, a context must be generated and assigned to each input before requesting a response from LLM. 

Said context is fetched using technique known as cosine similarity search. Essentially, cosine similarity is a measure of similarity between two non-zero vectors to determine text similarity. Our program is able to calculate this similarity using dot() method from NumPy library. The resulting similarity index of two non-zero vectors ranges from -1 to 1. The closer the score is to 1, the higher the similarity between the two vectors, and vice versa.

In our project, cosine similarity between the vectorized query and each vector from the vector store will be calculated. Then, the document text with the highest similarity score will be retrieved and used to augment chatbot’s response to better suit user’s context.


### 5. Response Augmentation
With context available, we are able to augment response so that it is relevant to the syllabus of KSSM. Combining RAG methodology with prompt engineering, Gemini is able to generate responses that are accurate and appropriate according to user’s goal of using the chatbot.


## Takeways 
This project was a wild ride. This is mainly due to 3 things: I was still a beginner in Python, it is my first time working with API keys, and it is also my first time creating a GUI. It was a challenging process to complete the assignment. Nevertheless, other than RAG context occasionally being ignored and slow reponse generation, the project was a success in my eyes. But I bet there would be a ton of changes to be made for optimisation if I really dive deep into each line of code. 

I always appreciated this project because I feel like it is the turning point that really ignited my passion in programming and IT in general, which I felt were kind of boring up until semester 3 (and for spoilers, things would get super intense and interesting in the following semesters, plus, who knows what happens for degree, I am simultaneously scared but excited). I guess I like challenges. It keeps me going. The same should go to you to, whoever you are that might be reading. Never settle in your comfort zone, expand your horizon and learn something new everyday. That's at least for me, how I achieve satisfaction and my meaning in life. I might have went a bit too philosophical there...

