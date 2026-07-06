select * from amazon_products_db.products;
select * from amazon_products_db.reviews;
SELECT product_name, category, rating, rating_count, discounted_price
from amazon_products_db.products
where rating_count > 50
order by rating desc
limit 10;
select category,
      round(avg(rating),2)as avg_rating,
      count(*) as total_products
 from amazon_products_db.products
 group by category
 order by avg_rating desc;
 
 SELECT 
    CASE 
        WHEN discount_percentage >= 50 THEN 'Heavy Discount (50%+)'
        WHEN discount_percentage >= 30 THEN 'Medium Discount (30-50%)'
        WHEN discount_percentage > 0  THEN 'Low Discount (0-30%)'
        ELSE 'No Discount'
    END AS discount_band,
    ROUND(AVG(rating), 2) AS avg_rating,
    COUNT(*) AS product_count
FROM amazon_products_db.products
GROUP BY discount_band
ORDER BY avg_rating DESC;
 
 SELECT user_name, COUNT(*) AS reviews_written,
       ROUND(AVG(rating), 2) AS avg_rating_given
FROM amazon_products_db.reviews
GROUP BY user_name
ORDER BY reviews_written DESC
LIMIT 10;


SELECT p.product_name,
       p.rating AS product_rating,
       ROUND(AVG(r.rating), 2) AS avg_review_rating,
       COUNT(r.review_id) AS review_count
FROM amazon_products_db.products p
JOIN amazon_products_db.reviews r ON p.product_id = r.product_id
GROUP BY p.product_id, p.product_name, p.rating
HAVING review_count >= 0 AND p.rating > AVG(r.rating)
ORDER BY (p.rating - AVG(r.rating)) DESC
limit 10;



SELECT 
    CASE 
        WHEN rating = 5 THEN '5 Stars'
        WHEN rating >= 4 THEN '4 Stars'
        WHEN rating >= 3 THEN '3 Stars'
        WHEN rating >= 2 THEN '2 Stars'
        ELSE '1 Star'
    END AS rating_bucket,
    COUNT(*) AS total_reviews
FROM amazon_products_db.reviews
GROUP BY rating_bucket
ORDER BY rating_bucket DESC;



SELECT p.product_name, 
       COUNT(r.review_id) AS review_count,
       ROUND(AVG(r.rating), 2) AS avg_review_rating
FROM amazon_products_db.products p
JOIN amazon_products_db.reviews r ON p.product_id = r.product_id
GROUP BY p.product_id, p.product_name
ORDER BY review_count DESC
LIMIT 10;



SELECT p.category,
       COUNT(r.review_id) AS total_reviews,
       ROUND(AVG(r.rating), 2) AS avg_review_rating
FROM amazon_products_db.products p
JOIN amazon_products_db.reviews r ON p.product_id = r.product_id
GROUP BY p.category
ORDER BY avg_review_rating DESC;



