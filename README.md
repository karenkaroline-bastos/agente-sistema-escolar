# 🤖 Assistente Inteligente do Sistema Escolar

Agente de Inteligência Artificial desenvolvido em Python para responder perguntas em linguagem natural sobre documentos internos de uma empresa.

O projeto utiliza um Manual do Sistema Escolar em formato Excel como base de conhecimento. O usuário pode realizar perguntas sem precisar abrir o documento manualmente, e o agente busca as informações mais relevantes no manual antes de gerar a resposta.

---

## 🎯 Objetivo

O objetivo deste projeto é desenvolver um agente de IA capaz de consultar documentos internos e responder perguntas de forma rápida, simples e natural.

A solução foi desenvolvida como parte de um desafio de Inteligência Artificial, utilizando técnicas de busca semântica e geração de respostas com um modelo de linguagem.

---

## 💡 Problema

Manuais de sistemas podem conter muitas informações e procedimentos, tornando a busca manual demorada.

Por exemplo, para descobrir como alterar uma senha, o usuário normalmente precisaria:

1. Abrir o manual;
2. Procurar o procedimento;
3. Identificar a informação correta;
4. Ler as instruções;
5. Aplicar o procedimento.

Com o agente desenvolvido neste projeto, o usuário pode simplesmente perguntar:

> "Esqueci minha senha. Como faço para acessar o sistema?"

O agente consulta o manual e apresenta a resposta em linguagem natural.

---

## 🚀 Solução

A aplicação utiliza uma arquitetura baseada em busca semântica e inteligência artificial.

O fluxo principal é:

```text
                    Manual Excel
                         │
                         ▼
                  Carregamento
                    do documento
                         │
                         ▼
                  Pré-processamento
                         │
                         ▼
                  Embeddings
                         │
                         ▼
                  Busca Semântica
                         │
                         ▼
                Conteúdo relevante
                         │
                         ▼
                     Gemini
                         │
                         ▼
                    Resposta
                         │
                         ▼
                   Interface Web
                    (Streamlit)


