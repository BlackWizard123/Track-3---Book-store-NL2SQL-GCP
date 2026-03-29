from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import psycopg2
import psycopg2.extras
import vertexai
from vertexai.generative_models import GenerativeModel
import os
from dotenv import load_dotenv
import re
import google.generativeai as genai

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
# model = genai.GenerativeModel("gemma-3-12B")
# model = genai.GenerativeModel("gemma-3-12b-it")
model = genai.GenerativeModel("gemini-2.5-flash")

# Database connection
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

# Schema for Gemini context
SCHEMA = """
PostgreSQL database schema for a bookstore:
 
TABLE authors:
  - id SERIAL PRIMARY KEY
  - name TEXT (author's full name)
  - country TEXT (author's country)
 
TABLE books:
  - id SERIAL PRIMARY KEY
  - title TEXT (book title)
  - author_id INT (foreign key → authors.id)
  - genre TEXT (one of: Self-help, Finance, Fiction, Dystopian)
  - price NUMERIC (price in INR)
  - rating NUMERIC (rating out of 5.0)
  - stock INT (available stock count)
 
TABLE orders:
  - id SERIAL PRIMARY KEY
  - book_id INT (foreign key → books.id)
  - quantity INT (number of books ordered)
  - order_date TIMESTAMP (when order was placed)
 
Sample data:
- Books: Atomic Habits (Self-help, ₹450), Rich Dad Poor Dad (Finance, ₹399), The Alchemist (Fiction, ₹299), The Psychology of Money (Finance, ₹499), 1984 (Dystopian, ₹350)
- Authors: James Clear (USA), Robert Kiyosaki (USA), Paulo Coelho (Brazil), Morgan Housel (USA), George Orwell (UK)
"""

app = FastAPI(title="Bookstore NL-to-SQL API")

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    question: str
    sql: str
    results: list
    answer: str

def clean_sql(raw: str) -> str:
    """Clean model output to extract only the SQL query."""
    # Remove markdown code blocks
    raw = re.sub(r"```sql", "", raw, flags=re.IGNORECASE)
    raw = re.sub(r"```", "", raw)
    # Remove lines starting with -- (comments) that aren't part of SQL
    lines = raw.strip().split("\n")
    sql_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.upper().startswith(("SELECT", "WITH", "FROM", "WHERE", "JOIN", "GROUP", "ORDER", "HAVING", "LIMIT")):
            sql_lines.append(line)
        elif sql_lines:  # continuation of SQL
            sql_lines.append(line)
    sql = "\n".join(sql_lines).strip() if sql_lines else raw.strip()
    # Take only the first statement
    sql = sql.split(";")[0].strip()
    return sql

@app.get("/")
def root():
    return FileResponse("static/index.html")

@app.get("/health")
def health():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM books")
        count = cur.fetchone()[0]
        cur.close()
        conn.close()
        return {
            "status": "healthy",
            "database": "connected",
            "books_count": count
        }
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    question = request.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")
 
    # Step 1 — Generate SQL using Gemma via Vertex AI
    sql_prompt = f"""You are a PostgreSQL expert. Use this schema:
{SCHEMA}
 
Generate a valid PostgreSQL SELECT query for this question:
"{question}"
 
Rules:
- Return ONLY the raw SQL query
- No markdown, no backticks, no explanation, no comments
- Use JOINs when querying across tables
- Use correct column names from the schema above
SQL:"""
 
    try:
        sql_response = model.generate_content(sql_prompt)
        raw_sql = sql_response.text.strip()
        sql = clean_sql(raw_sql)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"SQL generation failed: {str(e)}")
 
    if not sql.upper().startswith("SELECT") and not sql.upper().startswith("WITH"):
        raise HTTPException(
            status_code=400,
            detail=f"Model did not return a valid SELECT query. Got: {sql}"
        )
 
    # Step 2 — Execute SQL on AlloyDB
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(sql)
        rows = cursor.fetchall()
        results = [dict(row) for row in rows]
        cursor.close()
        conn.close()
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"SQL execution failed: {str(e)} | Generated SQL: {sql}"
        )
 
    # Step 3 — Generate human-friendly answer using Gemma
    answer_prompt = f"""A user asked about a bookstore database: "{question}"
 
The query returned these results: {results}
 
Write a short, friendly, conversational answer based on the results.
Do not mention SQL, databases, or technical details.
Be concise — 1 to 3 sentences max.
Answer:"""
 
    try:
        answer_response = model.generate_content(answer_prompt)
        answer = answer_response.text.strip()
    except Exception as e:
        # Fallback: format results as readable text
        if results:
            answer = f"Found {len(results)} result(s): " + ", ".join(
                [str(list(r.values())[0]) if len(r) == 1 else str(dict(r)) for r in results[:5]]
            )
        else:
            answer = "No results found for your query."
 
    return QueryResponse(
        question=question,
        sql=sql,
        results=results,
        answer=answer
    )
 