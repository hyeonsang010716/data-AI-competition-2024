from langchain_openai import AzureChatOpenAI , ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain.tools.retriever import create_retriever_tool
from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor
from Vector_DB.create_db import create_index
from RAG.prompts import sys_prompt
from RAG.history import create_with_message_history
class Agent:
    def __init__(self):
        self.store = {}
        self.tool = self.__tool_init()
        self.agent = self.__agent_init()

    def __tool_init(self):
        vector_store , documents = create_index()
        retriever = vector_store.as_retriever(
            search_type="mmr",
            search_kwargs={"k": 5},
        )
        #model = AzureChatOpenAI(
        #    model="gpt-4o",
        #    temperature=0.3,
        #)
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
        
        bm25_retriever = BM25Retriever.from_texts(
            [doc.page_content for doc in documents]
        )
        
        ensemble_retriever = EnsembleRetriever(
            retrievers=[bm25_retriever, multiquery_retriever],
            weights=[0.6, 0.4],
        )  
        tool = create_retriever_tool(
            ensemble_retriever,
            "Internal_Knowledge_Retriever",
            "Retrieval and Augmented Generation for MBC+ guide",
        )

        return [tool]

    def __agent_init(self):
        #model = AzureChatOpenAI(
        #    model="gpt-4o",
        #    temperature=0.3,
        #)
        model = ChatOpenAI(
            model="gpt-4o",
            temperature=0.3,
        )
        prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", sys_prompt),
                MessagesPlaceholder(variable_name="history"),
                ("human", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )
        agent = create_tool_calling_agent(llm=model, tools=self.tool, prompt=prompt_template)
        agent_executor = AgentExecutor(
            agent=agent, tools=self.tool, verbose=True, max_iterations=10
        )
        return create_with_message_history(agent_executor)
    
    def get_agent(self):
        return self.agent