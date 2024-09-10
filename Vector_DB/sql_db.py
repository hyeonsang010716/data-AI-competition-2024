# DB 생성 (경로는 main에서 전달 받음)
import os
import sqlite3
import json


def load_json(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file) # 전체 내용
    except FileNotFoundError:
        data = "파일을 찾을 수 없습니다."
    except json.JSONDecodeError:
        data = "유효하지 않은 JSON 형식입니다."
    return data


def read_json_files(directory):
    question = []
    answer = []
    # 디렉토리와 하위 디렉토리를 탐색
    for root, dirs, files in os.walk(directory):
        for file in files:
            # 파일 확장자가 .json인지 확인
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                # JSON 파일 읽기
                data = load_json(file_path)
                # json파일에서 question / answer 쌍으로 추출
                question.append(data['question']["comment"])
                answer.append(data['answer']["comment"])
                
    return question, answer


def create_db(path):
    # 데이터베이스 연결 (이 객체를 이용해서 데이터베이스 접근이 가능)
    conn = sqlite3.connect(path)
    # 커서 생성 (커서는 DB 명령어를 사용할 때 필요)
    cursor = conn.cursor()

    # 테이블 생성 
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS qa_pairs(
            id INTEGER PRIMARY KEY,
            question TEXT NOT NULL,
            answer TEXT NOT NULL
        )
    ''')
    return conn


def insert_data(conn, questions, answers):
    if len(questions) != len(answers):
        print("warnning")
        return 
    
    cursor = conn.cursor()

    for q, a in zip(questions, answers):  # 질문과 답변을 쌍으로 해서 추가
        cursor.execute("INSERT INTO qa_pairs (question, answer) VALUES (?, ?)", (q, a))


def get_db_data(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT question, answer FROM qa_pairs")

    # qa_pairs = cursor.fetchall() 전체 데이터가 적으면 더 빠른 방법

    # for row in cursor: # 데이터가 양이 많으면 직접 처리하는 게 메모리 효율이 좋음
    #     question, answer = row # 각 행 처리


if __name__ == "__main__":
    # 경로 설정
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root = os.path.dirname(current_dir)
    dir_path = os.path.join(root, "data", "Sample", "02.라벨링데이터", "국정감사", "16")  #원하는 경로 (일단 한정해 두었음)
    db_path = os.path.join(root, "data", "qa_database.db") # 경로를 어디에 놓을까? (일단 data 모으는 곳에 두긴 했어)

    questions, answers = read_json_files(dir_path) # 각각 질문 답변 데이터 수집

    db = create_db(db_path)
    insert_data(db, questions, answers)
    get_db_data(db)
