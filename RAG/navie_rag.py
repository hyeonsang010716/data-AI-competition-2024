import pandas as pd
from dotenv import load_dotenv
import os
from langchain_openai import AzureChatOpenAI
from langchain_openai import AzureOpenAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores.faiss import FAISS
import sqlite3
load_dotenv()
base_dir = os.path.dirname(os.path.abspath(__file__))
vector_store_path = os.path.join(base_dir, 'vector_store')
api_key = os.getenv('API')
endpoint = os.getenv('endpoint')

# getDB data
def get_db_data():
    path = os.path.join(base_dir, 'database1.db')
    conn = sqlite3.connect(path)
    query = "select keyword, comment from database1"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

df = get_db_data()
df['combined'] = df[['keyword', 'comment']].apply(lambda x: '&&'.join(x.astype(str)), axis=1)
#print(df['comment'][0])

embedding = AzureOpenAIEmbeddings(
    api_key = api_key,  
    api_version = "2024-02-01",  
    model="text-embedding-3-small",
    azure_endpoint = endpoint
)

texts = df['combined'].tolist()
vector_store = FAISS.from_texts(texts, embedding)

query ="산업재해가 해마다 증가하고 있는 이유가 뭐야? : \n\n"

results = vector_store.similarity_search(query, k=5)

for result in results:
    keyword , content = result.page_content.split("&&")
    query += "keyword :"+ keyword + "\n"
    query += "content :" + content + "\n\n"

prompt = PromptTemplate(
    template="너는 국회 회의록 기반 의정활동 지원 및 대국민 알권리 보장 챗봇 서비스 도우미야. 국정검사에 관한 내용은 다음을 참조합니다. {input_text}",
    input_variables=['input_text']
)

model = AzureChatOpenAI(
        azure_deployment="gpt-4o",
        azure_endpoint = endpoint,
        api_key = api_key,
        api_version = "2024-02-01",
        temperature=0.2,
    )

chain = prompt | model

response = chain.invoke(query)
print(response.content)



