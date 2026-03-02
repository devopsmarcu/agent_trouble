import streamlit as st
import requests

# Configuração da página
st.set_page_config(page_title="Suporte Técnico HSI", page_icon="🤖", layout="wide")

st.title("🤖 Suporte Técnico HSI")
st.markdown("Faça sua pergunta! Responderei com base na Base de Conhecimento Local.")

# Estado da sessão para armazenar o chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibir histórico de mensagens do chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# React to user input
if prompt := st.chat_input("Ex: Erro ao logar no domínio..."):
    # Render user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Consultando base de conhecimento..."):
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/ask",
                    json={"query": prompt}
                )

                if response.status_code == 200:
                    data = response.json()
                    source_label = data.get("source", "local").upper()

                    resp_markdown = f"**Fonte:** `{source_label}`\n\n{data.get('answer')}"
                    st.markdown(resp_markdown)
                    st.session_state.messages.append({"role": "assistant", "content": resp_markdown})
                else:
                    st.error(f"Erro do agente: {response.text}")

            except Exception:
                st.error("Falha ao comunicar com o servidor Backend (`FastAPI`). O servidor uvicorn está rodando?")
