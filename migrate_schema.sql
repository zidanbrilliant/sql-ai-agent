BEGIN TRANSACTION;

-- 1️⃣ Buat tabel baru dengan schema rapi
CREATE TABLE ecommerce_new (
    user_id TEXT,
    product_id TEXT,
    category TEXT,
    price REAL,
    discount_percent INTEGER,
    final_price REAL,
    payment_method TEXT,
    purchase_date TEXT
);

-- 2️⃣ Copy data dari tabel lama
INSERT INTO ecommerce_new (
    user_id,
    product_id,
    category,
    price,
    discount_percent,
    final_price,
    payment_method,
    purchase_date
)
SELECT
    "User_ID",
    "Product_ID",
    "Category",
    "Price (Rs.)",
    "Discount (%)",
    "Final_Price(Rs.)",
    "Payment_Method",
    "Purchase_Date"
FROM ecommerce;

-- 3️⃣ Hapus tabel lama
DROP TABLE ecommerce;

-- 4️⃣ Rename tabel baru
ALTER TABLE ecommerce_new RENAME TO ecommerce;

COMMIT;
