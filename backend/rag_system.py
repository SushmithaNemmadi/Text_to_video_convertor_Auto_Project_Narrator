import json
import os
from datetime import datetime
import torch

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

# Updated embeddings package
from langchain_huggingface import HuggingFaceEmbeddings

# HuggingFace LLM
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from langchain_community.llms import HuggingFacePipeline


# ==============================
# SETTINGS
# ==============================

DATA_PATH = "project_knowledge.json"
VECTOR_DB_PATH = "project_vector_db"
OUTPUT_LOG_FILE = "rag_output.txt"

SIMILARITY_THRESHOLD = 0.4


# ==============================
# STEP 1 — Load JSON Dataset
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
# STEP 2 — Split into Chunks
# ==============================

def create_chunks(documents):
    print("Splitting documents into chunks...")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(documents)

    print("Total chunks created:", len(chunks))
    return chunks


# ==============================
# STEP 3 — Create Embeddings
# ==============================

def get_embeddings():
    print("Loading embedding model...")

    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


# ==============================
# STEP 4 — Build Vector Database
# ==============================

def build_vector_db(chunks, embeddings):
    print("Creating FAISS vector database...")

    vector_db = FAISS.from_documents(chunks, embeddings)
    vector_db.save_local(VECTOR_DB_PATH)

    print("Vector database saved!")
    return vector_db


# ==============================
# STEP 5 — Load Vector DB
# ==============================

def load_vector_db(embeddings):
    print("Loading existing vector database...")

    return FAISS.load_local(
        VECTOR_DB_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )


# ==============================
# STEP 6 — Load HuggingFace LLM (FINAL FIXED VERSION)
# ==============================

def load_llm():
    print("Loading HuggingFace LLM...")

    model_name = "google/flan-t5-base"

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    device = 0 if torch.cuda.is_available() else -1

    pipe = pipeline(
        task="text2text-generation",
        model=model,
        tokenizer=tokenizer,
        device=device,
        max_new_tokens=512,
        do_sample=False
    )

    return HuggingFacePipeline(pipeline=pipe)


# ==============================
# STEP 7 — Ask Question (HYBRID RAG)
# ==============================

def ask_question(query, vector_db, llm):

    print("Searching knowledge base...")

    # 1️⃣ Exact Match
    docs = vector_db.similarity_search(query, k=10)

    for doc in docs:
        title = doc.metadata.get("title", "").lower()
        if query.lower() in title:
            print("Exact project title match found")

            context = f"Project Title: {doc.metadata['title']}\n{doc.page_content}"

            prompt = f"""
Use ONLY the context below.

Return structured output:

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

Context:
{context}
"""

            return llm.invoke(prompt)

    # 2️⃣ Semantic Match
    docs_with_scores = vector_db.similarity_search_with_score(query, k=3)

    if docs_with_scores:
        best_score = docs_with_scores[0][1]
        print("Best similarity score:", best_score)

        if best_score < SIMILARITY_THRESHOLD:
            print("Similar project found")

            context = "\n\n".join([
                f"Project Title: {doc.metadata.get('title','')}\n{doc.page_content}"
                for doc, _ in docs_with_scores
            ])

            prompt = f"""
Extract structured project details:

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

Context:
{context}
"""

            return llm.invoke(prompt)

    # 3️⃣ No Match
    print("Project not found → generating new info")

    prompt = f"""
Generate complete software project documentation for:

{query}

Return:

Project Title:
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