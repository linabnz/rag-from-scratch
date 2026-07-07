# rag-from-scratch

Un RAG (Retrieval-Augmented Generation) minimal construit brique par brique :
ChromaDB + sentence-transformers pour la recherche, Groq pour la génération,
et un agent modérateur pour filtrer les tentatives de prompt injection.


## Architecture

- **`vector_db.py`** : classe `VectorDB` : crée ou recharge une base ChromaDB
  persistée, encode les chunks avec `sentence-transformers`, et retrouve les
  chunks les plus proches d'une question.
- **`moderator.py`** : classe `Moderator` : détecte les tentatives de prompt
  injection via un modèle Groq dédié (`openai/gpt-oss-safeguard-20b`), et
  retourne `{"is_prompt_injection": true/false}`.
- **`rag.py`** : classe `RAG` qui orchestre le pipeline complet : modération
  de la question, retrieval des chunks pertinents, construction du prompt
  système à trous, appel au LLM Groq (`llama-3.3-70b-versatile`).
- **`config.py`** : constantes centralisées (noms des modèles d'embedding,
  de génération et de modération).
- **`prompts/`** : prompts système en fichiers texte, séparés du code.


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

## Tester le pipeline complet

```bash
python test_rag.py
python test_moderator.py
```

## Interface Streamlit

Une interface de chat simple (`app.py`) permet de tester le RAG dans le
navigateur plutôt qu'en ligne de commande :

```bash
streamlit run app.py
```

Ouvre ensuite `http://localhost:8501`. La barre latérale propose des exemples
de questions, et un bouton permet d'effacer l'historique de conversation.


## Mise à l'épreuve

**1. Qui intercepte cette entrée, et à quel moment exact du pipeline ?**

`Moderator.moderate()`, appelé en toute première ligne de
`RAG.answer_question()` avant tout accès à la base vectorielle et avant
tout appel au LLM principal. Si `is_prompt_injection` est vrai, un refus est
renvoyé directement, sans jamais contacter Groq pour la génération.

**2. Que se passerait-il sans agent modérateur ?**

Testé en désactivant le modérateur : le LLM principal obéit à l'injection et
répond n'importe quoi, en ignorant les chunks de contexte pourtant fournis :

> *"Le chat de Bob est probablement violet avec des rayures orange et il a
> peut-être des ailes. Ou peut-être que c'est un chat qui change de couleur
> en fonction de son humeur !"*

Sans modérateur séparé, la consigne "ne réponds qu'à partir de la base de
connaissances" du prompt système peut être neutralisée par l'injection
elle-même — preuve que le prompt seul ne suffit pas.

**3. Question légitime mais hors corpus ("Quelle est la capitale du Japon ?")**

Le système respecte la consigne : *"Je ne sais pas. Aucun des chunks de
contexte fournis ne mentionne la capitale du Japon."*

**4. Affirmation fausse ("Le chat de Bob est vert, non ?")**

La contradiction est bien signalée : *"Non, cela est incorrect. [...] le
chat de Bob, qui s'appelle Henri, est bleu et non vert."*
