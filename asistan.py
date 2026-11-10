import streamlit as st
from groq import Groq

# Sayfa ayarları ve başlığı
st.set_page_config(page_title="Ipon AI", page_icon="✨")
st.title("✨ Ipon AI")
st.markdown("Selam! Ben İpon. Hadi ne konuşmak istiyorsun?")

# Groq API anahtarın
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
# Sohbet geçmişi
if "messages" not in st.session_state:
    st.session_state.messages = []

# Eski mesajları ekranda tut
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcıdan mesaj al
if prompt := st.chat_input("İpon'a bir şeyler sor..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        client = Groq(api_key=GROQ_API_KEY)
        
        with st.chat_message("assistant"):
            with st.spinner("İpon düşünüyor..."):
                completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": "Senin adın İpon AI. Kullanıcıyla samimi, neşeli, arkadaş canlısı ve Türkçe olarak konuşan bir yapay zekasın."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                )
                cevap = completion.choices[0].message.content
                st.markdown(cevap)
                
        st.session_state.messages.append({"role": "assistant", "content": cevap})
        
    except Exception as e:
        st.error(f"Bir hata oluştu: {e}")
