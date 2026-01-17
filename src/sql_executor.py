from sqlalchemy import text
import pandas as pd


def execute_sql(sql: str, db):
    """
    Execute raw SQL safely and return columns & rows
    """
    engine = db._engine

    with engine.connect() as conn:
        result = conn.execute(text(sql))
        rows = result.fetchall()
        columns = result.keys()

    return list(columns), [list(row) for row in rows]
