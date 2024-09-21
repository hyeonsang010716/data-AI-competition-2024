from langchain_community.document_loaders import DirectoryLoader
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
import os
from dotenv import load_dotenv

load_dotenv()

def create_index():
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    directory_path = "./Vector_DB/chroma_db"
    if os.path.exists(directory_path):
        print("존재하는 임베딩 세팅")
        vectorstore = Chroma(
            embedding_function=embeddings, persist_directory=directory_path
        )
        return vectorstore
    else:
        print("새로운 임베딩 세팅")
        doc_loader = DirectoryLoader(".", glob="./assets/*.txt")
        documents = doc_loader.load()
        db = Chroma.from_documents(
            documents=documents,
            embedding=embeddings,
            persist_directory=directory_path,
            collection_name="my_db",
        )
        return db
