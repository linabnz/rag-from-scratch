# rag-from-scratch

Un RAG (Retrieval-Augmented Generation) minimal construit brique par brique :
ChromaDB + sentence-transformers pour la recherche, Groq pour la génération,
et un agent modérateur pour filtrer les tentatives de prompt injection.

Projet réalisé dans le cadre du mini-TP guidé du Master 2 MD5 — Data & IA.

## Architecture

- **`vector_db.py`** — classe `VectorDB` : crée ou recharge une base ChromaDB
  persistée, encode les chunks avec `sentence-transformers`, et retrouve les
  chunks les plus proches d'une question.
- **`moderator.py`** *(à venir)* — classe qui détecte les tentatives de prompt
  injection avant tout appel au LLM principal.
- **`rag.py`** *(à venir)* — classe `RAG` qui orchestre le pipeline complet :
  modération, retrieval, construction du prompt, appel au LLM.
- **`config.py`** — constantes centralisées (nom du modèle d'embedding et du LLM).
- **`prompts/`** *(à venir)* — prompts système en fichiers texte, séparés du code.

## Installation

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Créer un fichier `.env` à la racine avec ta clé API Groq :

```
GROQ_API_KEY=ta_cle_ici
```

## Corpus de test

Le corpus utilisé (`data/05_corpus_rag.csv`) est une base de faits inventés
(qui n'existent nulle part sur Internet) : si le système répond juste, c'est
forcément grâce au retrieval, pas à la mémoire du LLM.

## Tester le retrieval

```bash
python test_vector_db.py
```
