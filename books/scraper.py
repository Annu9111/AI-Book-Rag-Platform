import requests
from bs4 import BeautifulSoup

def scrape_books():
    url = "http://books.toscrape.com/"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    books = []

    articles = soup.find_all("article", class_="product_pod")

    for book in articles:
        title = book.h3.a["title"]

        price = book.find("p", class_="price_color").text
        rating = book.p["class"][1]  # e.g. "Three", "Four"

        books.append({
            "title": title,
            "author": "Unknown",
            "rating": 4.0,  # dummy numeric rating
            "description": f"Price: {price}, Rating: {rating}",
            "url": url
        })

    return books