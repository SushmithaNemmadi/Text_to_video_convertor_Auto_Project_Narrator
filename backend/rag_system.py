import json
import os
from datetime import datetime
import torch

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings

from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain_community.llms import HuggingFacePipeline


# ==============================
# SETTINGS
# ==============================

DATA_PATH = "project_knowledge.json"
VECTOR_DB_PATH = "project_vector_db"
OUTPUT_LOG_FILE = "rag_output.txt"

SIMILARITY_THRESHOLD = 0.4


# ==============================
# LOAD PROJECT DATA
# ==============================

def load_projects():
    print("Loading project dataset...")

    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"{DATA_PATH} not found")

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    documents = []

    for item in data:
        if item["documentation"] != "FAILED":
            documents.append(
                Document(
                    page_content=item["documentation"],
                    metadata={"title": item["title"]}
                )
            )

    print("Total valid documents:", len(documents))
    return documents


# ==============================
# SPLIT INTO CHUNKS
# ==============================

def create_chunks(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=200
    )
    return splitter.split_documents(documents)


# ==============================
# EMBEDDINGS
# ==============================

def get_embeddings():
    print("Loading embedding model...")
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


# ==============================
# VECTOR DB
# ==============================

def build_vector_db(chunks, embeddings):
    print("Creating FAISS vector database...")
    vector_db = FAISS.from_documents(chunks, embeddings)
    vector_db.save_local(VECTOR_DB_PATH)
    return vector_db


def load_vector_db(embeddings):
    print("Loading existing vector database...")
    return FAISS.load_local(
        VECTOR_DB_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )


# ==============================
# LOAD LLM (STABLE VERSION)
# ==============================

def load_llm():
    print("Loading HuggingFace LLM...")

    model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    device = 0 if torch.cuda.is_available() else -1

    pipe = pipeline(
        task="text-generation",
        model=model,
        tokenizer=tokenizer,
        device=device,
        max_new_tokens=512,
        do_sample=False,
        temperature=0.2
    )

    return HuggingFacePipeline(pipeline=pipe)


# ==============================
# ASK QUESTION (RAG)
# ==============================

def ask_question(query, vector_db, llm):

    print("Searching knowledge base...")

    docs = vector_db.similarity_search(query, k=5)

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    prompt = f"""
You are a software project documentation assistant.

Using the context below, generate structured output.

Context:
{context}

Question:
{query}

Return structured format:

Project Overview:
Objective:
Domain:
Software Requirements:
Hardware Requirements:
Workflow:
System Architecture:
Input:
Output:
Implementation Steps:
Benefits:
Future Scope:
"""

    return llm.invoke(prompt)


# ==============================
# SAVE OUTPUT
# ==============================

def save_output(query, answer):
    with open(OUTPUT_LOG_FILE, "w", encoding="utf-8") as f:
        f.write("=" * 60 + "\n")
        f.write(f"Time: {datetime.now()}\n\n")
        f.write(f"Question:\n{query}\n\n")
        f.write("Answer:\n")
        f.write(str(answer) + "\n")

    print("Output saved →", OUTPUT_LOG_FILE)


# ==============================
# MAIN
# ==============================

if __name__ == "__main__":

    print("\n===== PROJECT RAG SYSTEM =====\n")

    open(OUTPUT_LOG_FILE, "w").close()

    embeddings = get_embeddings()

    try:
        vector_db = load_vector_db(embeddings)
    except:
        documents = load_projects()
        chunks = create_chunks(documents)
        vector_db = build_vector_db(chunks, embeddings)

    llm = load_llm()

    query = input("Ask about any project: ")

    answer = ask_question(query, vector_db, llm)

    print("\nAnswer:\n", answer)

    save_output(query, answer)