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
        "dica" : "Ordem das dicas: 3, 5, 7, 1, 6, 4, 2"
    },
    3: {
        "titulo": "Fase 3",
        "desafio": "🔎📕",
        "senha" : st.secrets.senha_fase_3,
					"dica" : "p, l, p"
        
    },
    4: {
        "titulo": "Fase 4",
        "desafio": """
Era uma vez, em um reino muito distante, um Rei sortudo que governava sob a proteção dos trevos de quatro folhas. Ele vivia em um castelo cercado por 10 familiares muito unidos, que o ajudavam a manter a prosperidade das terras.

Certo dia, em uma viagem diplomática, o Rei encontrou uma Rainha apaixonada, cujos olhos brilhavam como o mais puro afeto. Foi amor à primeira vista, e o casal logo percebeu que suas vidas estavam entrelaçadas para sempre.

Para celebrar a união, o Rei enviou seu mais ágil mensageiro, conhecido por carregar as moedas reais. O mensageiro deveria levar 5 sacos de ouro para cada província, como símbolo de generosidade.

Porém, o caminho era perigoso. O reino vizinho, governado pelo medo, enviou um soldado solitário armado com uma lança afiada para impedir a festa. Esse soldado era acompanhado por 8 espiões que se escondiam nas sombras das montanhas.

Para proteger o reino, o Rei consultou o Mestre das Armas, um homem que conhecia todas as estratégias de combate. Ele forjou 4 espadas mágicas para os cavaleiros da guarda. 

No final, a paz prevaleceu. A Rainha, com sua sabedoria, organizou um banquete onde serviram 9 taças de cristal com o melhor vinho do reino para os líderes das vilas. E assim, o Rei sábio e sua Rainha viveram felizes, sabendo que a união era sua maior riqueza.
""",
        "senha" : st.secrets.senha_fase_4,
					"dica" : "O Caio irá orientá-los"
    },
    5: {
        "titulo": "Fase 5",
        "desafio": "A próxima senha é a minha maior vitória diária. Graças a Deus consegui acertar na 15ª tentativa hoje!",
        "senha" : st.secrets.senha_fase_5,
					"dica" : "Contextualizando vocês, a resposta da pergunta é a resposta de um jogo diário"
    },
    
    6 : {
        "titulo": "Fase 6",
        "desafio": "Adivinhe a regra do jogo!",
        "senha" : st.secrets.senha_fase_8,
        "dica" : "Peça a um integrante ",
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