import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv()


# ============================================================
# OBTÉM A CHAVE DA API
# ============================================================

def obter_api_key():

    # Streamlit Cloud
    try:
        api_key = st.secrets["GEMINI_API_KEY"]

        if api_key:
            return api_key

    except (KeyError, FileNotFoundError):
        pass

    # Ambiente local (.env)
    api_key = os.getenv("GEMINI_API_KEY")

    if api_key:
        return api_key

    raise ValueError(
        "GEMINI_API_KEY não foi encontrada. "
        "Configure a chave no arquivo .env "
        "ou nos Secrets do Streamlit."
    )


# ============================================================
# AGENTE
# ============================================================

class Agente:

    def __init__(self, buscador):

        self.buscador = buscador

        # Obtém a chave da API
        api_key = obter_api_key()

        # Cliente Gemini
        self.client = genai.Client(
            api_key=api_key
        )

        # Modelo Gemini
        self.modelo = "gemini-3.6-flash"


    # ========================================================
    # MÉTODO PRINCIPAL
    # ========================================================

    def perguntar(self, pergunta):

        # Busca informações no manual
        contexto = self.buscador.buscar(pergunta)

        # Se não encontrou informação
        if not contexto:

            return (
                "Não encontrei informações suficientes "
                "no Manual do Sistema Escolar para "
                "responder a essa pergunta."
            )

        # ====================================================
        # PROMPT
        # ====================================================

        prompt = f"""
Você é um assistente especializado no Sistema Escolar.

Sua função é responder perguntas utilizando exclusivamente
as informações encontradas no Manual do Sistema Escolar.

REGRAS:

1. Não invente informações.
2. Utilize somente o contexto fornecido.
3. Se a informação não estiver no contexto, informe que
   ela não foi encontrada no manual.
4. Responda sempre em português do Brasil.
5. Seja claro e objetivo.
6. Quando houver um procedimento, apresente os passos
   de forma numerada.

CONTEXTO DO MANUAL:

{contexto}

PERGUNTA DO USUÁRIO:

{pergunta}

RESPOSTA:
"""

        # ====================================================
        # GEMINI
        # ====================================================

        resposta = self.client.models.generate_content(
            model=self.modelo,
            contents=prompt
        )

        return resposta.text


    # ========================================================
    # COMPATIBILIDADE COM O APP.PY
    # ========================================================

    def responder(self, pergunta):

        """
        Método utilizado pelo app.py.

        Ele chama o método perguntar(), mantendo
        compatibilidade com a interface atual.
        """

        return self.perguntar(pergunta)
