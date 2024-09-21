from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_core.runnables import RunnablePassthrough
from Vector_DB.create_db import create_index
from dotenv import load_dotenv
import json

load_dotenv()


def multi_query_chain(query: str) -> str:
    vector_store = create_index()
    retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 5},
    )
    model = ChatOpenAI(
        model="gpt-4o",
        temperature=0.3,
    )

    multi_query_prompt = PromptTemplate.from_template(
        """You are an AI language model assistant. 
    Your task is to generate three different versions of the given user question to retrieve relevant documents from a vector database. 
    By generating multiple perspectives on the user question, your goal is to help the user overcome some of the limitations of the distance-based similarity search. 
    Your response should be a list of values separated by new lines, eg: `foo\nbar\nbaz\n`

    #ORIGINAL QUESTION: 
    {question}

    #Answer in Korean:
    """
    )

    custom_multiquery_chain = (
        {"question": RunnablePassthrough()}
        | multi_query_prompt
        | model
        | StrOutputParser()
    )
    multiquery_retriever = MultiQueryRetriever.from_llm(
        retriever=retriever,
        llm=custom_multiquery_chain,
    )

    prompt = PromptTemplate.from_template(
        """You are an assistant for question-answering tasks. 
        Use the following pieces of retrieved context to answer the question. 
        If you don't know the answer, just say that you don't know. 
        Answer in Korean.

        #Question: 
        {question} 
        #Context: 
        {context} 

        #Answer:"""
    )
    # 단계 8: 체인(Chain) 생성
    chain = (
        {"context": multiquery_retriever, "question": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )
    output = chain.invoke(query)
    return output
