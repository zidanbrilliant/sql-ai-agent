from langchain_community.utilities import SQLDatabase
from langchain_groq import ChatGroq
from src.sql_utils import extract_sql, auto_quote_columns
import pandas as pd
from sqlalchemy import text


# =========================
# DB SCHEMA UTILITIES
# =========================

def get_tables(db):
    engine = db._engine
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            AND name NOT LIKE 'sqlite_%';
        """))
        return [row[0] for row in result.fetchall()]


def get_table_columns(db, table_name):
    engine = db._engine
    with engine.connect() as conn:
        result = conn.execute(text(f'PRAGMA table_info("{table_name}");'))
        return [row[1] for row in result.fetchall()]


def get_schema(db):
    schema = {}
    for table in get_tables(db):
        schema[table] = get_table_columns(db, table)
    return schema


# =========================
# RESULT NORMALIZER
# =========================

def result_to_dataframe(result):
    """
    Normalize SQLDatabase.run() output to pandas DataFrame
    """
    if result is None:
        return pd.DataFrame()

    # scalar result (SUM, COUNT, AVG, etc.)
    if isinstance(result, (int, float, str)):
        return pd.DataFrame([[result]], columns=["result"])

    # single row
    if isinstance(result, tuple):
        return pd.DataFrame([result])

    # multiple rows
    if isinstance(result, list):
        return pd.DataFrame(result)

    # fallback
    return pd.DataFrame([result])


# =========================
# MAIN EXECUTOR
# =========================

def get_sql_executor(db_path: str):

    # 1️⃣ Connect DB
    db = SQLDatabase.from_uri(f"sqlite:///{db_path}")

    # 2️⃣ Load REAL schema
    tables = get_tables(db)
    schema = get_schema(db)

    print("📦 Tables found:", tables)
    print("🧱 Schema:", schema)

    # 3️⃣ LLM (Groq)
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0
    )

    def run(question: str):

        base_prompt = f"""
You are a senior SQLite expert.

DATABASE SCHEMA (REAL):
{schema}

Rules:
- Use ONLY tables and columns listed above
- Use SQLite syntax
- Wrap column names with special characters using double quotes
- DO NOT invent tables or columns
- DO NOT explain anything
- DO NOT use markdown
- Output ONLY a single valid SQL query
"""

        try:
            # 🔹 Generate SQL
            raw_sql = llm.invoke(
                f"{base_prompt}\nQUESTION: {question}"
            ).content.strip()

            print("\n🧠 Generated SQL:")
            print(raw_sql)

            clean_sql = extract_sql(raw_sql)
            clean_sql = auto_quote_columns(clean_sql, schema)


            print("\n🧹 Cleaned SQL:")
            print(clean_sql)

            # 🔒 Safety check
            if not any(t.lower() in clean_sql.lower() for t in tables):
                return "❌ SQL tidak menggunakan tabel yang valid."

            result = db.run(clean_sql)
            return result_to_dataframe(result)

        except Exception as e:
            print("⚠️ SQL Error detected, retrying...")

            retry_prompt = f"""
The SQL query below is INVALID:

{clean_sql}

Error:
{e}

DATABASE SCHEMA:
{schema}

Rules:
- FIX the SQL
- DO NOT change table names
- DO NOT invent columns
- Output ONLY corrected SQL
"""

            fixed_raw = llm.invoke(
                f"{retry_prompt}\nQUESTION: {question}"
            ).content.strip()

            fixed_sql = extract_sql(fixed_raw)
            fixed_sql = auto_quote_columns(fixed_sql, schema)

            print("\n🔧 Fixed SQL:")
            print(fixed_sql)

            result = db.run(fixed_sql)
            return result_to_dataframe(result)

    return run
