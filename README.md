# ZerDown-Hackathon

--will change the foreign key constraint to set the brokerage_id to null in the agent_info table if the corresponding brokerage is deleted from the brokerage table.

ALTER TABLE agent_info
DROP CONSTRAINT agent_ibfk_1;

ALTER TABLE agent_info
ADD CONSTRAINT agent_ibfk_1
FOREIGN KEY (brokerage_id)
REFERENCES brokerage(id)
ON DELETE SET NULL;

--to remove the duplicates from brokerages

WITH clean_brokerages AS (
  SELECT id, TRIM(LOWER(name)) AS clean_name
  FROM brokerage
), duplicates AS (
  SELECT MIN(id) AS keep_id, clean_name
  FROM clean_brokerages
  GROUP BY clean_name
  HAVING COUNT(*) > 1
)
DELETE FROM brokerage
WHERE id NOT IN (
  SELECT keep_id
  FROM duplicates
);


-- Add a new column to the agent_info table
ALTER TABLE agent_info ADD COLUMN address TEXT;

-- Populate the new address column with the result of the query
UPDATE agent_info SET address = COALESCE(street, '') || ', ' || COALESCE(city, '') || ', ' || COALESCE(state, '') || ', ' || COALESCE(county, '') || ', ' || COALESCE(zipcode, '');

  
--to indentify duplicate agents

WITH duplicates AS (
  SELECT 
    state_license, 
    phone_numbers, 
    email, 
    address, 
    ROW_NUMBER() OVER (PARTITION BY state_license, phone_numbers, email, address ORDER BY state_license) AS row_number
  FROM 
    agent_info
)
SELECT 
  state_license, 
  phone_numbers, 
  email, 
  address
FROM 
  duplicates
WHERE 
  row_number > 1;


