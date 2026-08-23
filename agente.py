import os
import streamlit as st
from dotenv import load_dotenv
from google import genai


# ============================================================
# CONFIGURAÇÃO DAS VARIÁVEIS DE AMBIENTE
# ============================================================

load_dotenv()


def obter_api_key():
    """
    Obtém a chave da API do Gemini.

    Primeiro tenta buscar nos Secrets do Streamlit Cloud.
    Se não encontrar, tenta buscar no arquivo .env local.
    """

    # Ambiente Streamlit Cloud
    try:
        api_key = st.secrets["GEMINI_API_KEY"]

        if api_key:
            return api_key

    except (KeyError, FileNotFoundError):
        pass

    # Ambiente local
    api_key = os.getenv("GEMINI_API_KEY")

    if api_key:
        return api_key

    raise ValueError(
        "GEMINI_API_KEY não foi encontrada. "
        "Configure a chave no arquivo .env ou nos Secrets do Streamlit."
    )


# ============================================================
# CLASSE DO AGENTE
# ============================================================

class Agente:

    def __init__(self, buscador):

        self.buscador = buscador

        # Obtém a chave da API
        api_key = obter_api_key()

        # Inicializa o cliente Gemini
        self.client = genai.Client(api_key=api_key)

        # Modelo utilizado pelo agente
        self.modelo = "gemini-3.6-flash"


    # ========================================================
    # REALIZA A PERGUNTA
    # ========================================================

    def perguntar(self, pergunta):

        # Busca informações relevantes no manual
        contexto = self.buscador.buscar(pergunta)

        # Caso não encontre informações
        if not contexto:

            return (
                "Não encontrei informações suficientes no "
                "Manual do Sistema Escolar para responder a essa pergunta."
            )


        # ====================================================
        # PROMPT DO AGENTE
        # ====================================================

        prompt = f"""
Você é um assistente especializado no Sistema Escolar.

Sua função é responder perguntas dos usuários utilizando
EXCLUSIVAMENTE as informações encontradas no manual fornecido.

Não invente informações.

Se a resposta não estiver presente no contexto fornecido,
informe educadamente que não encontrou a informação no manual.

Responda sempre em português do Brasil.

Se possível, apresente a resposta em passos numerados para
facilitar o entendimento do usuário.

CONTEXTO ENCONTRADO NO MANUAL:

{contexto}


PERGUNTA DO USUÁRIO:

{pergunta}


RESPOSTA:
"""


        # ====================================================
        # CHAMADA PARA O GEMINI
        # ====================================================

        resposta = self.client.models.generate_content(
            model=self.modelo,
            contents=prompt
        )


        return resposta.text
