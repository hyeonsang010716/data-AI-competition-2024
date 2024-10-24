from RAG.retriever import Agent
import streamlit as st
import time
from dotenv import load_dotenv
load_dotenv()
# llm 인스턴스를 세션 상태에 저장하고 재사용
if "llm" not in st.session_state:
    agent = Agent()
    st.session_state.llm = agent.get_agent()  # llm 인스턴스 저장

llm = st.session_state.llm

# 대답 방식
def response_generator(response):
    for word in response.split("\n"):
        print(word)
        yield word + "\n"
        time.sleep(0.05)


# 채팅 서비스 이름 설정
st.title("국회 회의록 챗봇")

# 채팅 기록 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# # 새로 고침 시 이전에 있던 채팅 기록 가져오기
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 유저 입력 = 변수 prompt
if prompt := st.chat_input("What is up?"):
    # 유저 메시지 기록에 추가
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 유저 메시지를 보여주기
    with st.chat_message("user"): # user가 보낸 응답이라는 의미
        st.write(prompt)

    session_id = "user_unique_session_id"

    answer = llm.invoke({"input" : prompt}, config={"configurable": {"session_id": session_id}})["output"]
    print(answer)

    # 메시지 기록에 담을 답변 내용을 생성
    assistant_response = ""
    with st.chat_message("assistant"):
        for word in response_generator(answer):
            st.write(word)
            assistant_response += word  # 각 단어를 차례대로 모아 답변 생성

    # 메시지 기록에 담기
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})