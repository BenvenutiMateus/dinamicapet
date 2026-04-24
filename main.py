# Adiciona pytz para controle de fuso horário
import streamlit as st
import time
import datetime
import pytz
# Função para iniciar o timer de uma fase



# Dicionário com as fases e desafios
FASES = {
    1: {
        "titulo": "Fase 1",
        "desafio": "",
        "senha" : datetime.datetime.now(pytz.timezone("America/Sao_Paulo")).strftime("%H:%M"),
        "dica" : "-... .- .-.. .- ---"
    },
    2: {
        "titulo": "Fase 2",
        "desafio": "Palavra cruzada",
        "senha" : st.secrets.senha_fase_2,
        "dica" : "teste"
    },
    3: {
        "titulo": "Fase 3",
        "desafio": "🔎📕",
        "senha" : st.secrets.senha_fase_3
        
    },
    4: {
        "titulo": "Fase 4",
        "desafio": "asjkpdjaksjfaop",
        "senha" : st.secrets.senha_fase_4
    },
    5: {
        "titulo": "Fase 5",
        "desafio": "A próxima senha é a minha maior vitória diária. Graças a Deus consegui acertar na 15ª tentativa hoje!",
        "senha" : st.secrets.senha_fase_5
    },
    6 : {
        "titulo": "Fase 6",
        "desafio": "Resolva a equação:",
        "senha" : st.secrets.senha_fase_6,
    },
    7 : {
        "titulo": "Fase 7",
        "desafio": "Encontre a raiz da função abaixo, dados os valores iniciais x₀ = 0.4 e x₁ = 0.6 com 5 iterações :",
        "formula": r"f(x) = \ln(x^2+1) \cdot \sin(5x) - \frac{x}{5}",
        "senha" : st.secrets.senha_fase_7,
        "dica" : "Use a fórmula da Secante para encontrar a raiz da função:",
        "dica_formula": r"x_2 = x_1 - \frac{f(x_1) x_0 - f(x_0) x_1}{f(x_1) - f(x_0)}"
    },
    8 : {
        "titulo": "Fase 8",
        "desafio": "Adivinhe a regra do jogo!",
        "senha" : st.secrets.senha_fase_8,
        "dica" : "Use a regra do trapézio para aproximar a integral:",
    }
}

def iniciar_fase(fase_nome):
    if f"start_time_{fase_nome}" not in st.session_state:
        st.session_state[f"start_time_{fase_nome}"] = time.time()

# Função para checar se já passaram 10 minutos
def passou_10_minutos(fase_nome):
    start_time = st.session_state.get(f"start_time_{fase_nome}")
    if start_time is None:
        return False
    return (time.time() - start_time) >= 600 # 600 segundos = 10 minutos

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
    iniciar_fase(fase["titulo"])
    st.header(fase["titulo"])
    # Exibir desafio e fórmula de forma elegante na fase 8
    if st.session_state.fase_atual == 7:
        st.write(f"**Desafio:** {fase['desafio']}")
        st.latex(fase['formula'])
    else:
        st.write(f"**Desafio:** {fase['desafio']}")

    tempo_decorrido = int(time.time() - st.session_state[f"start_time_{fase['titulo']}"])
    minutos = tempo_decorrido // 60
    segundos = tempo_decorrido % 60
    st.write(f"Tempo decorrido nesta fase: {minutos:02d}:{segundos:02d}")

    if passou_10_minutos(fase["titulo"]):
        if st.button("Mostrar dica!"):
            st.warning("Terão que pagar uma prenda!")
            dica = fase.get('dica', 'Aqui está sua dica para esta fase!')
            if st.session_state.fase_atual == 7:
                st.info(dica)
                st.latex(fase['dica_formula'])
            else:
                st.info(dica)

    resposta = st.text_input("Sua resposta:", key=f"resposta_{st.session_state.fase_atual}").lower().strip()
    senha = fase['senha']
    # Para as fases 7 e 8, permitir tolerância numérica
    if st.session_state.fase_atual in [6, 7]:
        try:
            resposta_num = float(resposta.replace(',', '.'))
            senha_num = float(str(senha).replace(',', '.'))
            correto = abs(resposta_num - senha_num) < 1e-3
        except Exception:
            correto = False
    else:
        correto = resposta == str(senha).lower().strip()

    if st.button("Verificar Resposta"):
        if correto:
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