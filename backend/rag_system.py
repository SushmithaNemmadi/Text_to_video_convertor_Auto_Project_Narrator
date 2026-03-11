import json
import sys
import os
from datetime import datetime
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import Ollama
from langchain_core.documents import Document
from docx import Document as WordDocument

# IMPORTANT: prevent output buffering
sys.stdout.reconfigure(line_buffering=True)


DATA_PATH = "project_knowledge.json"
VECTOR_DB_PATH = "project_vector_db"
OLLAMA_MODEL = "llama3:8b"

OUTPUT_LOG_FILE = "rag_output.txt"
DOC_OUTPUT_FILE = "project_documentation.docx"

SIMILARITY_THRESHOLD = 0.4


def load_projects():

    print("Loading project dataset...", flush=True)

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

    print("Total valid documents:", len(documents), flush=True)

    return documents


def create_chunks(documents):

    print("Splitting documents into chunks...", flush=True)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(documents)

    print("Total chunks created:", len(chunks), flush=True)

    return chunks


def get_embeddings():

    print("Loading embedding model...", flush=True)

    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


def build_vector_db(chunks, embeddings):

    print("Creating FAISS vector database...", flush=True)

    vector_db = FAISS.from_documents(chunks, embeddings)

    vector_db.save_local(VECTOR_DB_PATH)

    print("Vector database saved!", flush=True)

    return vector_db


def load_vector_db(embeddings):

    print("Loading existing vector database...", flush=True)

    return FAISS.load_local(
        VECTOR_DB_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )


def load_llm():

    print("Loading Ollama model...", flush=True)

    try:
        return Ollama(model=OLLAMA_MODEL, base_url="http://localhost:11434")
    except Exception as e:
        print("Ollama not running:", e)
        sys.exit()


def ask_question(query, vector_db, llm):

    print("Searching knowledge base...", flush=True)

    docs = vector_db.similarity_search(query, k=10)

    context = "\n\n".join(
        [f"Project Title: {doc.metadata.get('title','')}\n{doc.page_content}"
         for doc in docs]
    )

    prompt = f"""
Generate complete software project documentation.

Project Topic:
{query}

Context:
{context}

Return structured output:

Project Title
Project Overview
Objective
Domain
Software Requirements
Hardware Requirements
Workflow
System Architecture
Input
Output
Implementation Steps
Benefits
Future Scope
"""

    return llm.invoke(prompt)


def save_output(query, answer):

    with open(OUTPUT_LOG_FILE, "w", encoding="utf-8") as f:

        f.write("=" * 60 + "\n")
        f.write(f"Time: {datetime.now()}\n\n")

        f.write("Question:\n")
        f.write(query + "\n\n")

        f.write("Answer:\n")
        f.write(str(answer) + "\n")

        f.write("=" * 60 + "\n")

    print("Output saved ->", OUTPUT_LOG_FILE, flush=True)


def save_output_doc(query, answer):

    doc = WordDocument()

    doc.add_heading("Software Project Documentation", level=0)

    doc.add_heading("Project Query", level=1)
    doc.add_paragraph(query)

    doc.add_heading("Generated Documentation", level=1)
    doc.add_paragraph(str(answer))

    doc.save(DOC_OUTPUT_FILE)

    print("Word document created:", DOC_OUTPUT_FILE, flush=True)


if __name__ == "__main__":

    print("\n===== PROJECT RAG SYSTEM =====\n", flush=True)

    embeddings = get_embeddings()

    try:

        vector_db = load_vector_db(embeddings)

        print("Using existing vector database", flush=True)

    except Exception:

        print("Building new vector database...\n", flush=True)

        documents = load_projects()

        chunks = create_chunks(documents)

        vector_db = build_vector_db(chunks, embeddings)

    llm = load_llm()

    print("RAG system ready\n", flush=True)

    query = sys.argv[1] if len(sys.argv) > 1 else ""

    answer = ask_question(query, vector_db, llm)

    print("\nAnswer:\n", answer, flush=True)

    save_output(query, answer)

    save_output_doc(query, answer)