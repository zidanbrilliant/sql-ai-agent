from groq import Groq
import os

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_sql(question: str, schema: dict) -> str:
    """
    Generate SQLite SQL query using Groq LLM
    """

    schema_text = ""
    for table, columns in schema.items():
        schema_text += f"Table {table}: {', '.join(columns)}\n"

    prompt = f"""
You are an expert data analyst.

Database schema:
{schema_text}

Rules:
- Generate ONLY valid SQLite SQL
- Do NOT explain
- Do NOT use markdown
- Return ONLY the SQL query

User question:
{question}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You generate SQL queries."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    sql = response.choices[0].message.content.strip()
    return sql
