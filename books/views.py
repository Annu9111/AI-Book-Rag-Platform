from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Book
from .serializers import BookSerializer
from .scraper import scrape_books


# GET all books
@api_view(['GET'])
def get_books(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)


# GET single book
@api_view(['GET'])
def get_book(request, id):
    try:
        book = Book.objects.get(id=id)
        serializer = BookSerializer(book)
        return Response(serializer.data)
    except Book.DoesNotExist:
        return Response({"error": "Book not found"}, status=404)


# SCRAPE BOOKS (IMPORTANT)
@api_view(['GET'])
def scrape_books_api(request):
    books_data = scrape_books()

    created_books = []

    for book in books_data:
        serializer = BookSerializer(data=book)
        if serializer.is_valid():
            serializer.save()
            created_books.append(serializer.data)

    return Response({
        "message": "Books scraped and saved successfully!",
        "total_added": len(created_books)
    })


# ADD BOOK (POST API)
@api_view(['POST'])
def add_book(request):
    serializer = BookSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)

from .rag import ask_question

@api_view(['POST'])
def ask_books(request):
    query = request.data.get("query")

    if not query:
        return Response({"error": "Query is required"})

    answer = ask_question(query)

    return Response({"answer": answer})