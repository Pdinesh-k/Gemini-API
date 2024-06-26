from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
import google.generativeai as genai

from langchain_text_splitters import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings,ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_pdf_text(pdfs):
    text = ""
    for pdf in pdfs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text+=page.extract_text()
    return text

def get_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 10000 , chunk_overlap = 1000)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    vector_store = FAISS.from_texts(chunks,embedding = embeddings)
    vector_store.save_local("faiss-index")

def get_conversation_chain():
    prompt_template = """
    Answer every question I am providing by looking into the provided context , make sure
    to answer the questions from provided context only , if the answer is not provided
    in context just say , "answer 
    Context :\n {context}\n
    Question : \n{question}\n

    Answer:
    """

    model = ChatGoogleGenerativeAI(model = "gemini-pro",temperature = 0.3)
    prompt = PromptTemplate(
        template=prompt_template , input_variables = ["context","question"]
    )

    chain = load_qa_chain(model,chain_type="stuff",prompt=prompt)
    return chain

def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model  ="models/embedding-001")
    db = FAISS.load_local("faiss-index",embeddings,allow_dangerous_deserialization=True)
    docs = db.similarity_search(user_question)
    chain = get_conversation_chain()

    response = chain(
        {"input_documents" : docs , "question" : user_question},return_only_outputs=True
    )
    print(response)
    st.write("Reply: ",response["output_text"])

def main():
    st.set_page_config("Chat PDF")
    st.header("Chat with PDF using Gemini")

    user_question = st.text_input("Ask a question from the PDF files")

    if user_question:
        user_input(user_question)

    with st.sidebar:
        st.title("Menu:")
        pdf_docs = st.file_uploader(
            "Upload your PDF Files and Click on the Submit & Process Button",
            accept_multiple_files=True
        )
        if st.button("Submit & Process"):
            with st.spinner("Processing..."):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_chunks(raw_text)
                get_vector_store(text_chunks)
                st.success("Done")
if __name__ == "__main__":
    main()






