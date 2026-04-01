<img width="2133" height="752" alt="heroDesktopBgV2" src="https://github.com/user-attachments/assets/ba158d0f-79a3-4ad2-bfa9-97720b89cbe8" />

# Track 3 - Build and Migrate faster with AI-Ready Databases
# 📒 Bookstore AI - NL2SQL AI Assistant
A conversational AI assistant that lets anyone query a live bookstore database using plain English. Powered by **Gemini AI** for natural language understanding and **AlloyDB PostgreSQL** for data storage, it converts user questions into SQL, executes them, and returns friendly human-readable answers — all through a clean chat interface deployed on **Google Cloud Run**.

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/AlloyDB-PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Google Cloud](https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=googlecloud&logoColor=white)
![Cloud Run](https://img.shields.io/badge/Cloud_Run-Deployed-34A853?style=for-the-badge&logo=googlecloud&logoColor=white)
![Gemini AI](https://img.shields.io/badge/Gemini_AI-1.5_Flash-8E75B2?style=for-the-badge&logo=google&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white)

### Demo video link : https://www.youtube.com/watch?v=zyZZrFhhA20

---

## Problem Statement

Traditional database systems require users to know SQL to query data — a skill most end users simply don't have. This creates a barrier between business stakeholders and the data they need, forcing them to rely on developers or analysts to answer even basic questions.

> **The Challenge:** How can non-technical users query a live database using plain English — without writing a single line of SQL — while still getting accurate, real-time results from structured data?

This project answers that question by building an AI-enabled database feature using Google Cloud's AlloyDB for PostgreSQL, combined with Gemini AI, to create a natural language interface for a bookstore dataset.

---

## Project Outcome

A fully working, cloud-deployed web application where users type questions in plain English and receive meaningful answers sourced directly from a live AlloyDB PostgreSQL database — with no SQL knowledge required.

| ✅ What Was Built | 📊 Dataset Overview |
|---|---|
| AI-powered chat interface | 3 relational tables: books, authors, orders |
| Natural language → SQL conversion | 5 authors from 4 countries |
| Live AlloyDB query execution | 5 books across 4 genres |
| Human-friendly answer generation | Price range: ₹299 – ₹499 |
| Deployed on Google Cloud Run | Rating range: 4.6 – 4.8 out of 5 |
| Auto-generated SQL visible to user | Hosted on AlloyDB (PostgreSQL 16) |
| Results displayed as formatted table | Public IP with authorized access |

---

## How the Solution Works

The system combines three components — a FastAPI backend, Google's Gemini AI model, and an AlloyDB PostgreSQL database — into a seamless pipeline that transforms a plain English question into a real database result and a human-readable answer.

---
## Application Preview:

Cloud-run URL : https://bookstore-api-1059652519537.us-central1.run.app/

<img width="1920" height="912" alt="c7a53265-27af-49ea-ac96-92a1ef7cb468" src="https://github.com/user-attachments/assets/a7e6428e-c220-4446-b877-bf50ce3e4b97" />
-
<img width="1920" height="1389" alt="694a1e5a-a0b8-4116-a302-3431f19dd828" src="https://github.com/user-attachments/assets/b5d2571a-3529-4886-9f88-ced5ad25884a" />

---
### Architecture Flow

<img width="773" height="1013" alt="bookstore-flow drawio" src="https://github.com/user-attachments/assets/d8ae280a-5afd-413d-b7fc-8f7bd37e8d11" />

---
**Step by step:**

1. **User asks a question** — types in plain English, e.g. *"Which book has the highest rating?"*
2. **FastAPI receives the request** — the `/query` endpoint accepts the question as JSON and begins the pipeline
3. **Gemini generates SQL** — the question and full database schema are sent to Gemini 1.5 Flash, which returns a valid PostgreSQL SELECT query
4. **SQL executes on AlloyDB** — the generated SQL runs against the live database via psycopg2 and returns structured rows
5. **Gemini generates the answer** — raw results are sent back to Gemini, which produces a concise, friendly natural language response
6. **Response returned to user** — the API returns the question, generated SQL, raw results, and AI answer to the chat UI

---

## Tech Stack

| Technology | Role |
|---|---|
| **AlloyDB** | PostgreSQL-compatible managed database on Google Cloud — stores books, authors, and orders |
| **FastAPI** | Python web framework — handles HTTP requests, orchestrates the NL-to-SQL pipeline, serves the chat UI |
| **Gemini 1.5 Flash** | Google's LLM — converts natural language to SQL and generates human-friendly answers |
| **psycopg2** | PostgreSQL adapter for Python — connects FastAPI to AlloyDB and executes generated SQL |
| **Cloud Run** | Serverless container platform — hosts the FastAPI app with a public HTTPS URL |
| **Cloud Shell** | GCP's browser-based terminal — used for development, testing, and deployment |
| **HTML / CSS / JS** | Single-page chat interface — parchment-themed with live SQL preview and results table |
| **python-dotenv** | Manages environment variables — keeps credentials out of source code |

---

## Database Schema

```sql
CREATE TABLE authors (
    id      SERIAL PRIMARY KEY,
    name    TEXT NOT NULL,
    country TEXT
);

CREATE TABLE books (
    id        SERIAL PRIMARY KEY,
    title     TEXT NOT NULL,
    author_id INT REFERENCES authors(id),
    genre     TEXT,
    price     NUMERIC(10,2),
    rating    NUMERIC(2,1),
    stock     INT
);

CREATE TABLE orders (
    id         SERIAL PRIMARY KEY,
    book_id    INT REFERENCES books(id),
    quantity   INT,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Sample data:**

| Title | Author | Genre | Price | Rating |
|---|---|---|---|---|
| Atomic Habits | James Clear (USA) | Self-help | ₹450 | 4.8 |
| Rich Dad Poor Dad | Robert Kiyosaki (USA) | Finance | ₹399 | 4.7 |
| The Alchemist | Paulo Coelho (Brazil) | Fiction | ₹299 | 4.6 |
| The Psychology of Money | Morgan Housel (USA) | Finance | ₹499 | 4.8 |
| 1984 | George Orwell (UK) | Dystopian | ₹350 | 4.7 |

---

## How to Run

### Prerequisites

- Google Cloud project with AlloyDB instance running
- AlloyDB public IP enabled with your IP in authorized networks
- Gemini API key from [aistudio.google.com](https://aistudio.google.com)
- Python 3.11+

---

### 1 — Project Structure

```
bookstore-api/
├── main.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .env
└── static/
    └── index.html
```

---

### 2 — Configure Environment

Create a `.env` file:

```env
DB_HOST=<your-alloydb-public-ip>
DB_PORT=5432
DB_NAME=book
DB_USER=postgres
DB_PASSWORD=<your-password>
GEMINI_API_KEY=<your-gemini-api-key>
GCP_PROJECT_ID=<your-gcp-project-id>
```

---

### 3 — Install & Run Locally

```bash
pip install -r requirements.txt

uvicorn main:app --host 0.0.0.0 --port 8080 --reload

# Open: http://localhost:8080
```

---

### 4 — Deploy to Cloud Run

```bash
# Enable required APIs
gcloud services enable run.googleapis.com \
  artifactregistry.googleapis.com \
  cloudbuild.googleapis.com

# Deploy
gcloud run deploy bookstore-api \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080 \
  --set-env-vars="DB_HOST=<ip>,DB_PORT=5432,DB_NAME=book,DB_USER=postgres,DB_PASSWORD=<pwd>,GEMINI_API_KEY=<key>" \
  --memory 512Mi \
  --cpu 1

# You will receive a public URL:
# https://bookstore-api-xxxx-uc.a.run.app
```

---

### 5 — API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Serves the chat UI (index.html) |
| `GET` | `/health` | Database connectivity check + book count |
| `POST` | `/query` | Accepts `{question}` → returns SQL, results, and AI answer |

**Example request:**
```bash
curl -X POST http://localhost:8080/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Which book has the highest rating?"}'
```

**Example response:**
```json
{
  "question": "Which book has the highest rating?",
  "sql": "SELECT title, rating FROM books ORDER BY rating DESC LIMIT 1",
  "results": [{"title": "Atomic Habits", "rating": 4.8}],
  "answer": "Atomic Habits by James Clear has the highest rating of 4.8 out of 5!"
}
```

---

## Example Queries

| Natural Language Question | Generated SQL |
|---|---|
| Which book has the highest rating? | `SELECT title, rating FROM books ORDER BY rating DESC LIMIT 1` |
| Show me all finance books | `SELECT title, price FROM books WHERE genre = 'Finance'` |
| Which author is from Brazil? | `SELECT name FROM authors WHERE country = 'Brazil'` |
| Books under ₹400 | `SELECT title, price FROM books WHERE price < 400` |
| Show all books with their authors | `SELECT b.title, a.name FROM books b JOIN authors a ON b.author_id = a.id` |
| What orders have been placed? | `SELECT o.id, b.title, o.quantity FROM orders o JOIN books b ON o.book_id = b.id` |
| Most expensive book? | `SELECT title, price FROM books ORDER BY price DESC LIMIT 1` |
| How many books are in stock? | `SELECT title, stock FROM books ORDER BY stock DESC` |

---

## Future Improvements

### Short Term
- **SQL Validation Layer** — retry with a corrected prompt if Gemini returns invalid SQL
- **Conversation History** — maintain context across multiple questions in a session
- **Streaming Responses** — stream Gemini output token-by-token for faster perceived response
- **Query Caching** — cache frequent questions to reduce API calls and latency
- **Input Sanitization** — validate all generated queries before execution to prevent issues

### Medium Term
- **alloydb_ai_nl Integration** — migrate to native AlloyDB NL-to-SQL once the extension reaches GA
- **Authentication** — add Google OAuth or API key auth to secure the `/query` endpoint
- **Larger Dataset** — expand to thousands of books with reviews, categories, and inventory history
- **Voice Input** — add speech-to-text so users can ask questions by speaking
- **Multi-language Support** — handle questions in Tamil, Hindi, and other regional languages

### Long Term
- **AlloyDB Vector Search** — use pgvector for semantic book recommendations alongside NL queries
- **Analytics Dashboard** — charts showing sales trends, popular genres, and stock levels
- **Multi-tenant SaaS** — allow different bookstores to connect their own AlloyDB databases
- **Fine-tuned SQL Model** — fine-tune a smaller model on the bookstore schema for cheaper inference
- **Mobile App** — React Native frontend connecting to the same Cloud Run API

---

*Built with ❤️ on Google Cloud — AlloyDB · Gemini AI · FastAPI · Cloud Run*
