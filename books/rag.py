from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from .models import Book

from openai import OpenAI
import os


# 🔹 Create vector database
def create_vector_db():
    books = Book.objects.all()

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

    # ⚠️ If no books
    if not docs:
        return None

    try:
        embeddings = OpenAIEmbeddings(
            api_key=os.getenv("OPENAI_API_KEY")
        )

        db = FAISS.from_documents(docs, embeddings)
        return db

    except Exception:
        # 🔥 fallback if embeddings fail
        return None


# 🔹 Ask question (MAIN FUNCTION)
def ask_question(query):
    try:
        db = create_vector_db()

        if db is None:
            return f"""
📚 Demo Response

Recommended Book: Pride and Prejudice

💡 Reason:
A timeless romantic novel with strong characters.

🔍 Your query:
{query}
"""

        docs = db.similarity_search(query, k=3)
        context = "\n".join([doc.page_content for doc in docs])

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a smart book recommendation assistant."
                },
                {
                    "role": "user",
                    "content": f"""
Books data:
{context}

User question:
{query}

Give best recommendation with reason.
"""
                }
            ]
        )

        return response.choices[0].message.content

    except Exception:
        # 🔥 IMPORTANT: fallback if API quota error
        return f"""
⚠️ Demo Mode (API limit reached)

📚 Recommended Book:
Pride and Prejudice by Jane Austen

💡 Reason:
Classic romantic novel with deep emotional storytelling.

🔍 Your query:
{query}
"""