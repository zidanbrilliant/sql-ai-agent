import pandas as pd
import sqlite3

def setup_db():
    # 1. Load CSV
    df = pd.read_csv("data/raw/ecommerce_dataset_updated.csv")

    # 🔍 Cek kolom (PENTING, tapi HARUS di dalam fungsi)
    print("Kolom dataset:")
    print(df.columns)

    # 2. Connect ke SQLite
    conn = sqlite3.connect("data/ecommerce.db")

    # 3. Simpan ke tabel SQL
    df.to_sql("ecommerce", conn, index=False, if_exists="replace")

    conn.close()
    print("✅ Database berhasil dibuat")

if __name__ == "__main__":
    setup_db()
