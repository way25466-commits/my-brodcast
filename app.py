import streamlit as st
from gtts import gTTS
import io
import time

st.set_page_config(page_title="스마트 방송국", page_icon="📢", layout="centered")
st.title("📢 모바일 스마트 방송 시스템")
st.caption("텍스트를 입력하면 안내 음성 MP3를 만들고 브라우저에서 차임벨과 함께 연속 재생합니다.")

# 웹에 등록된 오픈소스 차임벨 MP3 주소 (안정적인 4타음 효과음)
CHIME_URL = "https://google.com" 
# 혹은 알림용 다른 무료 벨소리 주소 활용 가능

broadcast_text = st.text_area(
    "💬 방송 안내문을 입력하세요:", 
    value="주민 여러분 안녕하십니까. 관리사무소에서 안내 말씀 드립니다. 잠시 후 오전 10시부터 단지 내 물탱크 청소로 인해 단수가 예정되어 있습니다. 주민 여러분께서는 미리 생활용수를 확보하시어 불편이 없으시길 바랍니다. 감사합니다.",
    height=200
)

include_chime = st.checkbox("🔔 방송 시작 전 차임벨(시작음) 먼저 재생하기", value=True)
speed_option = st.radio("🏃‍♂️ 방송 속도 조절", ["보통 속도", "조금 느리게"], index=0)
slow_mode = True if speed_option == "조금 느리게" else False

if st.button("🚀 방송 MP3 파일 만들기", use_container_width=True):
    if not broadcast_text.strip():
        st.error("방송 내용을 입력해 주세요!")
    else:
        with st.spinner("⏳ 아나운서 기계음 생성 중..."):
            try:
                # 구글 TTS 음성 생성
                tts = gTTS(text=broadcast_text, lang='ko', slow=slow_mode)
                voice_fp = io.BytesIO()
                tts.write_to_fp(voice_fp)
                voice_bytes = voice_fp.getvalue()
                
                st.success("🎉 방송 파일 작성이 완료되었습니다!")
                
                # 차임벨 선택 시 브라우저에서 차임벨 송출 후 음성 안내 진행 유도
                if include_chime:
                    st.write("🎵 **[1단계] 방송 시작 알림음:**")
                    st.audio(CHIME_URL, format="audio/ogg")
                    st.write("🗣️ **[2단계] 실제 안내 방송 내용:**")
                
                # 본문 안내방송 오디오 플레이어
                st.audio(voice_bytes, format="audio/mp3")
                
                # 다운로드 버튼
                st.download_button(
                    label="📥 스마트폰에 방송 MP3 다운로드하기",
                    data=voice_bytes,
                    file_name="스마트_모바일_방송.mp3",
                    mime="audio/mp3",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
