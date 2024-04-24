UPDATE dim_products
SET product_price=REPLACE(product_price,'£','');

ALTER TABLE dim_products
ADD COLUMN weight_class VARCHAR(50);

ALTER TABLE dim_products
RENAME COLUMN weight TO weight_kg;

UPDATE dim_products
SET weight_kg= REPLACE(weight_kg,'kg','');

ALTER TABLE dim_products
ALTER COLUMN weight_kg SET DATA TYPE FLOAT USING weight_kg::float;


UPDATE dim_products
SET weight_class= CASE 	
						WHEN weight_kg < 2 THEN 'light'
						WHEN weight_kg >=2 AND weight_kg<40 THEN 'Mid_Sized'
						WHEN weight_kg>=40 AND weight_kg <140 THEN 'Heavy'
						WHEN weight_kg>=140 THEN 'Truck_Required'
				  END;

