-- Rename columns to SQL & AI-friendly names

ALTER TABLE ecommerce RENAME COLUMN "User_ID" TO user_id;
ALTER TABLE ecommerce RENAME COLUMN "Product_ID" TO product_id;
ALTER TABLE ecommerce RENAME COLUMN "Category" TO category;

ALTER TABLE ecommerce RENAME COLUMN "Price (Rs.)" TO price;
ALTER TABLE ecommerce RENAME COLUMN "Discount (%)" TO discount_percent;
ALTER TABLE ecommerce RENAME COLUMN "Final_Price(Rs.)" TO final_price;

ALTER TABLE ecommerce RENAME COLUMN "Payment_Method" TO payment_method;
ALTER TABLE ecommerce RENAME COLUMN "Purchase_Date" TO purchase_date;
