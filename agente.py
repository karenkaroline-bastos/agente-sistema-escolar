import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv()


# ============================================================
# CONFIGURAÇÃO DA API
# ============================================================

def obter_api_key():

    # Streamlit Cloud
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

        # Inicializa Gemini
        self.client = genai.Client(
            api_key=api_key
        )

        # Modelo
        self.modelo = "gemini-3.6-flash"


    # ========================================================
    # CONSULTA AO MANUAL
    # ========================================================

    def perguntar(self, pergunta):

        # Busca informações no manual
        contexto = self.buscador.buscar(pergunta)

        # ----------------------------------------------------
        # Verifica se não encontrou resultados
        # ----------------------------------------------------

        if contexto is None:
            return (
                "Não encontrei informações suficientes "
                "no Manual do Sistema Escolar para "
                "responder a essa pergunta."
            )

        # Se o retorno for um DataFrame
        if hasattr(contexto, "empty"):

            if contexto.empty:
                return (
                    "Não encontrei informações suficientes "
                    "no Manual do Sistema Escolar para "
                    "responder a essa pergunta."
                )

            # Converte o DataFrame para texto
            contexto = contexto.to_string(
                index=False
            )

        # Se o retorno for uma lista vazia
        elif isinstance(contexto, list):

            if len(contexto) == 0:
                return (
                    "Não encontrei informações suficientes "
                    "no Manual do Sistema Escolar para "
                    "responder a essa pergunta."
                )

            contexto = "\n".join(
                str(item) for item in contexto
            )

        # Se for outro tipo de retorno
        else:

            contexto = str(contexto)

            if not contexto.strip():
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
2. Utilize somente as informações do contexto.
3. Se a informação não estiver no contexto, informe que
   ela não foi encontrada no manual.
4. Responda sempre em português do Brasil.
5. Seja claro e objetivo.
6. Quando houver um procedimento, apresente os passos
   de forma numerada.
7. Não crie procedimentos que não estejam no manual.

CONTEXTO DO MANUAL:

{contexto}

PERGUNTA DO USUÁRIO:

{pergunta}

RESPOSTA:
"""


        # ====================================================
        # CONSULTA AO GEMINI
        # ====================================================

        resposta = self.client.models.generate_content(
            model=self.modelo,
            contents=prompt
        )

        return resposta.text


    # ========================================================
    # MÉTODO UTILIZADO PELO APP.PY
    # ========================================================

    def responder(self, pergunta):

        return self.perguntar(pergunta)
