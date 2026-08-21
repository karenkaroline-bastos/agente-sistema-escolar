from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class Buscador:
    """
    Realiza busca semântica nos conteúdos do manual.
    """

    def __init__(self, df):

        self.df = df

        print("Carregando modelo de embeddings...")

        self.modelo = SentenceTransformer(
            "paraphrase-multilingual-MiniLM-L12-v2"
        )

        print("Criando embeddings do manual...")

        self.embeddings = self.modelo.encode(
            df["conteudo"].tolist(),
            convert_to_numpy=True
        )

        print("Busca semântica pronta!")

    def buscar(
        self,
        pergunta,
        top_k=3,
        limite=0.35
    ):
        """
        Encontra os conteúdos mais semelhantes à pergunta.
        """

        pergunta_embedding = self.modelo.encode(
            [pergunta],
            convert_to_numpy=True
        )

        similaridades = cosine_similarity(
            pergunta_embedding,
            self.embeddings
        )[0]

        indices = similaridades.argsort()[::-1][:top_k]

        resultados = self.df.iloc[indices].copy()

        resultados["similaridade"] = similaridades[indices]

        # Mantém apenas resultados acima do limite
        resultados = resultados[
            resultados["similaridade"] >= limite
        ]

        return resultados