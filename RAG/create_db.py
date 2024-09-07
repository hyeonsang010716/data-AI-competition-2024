from dotenv import load_dotenv
import os
import json
import sqlite3

load_dotenv()
base_dir = os.path.dirname(os.path.abspath(__file__))
api_key = os.getenv('data_API')

def read_dir():
    # 디렉토리 안의 항목 리스트 가져오기
    dirs = []
    directory_path = os.path.join(base_dir, '../data')
    try:
        items = os.listdir(directory_path)
        for item in items:
            item_path = os.path.join(directory_path, item)
            if os.path.isdir(item_path):
                dirs.append(item_path)
                print(f"Directory: {item_path}")
                return dirs
    except FileNotFoundError:
        print(f"The directory {directory_path} does not exist.")
    except PermissionError:
        print(f"You do not have permission to access the directory {directory_path}.")

    return dirs

def read_file(dirs):
    files = []
    # 디렉토리 안의 파일 리스트 가져오기
    try:
        for dir_path in dirs:
            items = os.listdir(dir_path)
            for item in items:
                item_path = os.path.join(dir_path, item)
                file_dirs = os.listdir(item_path)
                for file in file_dirs:
                    file_path = os.path.join(item_path, file)
                    if os.path.isfile(file_path):
                        files.append(file_path)
                        print(f"Directory: {file_path}")
                return files
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
    except PermissionError:
        print(f"You do not have permission to access the file {file_path}.")
    return files

def create_db():
    
    path = os.path.join(base_dir, 'database1.db')
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS database1 (
            id INTEGER PRIMARY KEY,
            keyword TEXT,
            comment TEXT
        )
    ''')
    conn.commit()
    return conn

def insert_data(conn, data):
    key1 = set(data['question']['keyword'].split(","))
    key2 = set(data['answer']['keyword'].split(","))
    temp = set()
    for x in key1:
        temp.add(x.strip())
    for x in key1:
        temp.add(x.strip())
    keyword = ",".join(list(temp))
    print(keyword)
    cursor = conn.cursor()
    cursor.execute('''
    SELECT * FROM database1 WHERE keyword=? AND comment=?
    ''', (keyword, data['answer']['comment']))
    
    if cursor.fetchone() is None:
        cursor.execute('''
            INSERT INTO database1 (keyword, comment)
            VALUES (?, ?)
        ''', (keyword, data['answer']['comment']))
        conn.commit()


dirs = read_dir()
files = read_file(dirs)

db = create_db()



# JSON 파일 읽기
try:
    for file in files:
        with open(file, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)  # JSON 데이터를 파이썬 딕셔너리로 로드
            insert_data(db , data)
except FileNotFoundError:
    print(f"The file {file} does not exist.")
except json.JSONDecodeError:
    print(f"The file {file} is not a valid JSON file.")
except PermissionError:
    print(f"You do not have permission to access the file {file}.")


