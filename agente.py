import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv()


def obter_api_key():

    # Tenta obter a chave do Streamlit Cloud
    try:
        return st.secrets["GEMINI_API_KEY"]

    except (KeyError, FileNotFoundError):

        # Tenta obter a chave do arquivo .env
        api_key = os.getenv("GEMINI_API_KEY")

        if api_key:
            return api_key

        raise ValueError(
            "GEMINI_API_KEY não foi encontrada. "
            "Configure a chave no .env ou nos Secrets do Streamlit."
        )


class Agente:

    def __init__(self, buscador):

        self.buscador = buscador

        # Obtém a chave da API
        api_key = obter_api_key()

        # Cria o cliente Gemini
        self.client = genai.Client(
            api_key=api_key
        )

        # Modelo Gemini
        self.modelo = "gemini-3.6-flash"


    def perguntar(self, pergunta):

        # Busca informações no manual
        contexto = self.buscador.buscar(pergunta)

        if not contexto:

            return (
                "Não encontrei informações suficientes "
                "no Manual do Sistema Escolar para "
                "responder a essa pergunta."
            )

        prompt = f"""
Você é um assistente especializado no Sistema Escolar.

Sua função é responder perguntas utilizando exclusivamente
as informações encontradas no manual.

Não invente informações.

Se a resposta não estiver no contexto, informe que
não encontrou a informação no manual.

Responda sempre em português do Brasil.

Quando possível, apresente a resposta em passos numerados.

CONTEXTO DO MANUAL:

{contexto}

PERGUNTA:

{pergunta}

RESPOSTA:
"""

        resposta = self.client.models.generate_content(
            model=self.modelo,
            contents=prompt
        )

        return resposta.text
