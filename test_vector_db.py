import csv

from vector_db import VectorDB

with open("data/05_corpus_rag.csv", encoding="utf-8") as f:
    CHUNKS = [row["text"] for row in csv.DictReader(f)]

QUESTIONS = [
    "Quelle est la couleur du chat de Bob ?",
    "Comment s'appelle le chien vert d'Alice ?",
    "Que collectionne la tortue de Carla ?",
    "Quel mot répète le perroquet de Diego ?",
    "Dans quel sens nage le poisson de Karim ?",
]

db = VectorDB(persist_path="./chroma_data", chunks=CHUNKS)

for question in QUESTIONS:
    result = db.retrieve(question, n=3)
    print(f"\nQuestion : {question}")
    for doc, dist in zip(result["documents"], result["distances"]):
        print(f"  [{dist:.4f}] {doc}")
