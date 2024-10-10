from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# 세션 기록을 저장할 딕셔너리
store = {}

# 세션 ID를 기반으로 세션 기록을 가져오는 함수
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# 세션 기반 히스토리를 관리하는 RunnableWithMessageHistory 객체를 생성하는 함수
def create_with_message_history(agent_executor, input_key="input", history_key="history"):
    return RunnableWithMessageHistory(
        agent_executor,
        get_session_history,
        input_messages_key=input_key,
        history_messages_key=history_key,
    )