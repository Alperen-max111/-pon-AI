import streamlit as st
from groq import Groq

# Sayfa Sekme Ayarları ve İkonu
st.set_page_config(page_title="İSİM = ABLAM", page_icon="👑", layout="centered")

# Sol Kenar Çubuğu (Sidebar)
with st.sidebar:
    st.title("👑 İSİM = ABLAM")
    st.caption("Özel Yapay Zeka Asistanı")
    st.markdown("---")
    if st.button("🗑️ Sohbeti Temizle", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Sayfanın Ortasındaki Büyük Başlık
st.title("👑 İSİM = ABLAM")
st.write("Karşınızda en kral abla asistanı! Ona dilediğinizi sorabilirsiniz.")

# Groq İstemci Bağlantısı (Hatasız Model ile)
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ablana bir şeyler yaz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
        )
        answer = response.choices[0].message.content
        st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
