ALTER TABLE dim_card_details
ALTER COLUMN card_number SET DATA TYPE VARCHAR(50),
ALTER COLUMN expiry_date SET DATA TYPE VARCHAR(10),
ALTER COLUMN date_payment_confirmed  SET DATA TYPE DATE USING date_payment_confirmed ::DATE;