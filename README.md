# SQL AI Agent 🤖

SQL AI Agent adalah aplikasi berbasis Python yang memungkinkan pengguna mengajukan pertanyaan dalam **bahasa alami (Natural Language)** dan secara otomatis mengubahnya menjadi **query SQL yang valid** untuk database **SQLite** menggunakan **Large Language Model (LLM)**.

Project ini dirancang sebagai:
- Eksplorasi *Natural Language to SQL*
- AI assistant untuk analisis data
- Fondasi sistem *AI-powered data querying*

---

## ✨ Fitur Utama
- Konversi bahasa alami ke SQL menggunakan LLM (Groq)
- Menampilkan kueri SQL yang dihasilkan di UI
- Menjalankan kueri dan menampilkan hasilnya dalam tabel

---

## 🧠 Cara Kerja Singkat
1. User memasukkan pertanyaan bahasa alami
2. Agent membaca schema database aktual
3. LLM menghasilkan query SQL sesuai schema
4. Query divalidasi & dieksekusi ke SQLite
5. Hasil dikembalikan sebagai DataFrame


## 🛠️ Tech Stack
- Python 3.9+
- SQLite
- LangChain
- GROQ LLM (LLaMA 3.1)
- SQLAlchemy
- Pandas

---

## ⚙️ Instalasi

1️⃣ Clone Repository

bash
git clone https://github.com/username/sql-ai-agent.git
cd sql-ai-agent

2️⃣ Buat & Aktifkan Virtual Environment
python -m venv venv

Windows:
venv\Scripts\activate

Linux / Mac:
source venv/bin/activate

3️⃣ Install Dependency
pip install -r requirements.txt

🗄️ Database & Schema
Project ini menggunakan SQLite.

⚠️ File database (.db) tidak disertakan di repository
Silakan buat database sendiri menggunakan schema berikut.

Contoh Schema
sql
Copy code
CREATE TABLE ecommerce (
  user_id TEXT,
  product_id TEXT,
  category TEXT,
  price REAL,
  discount_percent INTEGER,
  final_price REAL,
  payment_method TEXT,
  purchase_date TEXT
);

Schema resmi tersedia di:
migrate_schema.sql

🔄 Migrasi Schema (Opsional)
Masuk ke SQLite shell:
sqlite3 data/ecommerce.db

Lalu jalankan:
.read migrate_schema.sql

Keluar:
.exit

▶️ Menjalankan Aplikasi
python main.py

Contoh pertanyaan:
Berapa total penjualan?
Apa product_id dengan penjualan tertinggi?
Berapa rata-rata harga setelah diskon?

⚠️ Aturan & Batasan
Hanya mendukung SQLite
Saat ini optimal untuk single table
Nama kolom harus sesuai schema
LLM hanya boleh menggunakan tabel & kolom yang tersedia
Query kompleks multi-join belum dioptimalkan

👨‍💻 Author
SQL AI Agent
Dibuat sebagai project eksplorasi AI untuk Data Engineering & Analytics.
