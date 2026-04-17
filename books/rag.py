from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_community.embeddings import HuggingFaceEmbeddings

from .models import Book

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()


# -------------------- CREATE VECTOR DB --------------------
def create_vector_db():
    books = Book.objects.all()

    if not books.exists():
        return None

    docs = []

    for book in books:
        content = f"""
Title: {book.title}
Author: {book.author}
Rating: {book.rating}
Description: {book.description}
Link: {book.url}
"""
        docs.append(Document(page_content=content))

    try:
        #  Better model (more accurate than default)
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        db = FAISS.from_documents(docs, embeddings)
        return db

    except Exception as e:
        print("❌ Embedding Error:", e)
        return None


# -------------------- FORMAT BOOKS (CLEAN OUTPUT) --------------------
def format_books(docs):
    result = ""

    for doc in docs:
        result += f"""
📖 Book

{doc.page_content.strip()}

-------------------------
"""

    return result


# -------------------- ASK QUESTION --------------------
def ask_question(query):
    try:
        db = create_vector_db()

        # ❌ No data case
        if db is None:
            return f"""
📚 No data found

👉 Please scrape books first using:
http://127.0.0.1:8000/scrape/

🔍 Your query:
{query}
"""

        docs = db.similarity_search(query, k=3)

        if not docs:
            return "❌ No relevant books found."

        context = "\n".join([doc.page_content for doc in docs])

        # -------------------- TRY OPENAI --------------------
        try:
            api_key = os.getenv("OPENAI_API_KEY")

            #  If no API key → skip OpenAI
            if not api_key:
                raise Exception("No API key found")

            client = OpenAI(api_key=api_key)

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful book recommendation assistant."
                    },
                    {
                        "role": "user",
                        "content": f"""
Books data:
{context}

User question:
{query}

Give the best recommendation with reason in clean format.
"""
                    }
                ]
            )

            return response.choices[0].message.content

        # -------------------- FALLBACK (NO API) --------------------
        except Exception as api_error:
            print("⚠️ OpenAI Error:", api_error)

            return f"""
⚠️ Demo Mode (No API)

📚 Recommended Books:

{format_books(docs)}

💡 Reason:
These books are selected based on semantic similarity to your query.

🔍 Your query:
{query}
"""

    except Exception as e:
        print("❌ RAG Error:", e)

        return f"""
❌ Something went wrong

Error:
{str(e)}

🔍 Your query:
{query}
"""