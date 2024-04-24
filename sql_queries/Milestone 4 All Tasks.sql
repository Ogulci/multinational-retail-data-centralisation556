--TASK 1. HOW MANY STORES DOES BUSINESS HAVE AND IN WHICH COUNTRIES? :  
SELECT 
	country_code AS country,
	COUNT(country_code) AS total_no_stores		
FROM dim_store_details
WHERE address NOTNULL
GROUP BY country_code
ORDER BY total_no_stores DESC;


--TASK 2. WHICH LOCATIONS CURRENTLY HAVE THE MOST STORES? :
SELECT locality,
		COUNT(locality) as total_no_stores
FROM dim_store_details
GROUP BY  dim_store_details.locality
ORDER BY total_no_stores DESC;

-- TASK 3. WHICH MONTHS PRODUCES THE LARGEST AMOUNT OF SALES? : 
SELECT 	
		ROUND(SUM(orders_table.product_quantity*dim_products.product_price)::NUMERIC,2) AS total_sales,
		dim_date_times.month AS "month"

FROM orders_table
JOIN dim_products ON orders_table.product_code= dim_products.product_code
JOIN dim_date_times ON orders_table.date_uuid =dim_date_times.date_uuid

GROUP BY "month"
ORDER BY  total_sales DESC
LIMIT 6;


--TASK 4 HOW MANY SALES ARE COMING FROM ONLINE? : 

SELECT 
    	COUNT(store_code) AS numbers_of_sales,
    	SUM(product_quantity) AS product_quantity_count,
    	CASE 
        	WHEN store_code LIKE 'WEB-1388012W' THEN 'Web'
        	ELSE 'Offline'
    		END AS "location"
FROM orders_table 
GROUP BY  "location" 
ORDER BY numbers_of_sales ;


--TASK 5. What percentage of sales come through each type of store? :
SELECT store_type,
	   total_sales,
	   ROUND((total_sales / SUM(total_sales) OVER() * 100)::numeric, 2) AS percentage
FROM (	
	
		SELECT  store_type,
		ROUND(SUM(product_quantity * product_price)::NUMERIC, 2) AS total_sales
		FROM orders_table
		JOIN dim_store_details ON orders_table.store_code=dim_store_details.store_code
		JOIN dim_products ON orders_table.product_code=dim_products.product_code
		GROUP BY  store_type
) 
GROUP BY store_type, total_sales
ORDER BY total_sales DESC;


--TASK 6. WHICH MONTH IN EACH YEAR PRODUCED THE HIGHEST COST OF SALES? :
SELECT  ROUND(SUM(product_price*product_quantity)::numeric, 2) AS sales,
		"year",
		"month"
		
FROM orders_table 
JOIN dim_products ON orders_table.product_code=dim_products.product_code
JOIN dim_date_times ON orders_table.date_uuid=dim_date_times.date_uuid

GROUP BY "year", "month"
ORDER BY sales DESC
LIMIT 10;


--TASK 7 WHAT IS OUR STAFF HEADCOUNT? : 

SELECT  SUM(staff_numbers) AS total_staff_number,
		country_code AS country
FROM dim_store_details
GROUP BY country
ORDER BY total_staff_number DESC;


--TASK 8 WHICH GERMAN STORE TYPE SELLING THE MOST?
SELECT  ROUND(SUM(product_quantity*product_price)::NUMERIC,2) as total_sales,
		store_type,
		country_code as country
		
FROM orders_table
JOIN dim_products ON orders_table.product_code=dim_products.product_code
JOIN dim_store_details ON orders_table.store_code=dim_store_details.store_code
WHERE country_code= 'DE'
GROUP BY store_type, country
ORDER BY total_sales;



--TASK 9 HOW QUICKLY IS THE COMPANY MAKING SALES? 
WITH full_date_cte AS (
    SELECT "year",
        TO_TIMESTAMP(year || '-' || month || '-' || day || ' ' || timestamp, 'YYYY-MM-DD HH24:MI:SS') AS full_date
    FROM 
        dim_date_times
),
next_full_date_cte AS (
	SELECT year,
    	full_date,
    	LEAD(full_date) OVER (ORDER BY full_date) AS next_full_date
FROM full_date_cte

),
avg_time_difference_cte AS ( SELECT year,
	 ABS(AVG(EXTRACT(EPOCH FROM (full_date - next_full_date)))) AS avg_time_difference

FROM next_full_date_cte
GROUP BY year
)
SELECT 
    year,
	CONCAT( 'hours: ', FLOOR(avg_time_difference/3600),', ',
		    'minutes: ', FLOOR((avg_time_difference %3600)/60), ', ',
		    'seconds: ', FLOOR(avg_time_difference %60 ), ', ',
		    'miliseconds: ', ROUND((avg_time_difference - FLOOR(avg_time_difference)) * 1000)	
	) AS actual_time_taken           
FROM avg_time_difference_cte
ORDER BY avg_time_difference DESC;
