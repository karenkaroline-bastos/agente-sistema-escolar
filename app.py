import streamlit as st
from dotenv import load_dotenv

from dados import carregar_manual
from busca import Buscador
from agente import Agente


# ==========================================
# CONFIGURAÇÃO
# ==========================================

load_dotenv()

st.set_page_config(
    page_title="Assistente Sistema Escolar",
    page_icon="🤖",
    layout="centered"
)


# ==========================================
# CARREGAMENTO DOS DADOS
# ==========================================

@st.cache_data
def carregar_dados():

    return carregar_manual()


@st.cache_resource
def criar_buscador(df):

    return Buscador(df)


df = carregar_dados()

buscador = criar_buscador(df)


df = carregar_dados()

buscador = criar_buscador(df)

agente = Agente(buscador)


# ==========================================
# CABEÇALHO
# ==========================================

st.title("🤖 Assistente do Sistema Escolar")

st.write(
    "Consulte informações do Manual do Sistema Escolar "
    "utilizando linguagem natural."
)


# ==========================================
# EXEMPLOS DE PERGUNTAS
# ==========================================

st.info(
    "💡 Exemplos: "
    "Como faço para cadastrar um aluno? "
    "Como altero minha senha? "
    "Como consulto uma matrícula?"
)


# ==========================================
# CAMPO DE PERGUNTA
# ==========================================

pergunta = st.text_input(
    "💬 Digite sua pergunta:",
    placeholder="Ex.: Como faço para cadastrar um aluno?"
)


# ==========================================
# BOTÃO PERGUNTAR
# ==========================================

if st.button(
    "🔍 Perguntar",
    use_container_width=True
):

    if not pergunta.strip():

        st.warning(
            "Digite uma pergunta antes de continuar."
        )

    else:

        with st.spinner(
            "🔎 Consultando o manual..."
        ):

            try:

                resposta = agente.responder(
                    pergunta
                )

                st.subheader("💬 Resposta")

                st.write(resposta)

            except Exception as erro:

                st.error(
                    "Ocorreu um erro ao consultar o agente."
                )

                st.exception(erro)


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.header("📚 Sobre o agente")

    st.write(
        "Este agente utiliza inteligência artificial "
        "para consultar o Manual do Sistema Escolar."
    )

    st.divider()

    st.metric(
        "Procedimentos disponíveis",
        len(df)
    )

    st.divider()

    st.write("Tecnologias utilizadas:")

    st.write(
        """
        🐍 Python  
        📊 Pandas  
        🧠 Embeddings  
        🔎 Busca semântica  
        🤖 Gemini  
        🎨 Streamlit  
        """
    )

    st.divider()

    st.caption(
        "Agente de IA para consulta "
        "inteligente de documentos."
    )