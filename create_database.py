from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma
from dotenv import load_dotenv
import os
import shutil

# Load the environment variables
load_dotenv() 

# Define the paths
CHROMA_PATH = "chroma"
DATA_PATH = "data/"


def main():
    generate_data_store()


def generate_data_store():
    documents = load_and_process_pdfs()
    chunks = split_text(documents)
    save_to_chroma(chunks)

def load_and_process_pdfs():
    all_pages = []
    for filename in os.listdir(DATA_PATH):
        if filename.endswith(".pdf"):
            file_path = os.path.join(DATA_PATH, filename)
            loader = PyPDFLoader(file_path)
            pages = loader.load_and_split()
            all_pages.extend(pages)
            print(f"Processed {len(pages)} pages from {filename}")
    return all_pages


def split_text(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=200,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    document = chunks[10]
    print(document.page_content)
    print(document.metadata)

    return chunks

# Creating vector store
def save_to_chroma(chunks):
    # Clear out the database first.
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
    # Create a new DB from the documents.
    db = Chroma.from_documents(
        chunks, OpenAIEmbeddings(), persist_directory=CHROMA_PATH
    )
    db.persist()
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")


if __name__ == "__main__":
    main()