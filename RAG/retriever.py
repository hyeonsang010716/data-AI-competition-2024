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
            search_kwargs={"k": 4},
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
        """
        You are an AI language model assistant.
        Your task is to generate three different rephrased versions of the given user question in order to retrieve relevant documents from a vector database.
        The goal is to create multiple variations of the original question that capture different aspects or interpretations, while ensuring that all variations stay grounded in the potential contents of the retrieved documents.

        When rephrasing the question:
        - Focus on different angles or possible interpretations, but make sure to avoid introducing information or assumptions not present in the original question.
        - The variations should aim to retrieve relevant documents without speculation, ensuring that the document content can directly support the query.
        - Avoid repetition and ensure each rephrased version explores different possible aspects of the question.

        ## Few-shot examples:

        ### Example 1:
        ORIGINAL QUESTION: "KBS 예산 지원에 대한 논의가 있나요?"
        Rephrased:
        1. "KBS 예산 지원과 관련된 세부 논의가 있었나요?"
        2. "KBS에 예산 지원이 이루어진 사례가 있나요?"
        3. "KBS에 특별 예산 지원이 논의된 적이 있나요?"

        ### Example 2:
        ORIGINAL QUESTION: "최근 국회에서 환경 규제와 관련된 법안이 논의된 적이 있나요?"
        Rephrased:
        1. "최근 환경 규제에 관한 법안이 국회에서 논의되었나요?"
        2. "환경 관련 규제 법안이 최근 국회에서 다루어진 사례가 있나요?"
        3. "국회에서 최근 환경 규제에 대해 논의한 법안이 있나요?"

        ### Example 3:
        ORIGINAL QUESTION: "국회의원이 제안한 교통 관련 법안이 통과된 사례가 있나요?"
        Rephrased:
        1. "교통 법안이 국회에서 논의되고 통과된 적이 있나요?"
        2. "교통과 관련된 국회의원 제안 법안이 국회를 통과한 적이 있나요?"
        3. "교통 관련 법안이 국회의원의 제안으로 통과된 사례가 있나요?"

        ### Example 4:
        ORIGINAL QUESTION: "정부의 재정 지원이 포함된 법안이 최근 논의된 적이 있나요?"
        Rephrased:
        1. "정부 재정 지원 법안이 최근 국회에서 논의되었나요?"
        2. "정부가 재정 지원을 포함한 법안이 최근 국회에서 다뤄진 적이 있나요?"
        3. "최근 국회에서 논의된 법안 중 정부 재정 지원을 포함한 사례가 있나요?"

        ### Example 5:
        ORIGINAL QUESTION: "농업 지원과 관련된 법안이 최근에 통과되었나요?"
        Rephrased:
        1. "농업 지원 법안이 최근 국회를 통과한 적이 있나요?"
        2. "최근 농업 지원 법안이 국회에서 통과되었나요?"
        3. "국회에서 농업 지원과 관련된 법안이 최근 통과된 사례가 있나요?"

        ## Now, generate three rephrased versions of the following question:

        # ORIGINAL QUESTION:
        {question}

        # Answer in Korean:
        
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