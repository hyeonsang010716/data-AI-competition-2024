# pip install git+https://github.com/explodinggradients/ragas.git
import pandas as pd 
import os
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_recall,
    context_precision,
)

current_dir = os.path.dirname(os.path.abspath(__file__))
current_dir = os.path.dirname(current_dir) 
assets_path = os.path.join(current_dir, "assets")
name = "qa_pairs"

def get_test(answers):
    df = pd.read_csv(os.path.join(assets_path, name+".csv"))

    questions = list(df["Question"])
    contexts = []
    for text in df["Text Reference"]:
        contexts.append([text])
    ground_truths = list(df["Answer"])

    data = {
        "question": questions,
        "answer": answers,
        "contexts": contexts,
        "ground_truth": ground_truths
    }
    

    dataset = Dataset.from_dict(data)

    result = evaluate(
        dataset = dataset, 
        metrics=[
            context_precision,
            context_recall,
            faithfulness,
            answer_relevancy,
        ],
    )

    # score 출력
    print(result)
    # DataFrame 생성
    df = result.to_pandas()
    return df