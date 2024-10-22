## 각 임베딩 모델 평가 및 지표 확인
사용된 모듈은 ragas이며 faithfulness와 answer_relevancy를 사용하였습니다.
> faithfulness
> - 생성된 답변이 얼마나 사실(Context)에 근거한 정확한 답변인가요?
> - answer와 context에서 계산됩니다. Faithfullness 측정값은 값은 (0,1) 범위로 스케일링 되며 높을수록 좋습니다.

> answer_relevancy
> - 생성된 답변이 질문(공식문서: 주어진 프롬프트)에 얼마나 관련성이 있나요?
> - 이 지표는 `question`, `answer` , `context` 사용하여 계산됩니다 .
> - 불완전하거나 중복된 정보를 포함하는 답변에는 낮은 점수가 부여되고, 높은 점수는 더 나은 관련성을 나타냅니다.

|임베딩 모델|faithfulness|answer_relevancy|
|------|---|---|
|text-embedding-3-small|0.5871|0.4452|
|intfloat/multilingual-e5-large-instruct|0.5865|0.5619|
|solar-embedding-1-large-passage|0.5839|0.3795|
|nomic-embed-text|0.6729|0.431|
|BAAI/bge-m3|0.5863|0.4152|
|BM-K/KoSimCSE-roberta-multitask|0.7569|0.43|
|intfloat/multilingual-e5-large|0.6721|0.2518|
|snunlp/KR-SBERT-V40K-klueNLI-augSTS|0.6737|0.5728|
|gpt4all Embedding|0.6743|0.3225|
