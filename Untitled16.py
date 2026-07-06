#!/usr/bin/env python
# coding: utf-8

# In[2]:


"""
Amazon Product & Review Data Loader
Reads CSV → Cleans with Pandas/NumPy → Loads into MySQL
"""
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text

# ---------- CONFIGURATION (CHANGE THESE) ----------
CSV_FILE = "C:/Users/This PC/Desktop/My First Project/amazon.csv"        # fILE PATH
MYSQL_PASSWORD = "Khan54321"     # MY_PASSW0RD
# -------------------------------------------------

# 1. READ CSV
print("Reading CSV file...")
df = pd.read_csv(CSV_FILE)

# Standardize column names: lowercase, replace spaces with underscores
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
print(f"Columns found: {df.columns.tolist()}")

# 2. SEPARATE PRODUCTS & REVIEWS
# Products: unique product_id, keep relevant columns
product_cols = [
    'product_id', 'product_name', 'category', 'actual_price',
    'discounted_price', 'discount_percentage', 'rating',
    'rating_count', 'about_product'
]
# Keep only columns that actually exist in the CSV
product_cols_exist = [col for col in product_cols if col in df.columns]
products_df = df[product_cols_exist].drop_duplicates(subset='product_id')

# Reviews: unique review_id
review_cols = [
    'review_id', 'product_id', 'user_id', 'user_name',
    'review_title', 'review_content', 'rating'
]
review_cols_exist = [col for col in review_cols if col in df.columns]
reviews_df = df[review_cols_exist].drop_duplicates(subset='review_id')
reviews_df = reviews_df.dropna(subset=['review_id', 'product_id'])

# 3. CLEAN DATA
# Price cleaner: remove ₹ symbol and commas, then convert to float
def clean_price(val):
    if isinstance(val, str):
        val = val.replace('₹', '').replace(',', '')
    try:
        return float(val)
    except (ValueError, TypeError):
        return np.nan

if 'actual_price' in products_df.columns:
    products_df['actual_price'] = products_df['actual_price'].apply(clean_price)
if 'discounted_price' in products_df.columns:
    products_df['discounted_price'] = products_df['discounted_price'].apply(clean_price)

# Discount percentage: remove '%' and convert to float
if 'discount_percentage' in products_df.columns:
    products_df['discount_percentage'] = (
        products_df['discount_percentage']
        .astype(str)
        .str.replace('%', '')
        .astype(float)
    )

# Ratings: convert to numeric
if 'rating' in products_df.columns:
    products_df['rating'] = pd.to_numeric(products_df['rating'], errors='coerce')
if 'rating_count' in products_df.columns:
    products_df['rating_count'] = pd.to_numeric(products_df['rating_count'], errors='coerce').fillna(0).astype(int)
if 'rating' in reviews_df.columns:
    reviews_df['rating'] = pd.to_numeric(reviews_df['rating'], errors='coerce')

print(f"Products to load: {len(products_df)}")
print(f"Reviews to load: {len(reviews_df)}")

# 4. CONNECT TO MYSQL (SSL DISABLED)
print("Connecting to MySQL...")
try:
    engine = create_engine(
        f"mysql+mysqlconnector://root:{MYSQL_PASSWORD}@localhost/amazon_products_db?ssl_disabled=true"
    )
    # Test connection
    with engine.connect() as test_conn:
        print("Connection successful.")
except Exception as e:
    print(f"Connection failed: {e}")
    print("Make sure MySQL is running and password is correct.")
    exit()

# 5. CREATE TABLES IF NOT EXIST
print("Creating tables (if not already present)...")
with engine.begin() as conn:   # begin() auto-commits
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS products (
            product_id VARCHAR(50) PRIMARY KEY,
            product_name TEXT,
            category VARCHAR(200),
            actual_price DECIMAL(10,2),
            discounted_price DECIMAL(10,2),
            discount_percentage DECIMAL(5,2),
            rating DECIMAL(3,1),
            rating_count INT,
            about_product TEXT
        )
    """))
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS reviews (
            review_id VARCHAR(50) PRIMARY KEY,
            product_id VARCHAR(50),
            user_id VARCHAR(50),
            user_name VARCHAR(200),
            review_title TEXT,
            review_content TEXT,
            rating DECIMAL(3,1)
        )
    """))
print("Tables ready.")

# 6. LOAD DATA INTO MYSQL
print("Loading products...")
products_df.to_sql('products', engine, if_exists='replace', index=False)
print("Loading reviews...")
reviews_df.to_sql('reviews', engine, if_exists='replace', index=False)

# 7. VERIFICATION
with engine.connect() as verify_conn:
    prod_count = verify_conn.execute(text("SELECT COUNT(*) FROM products")).scalar()
    rev_count = verify_conn.execute(text("SELECT COUNT(*) FROM reviews")).scalar()
    print(f"Verification: Products = {prod_count}, Reviews = {rev_count}")

print("✅ Data successfully loaded into MySQL!")


# In[ ]:




