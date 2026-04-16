from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.docstore.document import Document
from .models import Book
import os

def create_vector_db():
    books = Book.objects.all()

    docs = []
    for book in books:
        content = f"{book.title} by {book.author}. Rating: {book.rating}. {book.description}"
        docs.append(Document(page_content=content))

    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(docs, embeddings)

    return db


def ask_question(query):
    db = create_vector_db()
    docs = db.similarity_search(query)

    context = "\n".join([doc.page_content for doc in docs])

    return f"Based on books data:\n{context}"