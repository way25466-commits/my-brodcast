import streamlit as st
from gtts import gTTS
import io

st.set_page_config(page_title="스마트 방송국", page_icon="📢", layout="centered")
st.title("📢 모바일 스마트 방송 시스템")
st.caption("무료 여성 아나운서 목소리와 3단계 속도 제어가 가능한 방송 시스템입니다.")

# Google Actions 무료 차임벨 주소
CHIME_URL = "https://google.com" 

broadcast_text = st.text_area(
    "💬 방송 안내문을 입력하세요:", 
    value="주민 여러분 안녕하십니까. 관리사무소에서 안내 말씀 드립니다. 잠시 후 오전 10시부터 단지 내 물탱크 청소로 인해 단수가 예정되어 있습니다. 주민 여러분께서는 미리 생활용수를 확보하시어 불편이 없으시길 바랍니다. 감사합니다.",
    height=200
)

# 1. 목소리 선택 (무료 버전은 여성 기본 제공)
st.selectbox("👤 방송 목소리 선택", ["여성 아나운서 톤 (기본 무료)"], disabled=True)

# 2. 요청하신 3단계 속도 조절 메뉴
speed_option = st.radio("🏃‍♂️ 방송 속도 조절", ["매우 느리게", "보통", "매우 빠르게"], index=1)
include_chime = st.checkbox("🔔 방송 시작 전 차임벨(시작음) 먼저 재생하기", value=True)

if st.button("🚀 방송 MP3 파일 만들기", use_container_width=True):
    if not broadcast_text.strip():
        st.error("방송 내용을 입력해 주세요!")
    else:
        with st.spinner("⏳ 요청하신 속도로 여성 목소리 방송 생성 중..."):
            try:
                processing_text = broadcast_text.strip()
                slow_mode = False
                
                # 3단계 속도 가공 기술 적용
                if speed_option == "매우 느리게":
                    slow_mode = True  # 구글 엔진의 느린 모드 작동
                    # 글자 사이사이에 공백을 넓혀서 더 느리게 들리도록 텍스트 변환
                    processing_text = " ".join(list(processing_text.replace(" ", "  ")))
                elif speed_option == "매우 빠르게":
                    slow_mode = False
                    # 문장 부호와 공백을 바짝 붙여서 빠르게 읽도록 유도
                    processing_text = processing_text.replace(". ", ".").replace(", ", ",")
                else:
                    slow_mode = False  # 보통 속도
                
                # 구글 TTS 음성 생성
                tts = gTTS(text=processing_text, lang='ko', slow=slow_mode)
                
                mp3_fp = io.BytesIO()
                tts.write_to_fp(mp3_fp)
                mp3_bytes = mp3_fp.getvalue()
                
                if len(mp3_bytes) == 0:
                    st.error("음성 파일 생성에 실패했습니다. 다시 시도해 주세요.")
                else:
                    st.success("🎉 요청하신 방송 파일 작성이 완료되었습니다!")
                    
                    if include_chime:
                        st.write("🎵 **[1단계] 방송 시작 알림음:**")
                        st.audio(CHIME_URL, format="audio/ogg")
                        st.write("🗣️ **[2단계] 실제 안내 방송 내용:**")
                    
                    # 오디오 플레이어 노출 (여성 목소리 재생)
                    st.audio(mp3_bytes, format="audio/mp3")
                    
                    # 다운로드 버튼
                    st.download_button(
                        label="📥 스마트폰에 방송 MP3 다운로드하기",
                        data=mp3_bytes,
                        file_name="스마트_모바일_방송.mp3",
                        mime="audio/mp3",
                        use_container_width=True
                    )
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
