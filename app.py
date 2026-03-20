import streamlit as st
from PIL import Image
import pytesseract
from gtts import gTTS
import io

st.set_page_config(page_title="엄마 목소리 동화책", page_icon="📚")

st.title("📚 우리 엄마 동화책 읽어주기")
st.write("사진을 여러 장 올리면 순서대로 읽어드려요.")

# 1. 파일 업로드 (여러 장 선택 가능)
uploaded_files = st.file_uploader("동화책 페이지 사진들을 선택하세요", 
                                  type=['png', 'jpg', 'jpeg'], 
                                  accept_multiple_files=True)

if uploaded_files:
    # 파일 이름순으로 정렬 (1.jpg, 2.jpg 등 순서 보장)
    uploaded_files.sort(key=lambda x: x.name)
    
    full_text = ""
    
    for i, file in enumerate(uploaded_files):
        img = Image.open(file)
        st.image(img, caption=f"{i+1}번 페이지", width=200)
        
        # OCR 처리
        with st.spinner(f'{i+1}번 페이지 글자 읽는 중...'):
            text = pytesseract.image_to_string(img, lang='kor')
            st.info(f"**{i+1}번 내용:** {text[:50]}...") # 앞부분만 살짝 표시
            full_text += text + " "

    # 2. 통합 음성 생성
    if st.button("전체 페이지 순서대로 듣기"):
        if full_text.strip():
            with st.spinner('엄마 목소리(AI)로 변환 중...'):
                tts = gTTS(text=full_text, lang='ko')
                audio_fp = io.BytesIO()
                tts.write_to_fp(audio_fp)
                st.audio(audio_fp, format='audio/mp3')
        else:
            st.error("사진에서 글자를 찾지 못했어요.")
