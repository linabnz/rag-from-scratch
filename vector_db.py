import chromadb
from sentence_transformers import SentenceTransformer

from config import EMBEDDING_MODEL


class VectorDB:
    def __init__(self, persist_path, chunks=None):
        self.client = chromadb.PersistentClient(path=persist_path)
        self.collection = self.client.get_or_create_collection(
            name="chunks",
            metadata={"embedding_model": EMBEDDING_MODEL},
        )

        if self.collection.count() > 0:
            # La base existe déjà : on recharge le modèle qui a servi à l'indexer,
            # pas forcément celui écrit dans config.py aujourd'hui.
            model_name = self.collection.metadata["embedding_model"]
            self.model = SentenceTransformer(model_name)
        elif chunks:
            self.model = SentenceTransformer(EMBEDDING_MODEL)
            embeddings = self._encode(chunks)
            self.collection.add(
                ids=[str(i) for i in range(len(chunks))],
                documents=chunks,
                embeddings=embeddings,
                metadatas=[{"source": f"chunk_{i}"} for i in range(len(chunks))],
            )
        else:
            raise ValueError(
                "Aucune base existante à ce chemin et aucun chunk fourni "
                "pour en créer une."
            )

    def _encode(self, texts):
        return self.model.encode(
            texts,
            batch_size=32,
            normalize_embeddings=True,
            show_progress_bar=True,
        ).tolist()

    def retrieve(self, question, n=3):
        query_embedding = self._encode([question])
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=n,
        )
        return {
            "documents": results["documents"][0],
            "metadatas": results["metadatas"][0],
            "distances": results["distances"][0],
        }
