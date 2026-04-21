import streamlit as st
# Configurar página
st.set_page_config(page_title="Desafios por Fases", layout="centered")

# Dicionário com as fases e desafios
FASES = {
    1: {
        "titulo": "Fase 1",
        "desafio": "Qual é a capital do Brasil?",
    },
    2: {
        "titulo": "Fase 2",
        "desafio": "Quanto é 15 × 8?",
    },
    3: {
        "titulo": "Fase 3",
        "desafio": "Qual é o maior planeta do sistema solar?",
    },
    4: {
        "titulo": "Fase 4",
        "desafio": "Qual é a fórmula química da água?",
    },
}
# Inicializar estado da sessão
if "fase_atual" not in st.session_state:
    st.session_state.fase_atual = 1
if "mensagem" not in st.session_state:
    st.session_state.mensagem = ""
if "senhas_corretas" not in st.session_state:
    st.session_state.senhas_corretas = []

st.title("🎮 Desafio por Fases")

# Verificar se completou todas as fases
if st.session_state.fase_atual > len(FASES):
    st.success("🎉 Parabéns! Você completou todos os desafios!")
    if st.button("Reiniciar"):
        st.session_state.fase_atual = 1
        st.session_state.mensagem = ""
        st.session_state.senhas_corretas = []
        st.rerun()
else:
    # Obter fase atual
    fase = FASES[st.session_state.fase_atual]
    st.header(fase["titulo"])
    st.write(f"**Desafio:** {fase['desafio']}")
    resposta = st.text_input("Sua resposta:", key=f"resposta_{st.session_state.fase_atual}").lower().strip()
    senha = st.secrets[f"senha_fase_{st.session_state.fase_atual}"].lower().strip()
    if st.button("Verificar Resposta"):
        if resposta == senha:
            st.session_state.mensagem = "✅ Correto!"
            st.success(st.session_state.mensagem)
            # Salvar senha correta
            st.session_state.senhas_corretas.append({"fase": st.session_state.fase_atual, "senha": senha})
            st.session_state.fase_atual += 1
            st.rerun()
        else:
            st.session_state.mensagem = "❌ Incorreto! Tente novamente."
            st.error(st.session_state.mensagem)
    st.caption(f"Fase {st.session_state.fase_atual} de {len(FASES)}")