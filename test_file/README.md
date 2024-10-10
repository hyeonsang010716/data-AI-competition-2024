## test 사용방법

1. ragas 설치 (최신 버전 설치를 위해서 사용)
   `pip install git+https://github.com/explodinggradients/ragas.git`
   1-1. 충돌 일어나면
   `pip install --upgrade pydantic streamlit pyarrow datasets`
2. 이후 make_testset에서 직접 테스트 셋을 만들거나 다운로드 하기
3. streamlit으로 test.py 실행(main과 동일)
4. 이후 terminal에 각 점수가 생성됨
   ㄴ 보기 쉽게 나중에 계산할 예정
   ㄴ 각 점수는 아래 코드(test_data.py)에서 metrics를 ragas reference 통해서 변경하면 됨

```
result = evaluate(
        dataset = dataset,
        metrics=[
            context_precision,
            context_recall,
            faithfulness,
            answer_relevancy,
        ],
)
```
