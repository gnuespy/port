import streamlit as st
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# 임베딩 모델 로드
encoder = SentenceTransformer('jhgan/ko-sroberta-multitask')

# 식당 관련 질문과 답변 데이터
questions = [
    "포트폴리오 주제가 무엇인가요?",
    "사용한 모델은 무엇인가요?",
    "프로젝트 인원은 어떻게 되나요??",
    "프로젝트 기간은 어떻게 되나요?",
    "맡은 역할은 무엇인가요?",
    "사용 데이터는 무엇이가요?",
    "프로젝트에서의 어려움이 있었니요?"
]

answers = [
    "YOLO를 이용한 유동인구 측정 프로그램입니다.",
    "YOLO 8버전을 사용했습니다.",
    "4명입니다.",
    "기획, 구현, 발표까지 총 3주 소요되었습니다.",
    "디비연동 및 홈페이지 구현입니다.",
    "직접 생성했습니다.",
    "학습이 어려웠습니다."
]

# 질문 임베딩과 답변 데이터프레임 생성
question_embeddings = encoder.encode(questions)
df = pd.DataFrame({'question': questions, '챗봇': answers, 'embedding': list(question_embeddings)})

# 대화 이력을 저장하기 위한 Streamlit 상태 설정
if 'history' not in st.session_state:
    st.session_state.history = []

# 챗봇 함수 정의
def get_response(user_input):
    # 사용자 입력 임베딩
    embedding = encoder.encode(user_input)
    
    # 유사도 계산하여 가장 유사한 응답 찾기
    df['distance'] = df['embedding'].map(lambda x: cosine_similarity([embedding], [x]).squeeze())
    answer = df.loc[df['distance'].idxmax()]

    # 대화 이력에 추가
    st.session_state.history.append({"user": user_input, "bot": answer['챗봇']})

# Streamlit 인터페이스
st.title("영화 추천 챗봇")
st.write("제가 만든 포트폴리오에 대해 질문 해주세요. 예: 주제가 무엇인가요?")

user_input = st.text_input("user", "")

if st.button("Submit"):
    if user_input:
        get_response(user_input)
        user_input = ""  # 입력 초기화

# 대화 이력 표시
for message in st.session_state.history:
    st.write(f"**사용자**: {message['user']}")
    st.write(f"**챗봇**: {message['bot']}")