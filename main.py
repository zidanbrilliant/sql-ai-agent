from src.agent_logic import get_sql_executor

sql_executor = get_sql_executor()

print("🤖 SQL AI siap digunakan!")

while True:
    question = input("\nMasukkan pertanyaan (atau ketik 'exit'): ")

    if question.lower() == "exit":
        break

    output = sql_executor(question)

    print("\n📊 Output:")
    print(output)