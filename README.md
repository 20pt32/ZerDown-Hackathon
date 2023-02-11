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


--to remove the duplicates

WITH duplicates AS (
  SELECT MIN(id) AS id, state_license, phone_numbers, email, address
  FROM agent_info
  GROUP BY state_license, phone_numbers, email, address
  HAVING COUNT(*) > 1
)
DELETE FROM agent_info
WHERE (id, state_license, phone_numbers, email, address) NOT IN (
  SELECT id, state_license, phone_numbers, email, address
  FROM duplicates
);

--to delete the duplicate brokerage branches
WITH duplicates AS (
  SELECT MIN(id) AS id, name, phone_numbers
  FROM brokerage
  GROUP BY name, phone_numbers
  HAVING COUNT(*) > 1
)
DELETE FROM brokerage
WHERE (id, name, phone_numbers) NOT IN (
  SELECT id, name, phone_numbers
  FROM duplicates
);

--creating a new table to store the relationships between agents by joining the home_info and agent_listing tables based on the home_id column. This new table can have columns for the home_id, listing_agent_id, and selling_agent_id, which can be derived from the agent_listing table based on the deal_side column.
CREATE TABLE agent_relationships AS
SELECT home_id,
       MIN(CASE WHEN deal_side = 'listing' THEN agent_id END) AS listing_agent_id,
       MIN(CASE WHEN deal_side = 'selling' THEN agent_id END) AS selling_agent_id
FROM home_info
JOIN agent_listing
ON home_info.id = agent_listing.home_id
GROUP BY home_id;
