import pandas as pd


def carregar_manual(caminho="Manual_Sistema_Escolar.xlsx"):
    """
    Carrega o manual em Excel e prepara o conteúdo
    para ser utilizado pelo agente.
    """

    df = pd.read_excel(caminho)

    # Verifica se as colunas esperadas existem
    colunas_necessarias = ["Chamados", "Respostas padrão"]

    for coluna in colunas_necessarias:
        if coluna not in df.columns:
            raise ValueError(
                f"A coluna '{coluna}' não foi encontrada no arquivo Excel."
            )

    # Remove linhas completamente vazias
    df = df.dropna(
        subset=colunas_necessarias,
        how="all"
    )

    # Preenche valores vazios
    df["Chamados"] = df["Chamados"].fillna("")
    df["Respostas padrão"] = df["Respostas padrão"].fillna("")

    # Cria o conteúdo que será utilizado na busca semântica
    df["conteudo"] = (
        "Chamado: "
        + df["Chamados"].astype(str)
        + "\nResposta: "
        + df["Respostas padrão"].astype(str)
    )

    return df