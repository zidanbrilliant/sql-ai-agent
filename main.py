from src.agent_logic import get_sql_executor

sql_executor = get_sql_executor("data/ecommerce.db")

print("🤖 SQL AI siap digunakan!")

while True:
    q = input("\nMasukkan pertanyaan (atau ketik 'exit'): ")
    if q.lower() == "exit":
        break

    output = sql_executor(q)
    print("\n📊 Output:")
    print(output)
