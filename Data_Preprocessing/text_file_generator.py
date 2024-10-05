import os
import json
import sys
def load_json(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)  # 전체 내용
    except FileNotFoundError:
        data = "파일을 찾을 수 없습니다."
    except json.JSONDecodeError:
        data = "유효하지 않은 JSON 형식입니다."
    return data


current_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_dir, "data")
current_dir = os.path.dirname(current_dir) 
assets_path = os.path.join(current_dir, "assets")

text = ""
for root, dirs, files in os.walk(data_path):
    for file in files:
        if file.endswith(".json"):
            file_path = os.path.join(root, file)
            data = load_json(file_path)
            text += (data['context_summary']["summary_q"] + "\n")
            text += data['context_summary']["summary_a"]
            text += "\n\n\n"


name = "total_text"
assets_file_path = os.path.join(assets_path, name + '.txt')
with open(assets_file_path, "a") as txt_file:
    txt_file.write(text)

