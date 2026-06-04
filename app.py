import streamlit as st
from gtts import gTTS
import io

st.set_page_config(page_title="스마트 방송국", page_icon="📢", layout="centered")

# ==========================================
# 🔒 [보안 설정] 여기에 원하시는 비밀번호를 적으세요!
# ==========================================
CORRECT_PASSWORD = "관리소비번123"  # <--- 이 부분을 원하시는 비밀번호로 변경하세요.
# ==========================================

# 🔑 로그인 화면 구현
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.title("🔒 스마트 방송국 로그인")
    st.write("안전한 방송 송출을 위해 관리자 비밀번호를 입력해 주세요.")
    
    # 비밀번호 입력창 (글자가 숨겨져서 입력됩니다)
    user_password = st.text_input("비밀번호 입력", type="password")
    
    if st.button("로그인하기", use_container_width=True):
        if user_password == CORRECT_PASSWORD:
            st.session_state["authenticated"] = True
            st.rerun()  # 화면 새로고침하여 본문 진입
        else:
            st.error("❌ 비밀번호가 올바르지 않습니다. 다시 입력해 주세요.")
            
    st.stop()  # 로그인 성공 전까지 아래 방송국 프로그램 실행을 완전히 차단

# ==========================================
# 🔓 로그인 성공 시에만 아래 실제 방송 프로그램이 실행됩니다.
# ==========================================

st.title("📢 모바일 스마트 방송 시스템")
st.caption("인증된 관리자 전용 방송 자동화 시스템입니다.")

# 로그아웃 버튼 (화면 우측 상단 배치)
col1, col2 = st.columns([4, 1])
with col2:
    if st.button("🔒 로그아웃"):
        st.session_state["authenticated"] = False
        st.rerun()

CHIME_URL = "https://google.com" 

templates = {
    "직접 타이핑하기": "",
    "🚬 층간흡연 자제 방송 (정중한 톤)": "주민 여러분 안녕하십니까. 관리사무소에서 안내 말씀 드립니다. 최근 공동주택 내 베란다, 복도, 그리고 세대 내 욕실에서의 흡연으로 인해 층간 간접흡연 피해를 호소하는 세대가 늘고 있습니다. 공동주택의 특성상 환기구와 베란다를 통해 담배 연기가 이웃 세대로 그대로 유입되어, 임산부나 어린 자녀가 있는 가정에 큰 고통을 주고 있습니다. 건강하고 쾌적한 주거 환경을 위해 세대 내 및 공용 공간에서의 흡연을 절대 자제해 주시기를 당부드립니다. 이웃을 배려하는 아름다운 문화를 만들어 갑시다. 감사합니다.",
    "🚫 층간흡연 자제 방송 (경고성 톤)": "주민 여러분 안녕하십니까. 관리사무소에서 간접흡연 피해 방지를 위한 강력한 당부 말씀 드립니다. 현재 일부 세대의 베란다, 복도, 욕실 내 흡연으로 인해 주변 세대에서 심각한 악취와 호흡기 고통을 호소하고 있습니다. 나에게는 개인 공간일지라도, 배관을 타고 올라가는 담배 연기는 이웃에게는 참기 힘든 피해가 됩니다. 이웃 주민들의 건강과 안전을 위협하는 행위이오니, 흡연은 반드시 지정된 외부 흡연 구역을 이용해 주시기 바랍니다. 공동생활의 기본 질서가 지켜질 수 있도록 주민 여러분의 적극적인 협조를 바랍니다. 감사합니다.",
    "🚰 단수 안내 방송": "주민 여러분 안녕하십니까. 관리사무소에서 안내 말씀 드립니다. 잠시 후 오전 10시부터 단지 내 물탱크 청소 및 배관 점검으로 인해 일부 동에 단수가 예정되어 있습니다. 주민 여러분께서는 미리 생활용수를 확보하시어 이용에 불편이 없으시길 바랍니다. 감사합니다.",
    "⚡ 정전 안내 방송": "주민 여러분 안녕하십니까. 관리사무소에서 안내 말씀 드립니다. 오늘 오후 2시부터 4시까지 아파트 내 전기 설비 정기 정밀 검사로 인해 아파트 전 세대 및 승강기 정전이 예정되어 있습니다. 정전 시간 동안 가전제품의 전원을 꺼두어 주시고 안전사고에 유의하시기 바랍니다. 감사합니다.",
    "🚗 주차 단속 안내 방송": "주민 여러분 안녕하십니까. 관리사무소에서 안내 말씀 드립니다. 현재 단지 내 소방차 전용 구역 및 통행로에 불법 주차된 차량으로 인해 다른 주민들의 통행에 큰 불편을 초래하고 있습니다. 해당 차주 분께서는 이 방송을 듣는 즉시 차량을 이동 주차해 주시기 바랍니다. 감사합니다.",
    "📦 택배 수령 안내 방송": "주민 여러분 안녕하십니까. 관리사무소에서 안내 말씀 드립니다. 경비실에 장기 보관 중인 택배 물품이 많아 보관 장소가 협소합니다. 주민 여러분께서는 경비실을 방문하시어 본인의 택배 물품을 조속히 수령해 가시기 바랍니다. 감사합니다."
}

st.subheader("📋 자주 쓰는 방송문 불러오기")
selected_template = st.selectbox("아래 목록에서 방송 종류를 선택하면 글자가 자동으로 채워집니다:", list(templates.keys()))

default_text = templates[selected_template]

st.subheader("💬 방송 내용 확인 및 수정")
broadcast_text = st.text_area(
    "방송 안내문을 확인하고 날짜나 시간을 수정하세요:", 
    value=default_text,
    height=200
)

st.selectbox("👤 방송 목소리 선택", ["여성 아나운서 톤 (기본 무료)"])
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
                
                if speed_option == "매우 느리게":
                    slow_mode = True
                    processing_text = " ".join(list(processing_text.replace(" ", "  ")))
                elif speed_option == "매우 빠르게":
                    slow_mode = False
                    processing_text = processing_text.replace(". ", ".").replace(", ", ",")
                else:
                    slow_mode = False
                
                tts = gTTS(text=processing_text, lang='ko', slow=slow_mode)
                
                mp3_fp = ioBytesIO() if 'ioBytesIO' in locals() else io.BytesIO()
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
                    
                    st.audio(mp3_bytes, format="audio/mp3")
                    st.download_button(
                        label="📥 스마트폰에 방송 MP3 다운로드하기",
                        data=mp3_bytes,
                        file_name="스마트_모바일_방송.mp3",
                        mime="audio/mp3",
                        use_container_width=True
                    )
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
