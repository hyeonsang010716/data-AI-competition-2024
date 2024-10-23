
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
import os
import pickle
from langchain.schema import Document

def save_documents(documents, file_path):
    with open(file_path, "wb") as file:
        pickle.dump(documents, file)

def load_documents(file_path):
    with open(file_path, "rb") as file:
        return pickle.load(file)
    
def load_learning_materials():
    learning_materials = ""
    base_path = "./assets"

    # TXT 파일 읽기
    txt_files = [f for f in os.listdir(base_path) if f.endswith(".txt")]
    for txt_file in txt_files:
        file_path = os.path.join(base_path, txt_file)
        if os.path.exists(file_path):
            with open(file_path, encoding="utf-8") as file:
                learning_materials += file.read() + "\n\n\n"
    return learning_materials

def create_index():
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large") # 임베딩 모델
    
    directory_path = "./Vector_DB/chromadb"
    if os.path.exists(directory_path):
        print("존재하는 임베딩 세팅")
        db = Chroma(
            embedding_function=embeddings, persist_directory=directory_path
        )
        recursive_splitted_document = load_documents("./assets/recursive_splitted_document.pkl")
        return db , recursive_splitted_document
    else:
        print("새로운 임베딩 세팅")
        learning_materials = load_learning_materials()
        texts = learning_materials.split("\n\n\n")
        # texts 리스트를 Document 객체로 변환
        documents = [Document(page_content=text) for text in texts]    

        save_documents(documents, "./assets/recursive_splitted_document.pkl")
        # 파일에 저장
        with open('chunk.txt', 'w', encoding='utf-8') as f:
            for i, chunk in enumerate(texts):
                f.write(f"Chunk {i+1}:\n")
                f.write(chunk + "\n")
                f.write("-" * 50 + "\n")

        db = Chroma.from_texts(
            texts=texts,
            embedding=embeddings,
            persist_directory=directory_path,
        )
        return db , documents


