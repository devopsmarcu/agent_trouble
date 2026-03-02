import streamlit as st
import requests

# Configuração da página
st.set_page_config(page_title="Agente Híbrido RAG", page_icon="🤖", layout="wide")

st.title("🤖 Suporte Técnico Híbrido (Local + Web)")
st.markdown("Faça sua pergunta! Responderei prioritariamente utilizando a Base de Conhecimento Local. Se o assunto for inédito, usarei a web para descobrir e você poderá avaliar se devo memorizar a resposta.")

# Estado da sessão para armazenar o chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibir histórico de mensagens do chat
for idx, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        
        # Se houver metadados (resultado de busca web), preparamos os botões
        if "metadata" in msg and msg["metadata"].get("needs_feedback") and not msg.get("feedback_given"):
            meta = msg["metadata"]
            col1, col2 = st.columns([1, 4])
            
            with col1:
                # Botão interativo que chama callback
                if st.button("👍 Útil (Salvar)", key=f"btn_useful_{idx}"):
                    try:
                        resp = requests.post("http://127.0.0.1:8000/feedback", json={
                            "query": meta["query"],
                            "answer": meta["answer"],
                            "context": meta["context"],
                            "source": meta["source"] or "web",
                            "is_helpful": True
                        })
                        if resp.status_code == 200:
                            st.success(resp.json().get("message", "Conhecimento salvo!"))
                            msg["feedback_given"] = True
                            st.rerun()
                    except Exception as e:
                        st.error("Erro de conexão com o Backend FastAPI.")

            with col2:
                if st.button("👎 Descartar", key=f"btn_discard_{idx}"):
                    msg["feedback_given"] = True
                    st.rerun()

# Barra lateral com configurações
with st.sidebar:
    st.header("⚙️ Configurações do Agente")
    search_mode = st.radio(
        "Modo de Busca:",
        options=["Automático (Local + Web)", "Apenas Base Local", "Apenas Web"],
        index=0,
        help="Automático: Tenta a base local (RAG), e se não tiver certeza, pesquisa na internet. Apenas Local: Não aciona a API externa sob hipótese alguma. Apenas Web: Ignora a memória e força uma nova busca online."
    )
    
    mode_map = {
        "Automático (Local + Web)": "auto",
        "Apenas Base Local": "local",
        "Apenas Web": "web"
    }

# React to user input
if prompt := st.chat_input("Ex: Erro ao logar no domínio..."):
    # Render user message
    st.chat_message("user").markdown(prompt)
    
    # Adicionar ao histórico
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Pensando ou pesquisando..."):
            try:
                # Chamada na porta do seu backend atual FastAPI passando a intenção local/web/auto
                payload = {
                    "query": prompt,
                    "mode": mode_map.get(search_mode)
                }
                response = requests.post("http://127.0.0.1:8000/ask", json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    source_label = data.get("source", "unknown").upper()
                    
                    # Formatação rica da resposta
                    resp_markdown = f"""
**Fonte de Conhecimento:** `{source_label}`
                    
{data.get("answer")}
"""
                    # Mostramos as URLs consultadas de maneira bonitinha.
                    if data.get("url") and data.get("url") != "N/A":
                        resp_markdown += f"\n\n🔗 **URLs de Base:** {data.get('url')}"
                        
                    st.markdown(resp_markdown)

                    # Salva no histórico. Se for web, guardamos dados para o botão aparecer em cima.
                    new_msg = {"role": "assistant", "content": resp_markdown}
                    
                    if data.get("needs_feedback"):
                        new_msg["metadata"] = {
                            "query": prompt,
                            "answer": data.get("answer"),
                            "context": data.get("context"),
                            "source": data.get("url"),
                            "needs_feedback": True
                        }
                        
                    st.session_state.messages.append(new_msg)
                    st.rerun()  # Atualiza a UI para que os botões (se houver) apareçam.
                else:
                    st.error(f"Erro do agente: {response.text}")
            except Exception as e:
                st.error("Falha ao comunicar com o servidor Backend (`FastAPI`). O servidor uvicorn está rodando?")
