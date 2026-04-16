from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from .models import Book

from openai import OpenAI


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

    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(docs, embeddings)

    return db


# 🔹 Ask question (MAIN AI FUNCTION)
def ask_question(query):
    db = create_vector_db()

    docs = db.similarity_search(query, k=3)

    context = "\n".join([doc.page_content for doc in docs])

    client = OpenAI()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a smart book recommendation assistant. "
                    "Always recommend books with reason."
                )
            },
            {
                "role": "user",
                "content": f"""
Books data:
{context}

User question:
{query}

Answer clearly and naturally.
"""
            }
        ]
    )

    return response.choices[0].message.content