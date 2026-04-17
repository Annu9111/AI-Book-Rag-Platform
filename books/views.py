from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import authentication_classes, permission_classes

from .models import Book
from .serializers import BookSerializer
from .scraper import scrape_books
from .rag import ask_question


# -------------------- HOME --------------------
def home(request):
    return render(request, "index.html")


# -------------------- GET ALL BOOKS --------------------
@api_view(['GET'])
def get_books(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)


# -------------------- GET SINGLE BOOK --------------------
@api_view(['GET'])
def get_book(request, id):
    try:
        book = Book.objects.get(id=id)
        serializer = BookSerializer(book)
        return Response(serializer.data)
    except Book.DoesNotExist:
        return Response({"error": "Book not found"}, status=404)


# -------------------- SCRAPE BOOKS --------------------
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


# -------------------- ADD BOOK --------------------
@api_view(['POST'])
@csrf_exempt
@authentication_classes([])   # IMPORTANT
@permission_classes([])       # IMPORTANT
def add_book(request):
    serializer = BookSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)


# -------------------- AI ASK (MAIN FEATURE) --------------------
@api_view(['POST'])
@csrf_exempt
@authentication_classes([])   
@permission_classes([])       
def ask_books(request):
    query = request.data.get("query")

    if not query:
        return Response(
            {"error": "Query is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        answer = ask_question(query)

        return Response({
            "answer": answer
        })

    except Exception as e:
        print("❌ ERROR:", str(e))   # shows error in terminal

        return Response({
            "error": "AI failed",
            "details": str(e)
        }, status=500)