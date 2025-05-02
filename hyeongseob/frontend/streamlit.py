# default
FASTAPI_URL = "http://127.0.0.1:8000"
audio_extraction_api_url = "http://localhost:8000//audio/extraction"
text_conversion_api_url = "http://localhost:8000/stt/conversion"
text_summary_api_url = "http://localhost:8000/tt/summary"

import streamlit as st
import requests

# 배경색 변경 (CSS 적용)
st.markdown(
    """
    <style>
    .main {
        background-color: #004e89;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 100vh;
    }
    .custom-container {
        text-align: center;
        background-color: transparent;
        padding: 50px;
        border-radius: 10px;
    }
    .custom-button {
        background-color: #ffd700;
        color: #004e89;
        font-size: 20px;
        padding: 15px 30px;
        border-radius: 10px;
        text-align: center;
        display: inline-block;
        border: none;
        cursor: pointer;
        font-weight: bold;
    }
    .custom-button:hover {
        background-color: #e6c200;
    }
    .input-box input {
        font-size: 18px !important;
        padding: 15px !important;
        height: 50px !important;
        width: 100% !important;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="custom-container">', unsafe_allow_html=True)

# 제목
st.markdown("<h1 style='text-align: center; color: #ffd700;'>🤑경제 유튜브, 핵심만 보자!</h1>", unsafe_allow_html=True)

# user's input()
st.header("🎥 Video URL 입력")
video_url = st.text_input("링크 입력", label_visibility="collapsed", placeholder="🔗 링크를 입력하세요 - 유튜브, 팟캐스트", key="big_textbox")
data = {"url": video_url}

# button size detail
col1, col2, col3 = st.columns([1, 2, 1])

# frontend audio extraction logic
if st.button("😉영상 요약하기", use_container_width=True):
    if not video_url:
        st.warning("URL이 아닙니다. URL을 입력해주세요", icon="⚠️")
    else:
        with st.spinner("내용 확인 중...⏳ 잠시만 기다려주세요"):
            try:
                response = requests.post(audio_extraction_api_url, json=data)
                st.subheader("동영상")
                st.video(video_url)

            except Exception as e:
                st.error(f"오류 발생: {e}")

    st.spinner("오디오를 텍스트로 변환 중...⏳ 잠시만 기다려주세요")
    response = requests.post(text_conversion_api_url)
    conversion_text = response.json()["conversion_text"]
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander(label="😎오디오 추출 텍스트 원문", expanded=False):
        st.markdown(conversion_text, unsafe_allow_html=True)


    st.spinner("변환된 텍스트 내용 정리중...⏳ 잠시만 기다려주세요")
    response = requests.post(text_summary_api_url)
    summary_text = response.json()["summary"]
    with st.expander(label="🤞영상 내용 요약 전문", expanded=True):
        st.markdown(summary_text, unsafe_allow_html=True)