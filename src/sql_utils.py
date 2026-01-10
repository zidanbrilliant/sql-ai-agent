import re

def extract_sql(text: str) -> str:
    """
    Extract SQL query from LLM output.
    Handles markdown blocks and extra explanations.
    """

    if not text:
        return ""

    # 1. Ambil SQL dari ```sql ... ```
    match = re.search(r"```sql(.*?)```", text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()

    # 2. Ambil SQL dari ``` ... ```
    match = re.search(r"```(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()

    # 3. Fallback: cari SELECT ... ;
    match = re.search(
        r"(SELECT\s+.*?;)",
        text,
        re.DOTALL | re.IGNORECASE
    )
    if match:
        return match.group(1).strip()

    # 4. Kalau tidak ketemu apa-apa, balikin text asli (last resort)
    return text.strip()

def auto_quote_columns(sql: str, schema: dict) -> str:
    """
    Automatically wrap columns containing special characters with double quotes
    """
    for table, columns in schema.items():
        for col in columns:
            if any(c in col for c in ["(", ")", "%", ".", " "]):
                pattern = rf'(?<!")\b{re.escape(col)}\b(?!")'
                sql = re.sub(pattern, f'"{col}"', sql)
    return sql
