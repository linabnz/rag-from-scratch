import csv

import streamlit as st

from rag import RAG

st.set_page_config(page_title="Mon premier RAG", page_icon="🐾", layout="centered")

st.markdown(
    """
    <style>
    .stChatMessage { border-radius: 12px; }
    div[data-testid="stChatMessageContent"] { font-size: 0.95rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🐾 Mon premier RAG")
st.caption(
    "Pose une question sur le corpus d'histoires absurdes "
    "(les animaux de Bob, Alice, Carla, Diego, Karim...)."
)

with st.sidebar:
    st.header("À propos")
    st.markdown(
        "Ce RAG s'appuie **uniquement** sur un corpus de faits inventés : "
        "s'il répond juste, c'est grâce au retrieval, pas à sa mémoire."
    )
    st.divider()
    st.subheader("Exemples de questions")
    st.markdown(
        "- Quelle est la couleur du chat de Bob ?\n"
        "- Comment s'appelle le chien vert d'Alice ?\n"
        "- Que collectionne la tortue de Carla ?\n"
        "- Quelle est la capitale du Japon ? *(hors corpus)*"
    )
    st.divider()
    if st.button("🗑️ Effacer la conversation"):
        st.session_state.messages = []
        st.rerun()


@st.cache_resource
def load_rag():
    with open("data/05_corpus_rag.csv", encoding="utf-8") as f:
        chunks = [row["text"] for row in csv.DictReader(f)]
    return RAG(persist_path="./chroma_data", chunks=chunks)


with st.spinner("Chargement du modèle et de la base vectorielle..."):
    rag = load_rag()

if "messages" not in st.session_state:
    st.session_state.messages = []

AVATARS = {"user": "🧑", "assistant": "🐾"}

for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=AVATARS[message["role"]]):
        st.markdown(message["content"])

question = st.chat_input("Pose ta question ici...")
if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user", avatar=AVATARS["user"]):
        st.markdown(question)

    with st.chat_message("assistant", avatar=AVATARS["assistant"]):
        with st.spinner("Recherche en cours..."):
            answer = rag.answer_question(question)
        st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
