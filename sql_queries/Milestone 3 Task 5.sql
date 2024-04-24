ALTER TABLE dim_products
RENAME COLUMN removed TO still_available;

UPDATE dim_products
SET still_available= CASE
						WHEN still_available= 'Still_avaliable' THEN TRUE
						WHEN still_available='Removed' THEN FALSE
					END;
					
ALTER TABLE dim_products
ALTER COLUMN still_available SET DATA TYPE BOOL USING still_available::bool,
ALTER COLUMN product_price SET DATA TYPE FLOAT USING product_price::float,
ALTER COLUMN "EAN" SET DATA TYPE VARCHAR(255),
ALTER COLUMN product_code SET DATA TYPE VARCHAR(255),
ALTER COLUMN date_added SET DATA TYPE DATE USING date_added::DATE,
ALTER COLUMN uuid SET DATA TYPE UUID USING uuid::UUID;



