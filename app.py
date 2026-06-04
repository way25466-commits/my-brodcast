import streamlit as st
from gtts import gTTS
from pydub import AudioSegment
from pydub.generators import Sine
import io
import os

st.set_page_config(page_title="스마트 방송국", page_icon="📢", layout="centered")
st.title("📢 모바일 스마트 방송 시스템")
st.caption("텍스트를 입력하면 차임벨과 무료 기계음 음성이 합성된 MP3를 만듭니다.")

broadcast_text = st.text_area(
    "💬 방송 안내문을 입력하세요:", 
    value="주민 여러분 안녕하십니까. 관리사무소에서 안내 말씀 드립니다. 잠시 후 오전 10시부터 단지 내 물탱크 청소로 인해 단수가 예정되어 있습니다. 주민 여러분께서는 미리 생활용수를 확보하시어 불편이 없으시길 바랍니다. 감사합니다.",
    height=200
)

include_chime = st.checkbox("🔔 방송 시작 전 차임벨(4타음 딩동댕) 넣기", value=True)
speed_option = st.radio("🏃‍♂️ 방송 속도 조절", ["보통 속도", "조금 느리게"], index=0)
slow_mode = True if speed_option == "조금 느리게" else False

def generate_chime():
    notes = [523.25, 659.25, 783.99, 1046.50]
    chime_audio = AudioSegment.empty()
    for note in notes:
        tone = Sine(note).to_audio_segment(duration=400).apply_gain(-10)
        tone = tone.fade_out(100)
        chime_audio += tone
    return chime_audio + AudioSegment.silent(duration=1500)

if st.button("🚀 방송 MP3 파일 만들기", use_container_width=True):
    if not broadcast_text.strip():
        st.error("방송 내용을 입력해 주세요!")
    else:
        with st.spinner("⏳ 아나운서 기계음 합성 중..."):
            try:
                tts = gTTS(text=broadcast_text, lang='ko', slow=slow_mode)
                voice_fp = io.BytesIO()
                tts.write_to_fp(voice_fp)
                voice_fp.seek(0)
                voice_audio = AudioSegment.from_file(voice_fp, format="mp3")
                
                if include_chime:
                    chime_audio = generate_chime()
                    final_audio = chime_audio + voice_audio
                else:
                    final_audio = voice_audio
                
                output_fp = io.BytesIO()
                final_audio.export(output_fp, format="mp3")
                output_bytes = output_fp.getvalue()
                
                st.success("🎉 방송 파일 작성이 완료되었습니다!")
                st.audio(output_bytes, format="audio/mp3")
                st.download_button(
                    label="📥 스마트폰에 MP3 다운로드하기",
                    data=output_bytes,
                    file_name="스마트_모바일_방송.mp3",
                    mime="audio/mp3",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
