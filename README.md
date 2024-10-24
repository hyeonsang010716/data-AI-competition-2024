# 국회 회의록 기반 RAG 시스템 채팅 서비스

이 프로젝트는 RAG (Retrieval-Augmented Generation) 시스템을 이용하여 국회 회의록 데이터를 기반으로 질의응답 채팅 서비스를 제공합니다. 사용자는 Streamlit을 통해 웹에서 직접 국회 회의록 데이터에 대한 질문을 하고, AI가 해당 내용을 기반으로 답변을 제공합니다.

## 주요 기능

- **국회 회의록 데이터 질의응답**: 국회 회의록 데이터를 기반으로 자연어 질문에 대한 답변을 생성합니다.
- **RAG 기반 검색**: 문서 검색 및 답변 생성에 RAG 시스템을 사용하여 높은 정확도를 제공합니다.
- **Streamlit UI**: 사용자 친화적인 Streamlit 인터페이스로 쉽게 접근할 수 있는 채팅 서비스입니다.

## 설치 방법

로컬 환경에서 프로젝트를 실행하려면 다음 단계를 따르세요:

1. **레포지토리 클론**:
   ```bash
   git clone https://github.com/your-username/repo-name.git
   cd repo-name

2. 필요한 패키지 설치
    ```bash
    pip install -r requirements.txt

3. .env 파일 설정
    ```
    OPENAI_API_KEY=your_api_key="your_api_key"

4. Streamlit 실행
    ```bash
    streamlit run __main__.py

## 사용 방법
    1. 터미널에서 streamlit run app.py를 실행하여 웹 애플리케이션을 시작합니다.
    2. 웹 브라우저에서 열리는 채팅 화면에서 질문을 입력하세요.
    3. AI가 국회 회의록 데이터를 검색하고 적절한 답변을 제공합니다.

    예시 질문: 신도시의 평준화 교육 정책 결정 시 학부모의 의견을 어떻게 고려할 계획인가요?
    
    a.  신도시의 평준화 교육 정책 결정 시 학부모의 의견은 신빙성 있는 조사를 통해 고려될 예정입니다.
        교육청은 평준화 정책에 대한 조사 결과와 학부모의 의견을 종합하여 내년 초에 정책을 결정할 계획입니다.
        요약하자면, 신도시 평준화 교육 정책은 학부모의 의견을 반영하여 신중하게 결정될 예정입니다. 
        혹시 더 궁금한 부분이 있으면 물어보세요.

## 프로젝트 구조
-  _ main__.py : streamlit을 사용한 웹 어플리케이션 메인 파일입니다.
- assets : 국회 회의록 데이터를 가공하여 만든 total.txt 등의 데이터가 있는 디렉터리입니다.
- RAG : Rag 시스템 구축을 위한 prompt, history, retriever 등이 담겨 있는 모듈화된 디렉토리 입니다.
- Data_preprocessing : 데이터 전처리를 처리하는 코드들이 담겨있는 디렉토리 입니다.
- Vector_DB, SQLite_DB : vector, sql 등 Database를 생성하고 관리하는 함수들이 담겨있습니다.
