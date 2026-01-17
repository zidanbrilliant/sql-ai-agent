from langchain_community.utilities import SQLDatabase
from langchain_groq import ChatGroq
from sqlalchemy import text
import pandas as pd
from src.sql_utils import extract_sql, auto_quote_columns
from .sql_generator import generate_sql
from .sql_executor import execute_sql

# =========================
# SCHEMA LOADER
# =========================

def get_schema(db):
    engine = db._engine
    schema = {}

    with engine.connect() as conn:
        tables = conn.execute(text("""
            SELECT name FROM sqlite_master
            WHERE type='table'
            AND name NOT LIKE 'sqlite_%';
        """)).fetchall()

        for (table,) in tables:
            columns = conn.execute(
                text(f'PRAGMA table_info("{table}")')
            ).fetchall()

            schema[table] = [col[1] for col in columns]

    return schema


# =========================
# MAIN EXECUTOR
# =========================

def get_sql_executor(db_path: str):

    db = SQLDatabase.from_uri(f"sqlite:///{db_path}")
    schema = get_schema(db)

    print("📦 Tables found:", list(schema.keys()))
    print("🧱 Schema:", schema)

    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0
    )

    def run(question: str):

        prompt = f"""
You are a professional SQLite query generator.

DATABASE SCHEMA (ONLY SOURCE OF TRUTH):
{schema}

STRICT RULES:
- Use ONLY tables and columns listed in the schema
- Use SQLite-compatible syntax ONLY
- Always use explicit column names (no SELECT *)
- Always wrap column names using double quotes
- DO NOT invent tables or columns
- DO NOT use aliases unless necessary
- DO NOT use JOIN unless required by the question
- DO NOT use subqueries unless required
- NEVER use INSERT, UPDATE, DELETE, DROP, ALTER
- Output ONLY a single valid SQL query
- No explanation
- No markdown
- No extra text

Question:
{question}
"""

        # 1️⃣ Generate SQL
        sql = llm.invoke(prompt).content.strip()

        print("\n🧠 Generated SQL:")
        print(sql)

        # 2️⃣ Execute SQL
        result = db.run(sql)

        # 3️⃣ Normalize result
        if isinstance(result, list):
            return pd.DataFrame(result)
        if isinstance(result, tuple):
            return pd.DataFrame([result])
        return pd.DataFrame([[result]], columns=["result"])

    def run_with_sql(question: str) -> dict:
        raw_sql = generate_sql(question, schema)
        sql = auto_quote_columns(extract_sql(raw_sql), schema)
        columns, rows = execute_sql(sql, db)

        return {
            "question": question,
            "sql": sql,
            "columns": columns,
            "rows": rows
        }

    return run, run_with_sql
