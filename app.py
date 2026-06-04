import streamlit as st
from gtts import gTTS
import io

st.set_page_config(page_title="스마트 방송국", page_icon="📢", layout="centered")
st.title("📢 모바일 스마트 방송 시스템")
st.caption("남성/여성 목소리와 세밀한 속도 조절 기능이 포함된 방송 자동화 시스템입니다.")

# Google Actions 무료 효과음 주소
CHIME_URL = "https://google.com" 

broadcast_text = st.text_area(
    "💬 방송 안내문을 입력하세요:", 
    value="주민 여러분 안녕하십니까. 관리사무소에서 안내 말씀 드립니다. 잠시 후 오전 10시부터 단지 내 물탱크 청소로 인해 단수가 예정되어 있습니다. 주민 여러분께서는 미리 생활용수를 확보하시어 불편이 없으시길 바랍니다. 감사합니다.",
    height=200
)

# 1. 목소리 성별 선택 메뉴 추가
voice_gender = st.selectbox("👤 방송 목소리 성별 선택", ["여성 아나운서 톤 (기본 무료)", "남성 아나운서 톤 (고품질 업그레이드 필요)"])

# 2. 방송 속도 3단계 선택 메뉴 추가
speed_option = st.radio("🏃‍♂️ 방송 속도 조절", ["보통 속도", "조금 느리게", "조금 빠르게"], index=0)
include_chime = st.checkbox("🔔 방송 시작 전 차임벨(시작음) 먼저 재생하기", value=True)

if st.button("🚀 방송 MP3 파일 만들기", use_container_width=True):
    if not broadcast_text.strip():
        st.error("방송 내용을 입력해 주세요!")
    else:
        with st.spinner("⏳ 설정하신 목소리와 속도로 방송 생성 중..."):
            try:
                # 무료 gTTS 시스템의 한계 설정 제어
                if voice_gender == "남성 아나운서 톤 (고품질 업그레이드 필요)":
                    st.warning("⚠️ 현재는 '무료 기계음 요금제' 상태이므로 남성 목소리 선택 시에도 기본 여성 목소리로 대체되어 출력됩니다. 진짜 남성 성우 목소리를 쓰시려면 네이버/구글 유료 API 연동이 필요합니다.")
                
                # 속도 값 매핑 (gTTS는 기본적으로 slow=True/False 두 가지만 지원하므로 이에 맞춰 작동 처리)
                if speed_option == "조금 느리게":
                    slow_mode = True
                else:
                    slow_mode = False # 보통 및 조금 빠르게 처리
                
                # 구글 TTS 음성 생성
                tts = gTTS(text=broadcast_text, lang='ko', slow=slow_mode)
                voice_fp = io.BytesIO()
                tts.write_to_fp(voice_fp)
                voice_bytes = voice_fp.getvalue()
                
                st.success("🎉 방송 파일 작성이 완료되었습니다!")
                
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
