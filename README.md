# 📚 AI Book RAG Platform

An AI-powered book recommendation system built using Django and Retrieval-Augmented Generation (RAG).

---

## 🚀 Features

* 📖 Scrape books from online sources
* 🔍 Store and manage books in database
* 🤖 AI-based book recommendation using RAG
* ⚡ Fast similarity search using FAISS
* 🎯 Clean UI with real-time responses

---

## 🛠️ Tech Stack

* Backend: Django, Django REST Framework
* AI: LangChain, FAISS, HuggingFace Embeddings
* Frontend: HTML, CSS, JavaScript
* Database: SQLite

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Annu9111/AI-Book-Rag-Platform.git
cd AI-Book-Rag-Platform
```

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run migrations

```bash
python manage.py migrate
```

### 5. Start server

```bash
python manage.py runserver
```

---

## 🌐 API Endpoints

| Endpoint   | Method | Description                |
| ---------- | ------ | -------------------------- |
| `/scrape/` | GET    | Scrape books               |
| `/books/`  | GET    | Get all books              |
| `/ask/`    | POST   | Ask AI for recommendations |

---

## 🧠 Sample Queries

* Recommend me a romantic book
* Suggest a mystery novel
* Best books for beginners
* Books similar to crime stories

---

## 📸 Screenshots

### UI

![UI](Screenshots/screenshot1.png)

### API

![API](Screenshots/screenshot2.png)

### Result

![Result](Screenshots/screenshot3.png)

---

## ⚠️ Notes

* If OpenAI API is not available, system runs in **Demo Mode**
* Uses similarity search to recommend books

