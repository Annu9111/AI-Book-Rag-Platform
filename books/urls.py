from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.get_books),
    path('books/<int:id>/', views.get_book),
    path('books/add/', views.add_book),
    path('scrape/', views.scrape_books_api),
    path('ask/', views.ask_books),
]