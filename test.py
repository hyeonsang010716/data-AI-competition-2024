from RAG.ensemble_retriever import Agent
import streamlit as st
import time
import pandas as pd 
from dotenv import load_dotenv
from test_file.test_data import get_test
import os

load_dotenv()

current_dir = os.path.dirname(os.path.abspath(__file__))
assets_path = os.path.join(current_dir, "assets")
name = "qa_pairs"

df = pd.read_csv(os.path.join(assets_path, name+".csv"))
questions = df["Question"]
answers = []

# llm 인스턴스를 세션 상태에 저장하고 재사용
if "llm" not in st.session_state:
    agent = Agent()
    st.session_state.llm = agent.get_agent()  # llm 인스턴스 저장

llm = st.session_state.llm

# 대답 방식
def response_generator(response):
    for word in response.split():
        yield word + " "
        time.sleep(0.05)


# 채팅 서비스 이름 설정
st.title("Simple chat")

# 채팅 기록 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# # 새로 고침 시 이전에 있던 채팅 기록 가져오기
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 유저 입력 = 변수 prompt
for prompt in questions:
    # 유저 메시지 기록에 추가
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 유저 메시지를 보여주기
    with st.chat_message("user"): # user가 보낸 응답이라는 의미
        st.write(prompt)

    answer = llm.invoke({"input" : prompt})["output"]
    answers.append(answer)

    with st.chat_message("assistant"):
        response = st.write_stream(response_generator(answer))
    
    # 메시지 기록에 담기
    st.session_state.messages.append({"role": "assistant", "content": response})

print(get_test(answers))
    
    