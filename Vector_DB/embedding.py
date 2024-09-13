# DB 경로를 받고 접근해서 임베딩 후 키워드와 유사한 값 리스트로 리턴
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


model = SentenceTransformer('paraphrase-MiniLM-L6-v2') # Sentence-BERT 모델 로드

def get_embedding(questions):# 질문 전부를 임베딩하기
    qustion_vectors = model.encode(questions)

    # 질문 벡터의 차원 확인
    vector_dimension = len(qustion_vectors[0])
    #Faiss index 생성
    index = faiss.IndexFlatL2(vector_dimension)
    # 인덱스에 벡터 추가
    index.add(np.array(qustion_vectors).astype('float32'))

    return index


def search_qa(query, index, k=5):
    # 질문(query)를 vector로 변환
    query_vector = model.encode([query])

    # distances는 query와 가장 가까운 값의 유사도
    # indices는 query와 가장 가까운 값의 인덱스 값
    distances, indices = index.search(np.array(query_vector).astype('float32'), k)
    return indices


if __name__ == "__main__":
    results = search_qa('그러니까 내가 아까 얘기한 부산지검의 명예를 회복하기 위해서 해야 된다는 얘기이고 그 이전의 지검 검사장도 이 지역사회에서 유착되었다는 설도 여기에서는 널리 유포되어 있었습니다. 그런데다가 최근에 두 지검 검사장이 이 사건의 변호인으로 선임되고 하니까 점점 부산지검은 다대ㆍ만덕사건에 관한 한 처음부터 수사를 못 하게 되어 있는 사건이다, 내가 아까 말한 대로 국정감사 때마다 요구하고 추궁하고 또 감사원 감사가 착수되고 하니까 할 수 없이 등 떠밀려서 마지못해서 하는 것 아니냐 하는 것입니다.  수사진은 왜 교체했습니까?')

    print(f"question: {results[0][0]}")
    print(f"answer: {results[0][1]}")
    print(f"distance: {results[0][2]}") # 쿼리 벡터와 찾은 질문 벡터 사이의 거리 (유사도)