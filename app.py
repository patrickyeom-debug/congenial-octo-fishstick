import streamlit as st
from PIL import Image
import pytesseract
from gtts import gTTS
import io

st.set_page_config(page_title="엄마 목소리 동화책", page_icon="📚")

st.title("📚 우리 엄마 동화책 읽어주기")
st.write("사진을 여러 장 올리면 순서대로 읽어드려요.")

uploaded_files = st.file_uploader("동화책 페이지 사진들을 선택하세요", 
                                  type=['png', 'jpg', 'jpeg'], 
                                  accept_multiple_files=True)

if uploaded_files:
    uploaded_files.sort(key=lambda x: x.name)
    full_text = ""
    
    for i, file in enumerate(uploaded_files):
        img = Image.open(file)
        st.image(img, caption=f"{i+1}번 페이지", width=300)
        
        with st.spinner(f'{i+1}번 페이지 글자 읽는 중...'):
            # 한국어(kor) 설정을 명시적으로 한 번 더 확인
            text = pytesseract.image_to_string(img, lang='kor')
            st.info(f"**{i+1}번 내용:**\n\n{text}")
            full_text += text + " "

    if st.button("전체 페이지 순서대로 듣기"):
        if full_text.strip():
            with st.spinner('목소리 생성 중...'):
                tts = gTTS(text=full_text, lang='ko')
                audio_fp = io.BytesIO()
                tts.write_to_fp(audio_fp)
                
                # 핵심 수정 부분: 파일의 시작점으로 이동해야 재생이 됩니다!
                audio_fp.seek(0) 
                
                st.audio(audio_fp, format='audio/mp3')
        else:
            st.error("사진에서 글자를 찾지 못했어요.")