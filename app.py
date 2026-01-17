from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse

from src.agent_logic import get_sql_executor

app = FastAPI(title="SQL AI Agent")

# =========================
# INIT AGENT (ONCE)
# =========================
run, run_with_sql = get_sql_executor("data/ecommerce.db")


# =========================
# REQUEST MODEL
# =========================
class QueryRequest(BaseModel):
    question: str


# =========================
# API ENDPOINT (JSON)
# =========================
@app.post("/query")
def query_db(req: QueryRequest):
    """
    Endpoint for UI / API
    Returns SQL + result
    """
    result = run_with_sql(req.question)

    return {
        "question": result["question"],
        "sql": result["sql"],
        "columns": result["columns"],
        "rows": result["rows"],
    }


# =========================
# UI ENDPOINT
# =========================
@app.get("/", response_class=HTMLResponse)
def home():
    with open("templates/ui.html", "r", encoding="utf-8") as f:
        return f.read()
