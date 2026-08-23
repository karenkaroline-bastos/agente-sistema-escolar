import os
import streamlit as st

from google import genai


class Agente:
    """
    Agente responsável por consultar o manual
    e gerar respostas utilizando o Gemini.
    """

    def __init__(self, buscador):

        self.buscador = buscador

        api_key = sst.secrets["GEMINI_API_KEY"]

        if not api_key:
            raise ValueError(
                "A variável GEMINI_API_KEY não foi encontrada. "
                "Verifique o arquivo .env."
            )

        self.cliente = genai.Client(
            api_key=api_key
        )

    def responder(self, pergunta):

        resultados = self.buscador.buscar(
            pergunta
        )

        # Caso nenhuma informação relevante seja encontrada
        if resultados.empty:

            return (
                "Não encontrei informações suficientes "
                "no Manual do Sistema Escolar para "
                "responder a essa pergunta."
            )

        # Junta os resultados encontrados
        contexto = "\n\n".join(
            resultados["conteudo"].tolist()
        )

        prompt = f"""
Você é um assistente especializado no Sistema Escolar.

Sua função é responder perguntas utilizando SOMENTE
as informações presentes no manual fornecido.

REGRAS IMPORTANTES:

1. Não invente informações.
2. Não utilize conhecimentos externos ao manual.
3. Responda sempre em português.
4. Seja claro e objetivo.
5. Se a informação não estiver no manual,
   informe que não encontrou a resposta.
6. Não diga que possui acesso a outros sistemas.
7. Não crie procedimentos que não estejam no manual.

INFORMAÇÕES ENCONTRADAS NO MANUAL:

{contexto}

PERGUNTA DO USUÁRIO:

{pergunta}

Responda somente com base nas informações
encontradas no manual.
"""

        resposta = self.cliente.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        return resposta.text
