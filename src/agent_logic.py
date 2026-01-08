from langchain_community.utilities import SQLDatabase
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

def normalize_question(question: str) -> str:
    replacements = {
        "final price": "Final_Price(Rs.)",
        "final_price": "Final_Price(Rs.)",
        "harga akhir": "Final_Price(Rs.)",
        "total penjualan": "SUM(Final_Price(Rs.))",
    }

    q = question.lower()
    for k, v in replacements.items():
        q = q.replace(k, v)

    return q

def get_sql_executor():
    # 1. Connect DB
    db = SQLDatabase.from_uri("sqlite:///data/ecommerce.db")

    # 2. LLM
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0
    )

    # 3. Prompt SQL generator
    prompt = PromptTemplate(
        input_variables=["question"],
        template="""
You are a senior SQL expert.

Database:
- Table name: ecommerce
- Columns:
  User_ID
  Product_ID
  Category
  Price (Rs.)
  Discount (%)
  Final_Price(Rs.)
  Payment_Method
  Purchase_Date

Rules:
- Use SQLite syntax
- ALWAYS wrap column names with special characters in double quotes
- DO NOT explain anything
- Output ONLY valid SQL

Question:
{question}

SQL:
"""
    )

    def run(question: str):
        try:
            question = normalize_question(question)

            sql = llm.invoke(
                f"""
                Given this question:
                {question}

                Generate a valid SQLite SQL query.
                Use EXACT column names.
                Table name is ecommerce.
                """
            ).content.strip()

            print("\n📄 SQL yang dijalankan:")
            print(sql)

            result = db.run(sql)
            return result

        except Exception as e:
            return f"⚠️ Query gagal dijalankan, kemungkinan karena nama kolom.\nDetail error: {e}"
    return run
