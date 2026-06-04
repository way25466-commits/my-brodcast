import streamlit as st
from gtts import gTTS
import io

st.set_page_config(page_title="스마트 방송국", page_icon="📢", layout="centered")
st.title("📢 모바일 스마트 방송 시스템")
st.caption("안정적인 오디오 스트리밍 기능이 반영된 무료 방송 자동화 버전입니다.")

# Google Actions에서 제공하는 기본 안내 방송용 알림음 주소
CHIME_URL = "https://google.com" 

broadcast_text = st.text_area(
    "💬 방송 안내문을 입력하세요:", 
    value="주민 여러분 안녕하십니까. 관리사무소에서 안내 말씀 드립니다. 잠시 후 오전 10시부터 단지 내 물탱크 청소로 인해 단수가 예정되어 있습니다. 주민 여러분께서는 미리 생활용수를 확보하시어 불편이 없으시길 바랍니다. 감사합니다.",
    height=200
)

# 1. 속도 옵션 제공
speed_option = st.radio("🏃‍♂️ 방송 속도 조절", ["보통 속도", "조금 느리게"], index=0)
include_chime = st.checkbox("🔔 방송 시작 전 차임벨(시작음) 먼저 재생하기", value=True)

if st.button("🚀 방송 MP3 파일 만들기", use_container_width=True):
    if not broadcast_text.strip():
        st.error("방송 내용을 입력해 주세요!")
    else:
        with st.spinner("⏳ 목소리 파일 생성 중..."):
            try:
                # 속도 모드 변환 설정
                slow_mode = True if speed_option == "조금 느리게" else False
                
                # 구글 음성 생성 엔진 안전 모드 가동
                tts = gTTS(text=broadcast_text.strip(), lang='ko', slow=slow_mode)
                
                # 메모리 버퍼 안정화 후 데이터 추출
                mp3_fp = io.BytesIO()
                tts.write_to_fp(mp3_fp)
                mp3_bytes = mp3_fp.getvalue()
                
                if len(mp3_bytes) == 0:
                    st.error("음성 데이터를 생성하지 못했습니다. 다시 시도해 주세요.")
                else:
                    st.success("🎉 방송 파일 작성이 완료되었습니다!")
                    
                    # 차임벨 선택 시 브라우저에서 차임벨 우선 노출
                    if include_chime:
                        st.write("🎵 **[1단계] 방송 시작 알림음:**")
                        st.audio(CHIME_URL, format="audio/ogg")
                        st.write("🗣️ **[2단계] 실제 안내 방송 내용:**")
                    
                    # 안전하게 음성 플레이어 출력
                    st.audio(mp3_bytes, format="audio/mp3")
                    
                    # 다운로드 버튼 제공
                    st.download_button(
                        label="📥 스마트폰에 방송 MP3 다운로드하기",
                        data=mp3_bytes,
                        file_name="스마트_모바일_방송.mp3",
                        mime="audio/mp3",
                        use_container_width=True
                    )
            except Exception as e:
                st.error(f"오디오 변환 중 서버 통신 에러가 발생했습니다: {e}")
                st.info("방송 내용 문장 끝에 마침표(.)를 명확히 찍어 주시거나 텍스트 길이를 조금 줄여서 다시 시도해 보세요.")
