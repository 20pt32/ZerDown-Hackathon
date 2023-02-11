# ZerDown-Hackathon

--will change the foreign key constraint to set the brokerage_id to null in the agent_info table if the corresponding brokerage is deleted from the brokerage table.

ALTER TABLE agent_info
DROP CONSTRAINT agent_ibfk_1;

ALTER TABLE agent_info
ADD CONSTRAINT agent_ibfk_1
FOREIGN KEY (brokerage_id)
REFERENCES brokerage(id)
ON DELETE SET NULL;

-- 1. to identify and delete duplicate brokerages using fuzzy string matching algorithm

-- Install the fuzzystrmatch extension

CREATE EXTENSION IF NOT EXISTS fuzzystrmatch;

-- Create a temporary table to store the levenshtein distances between brokerages

CREATE TEMPORARY TABLE temp_brokerage AS
SELECT 
  b1.id AS id1,
  b2.id AS id2,
  levenshtein(b1.name, b2.name) AS distance
FROM 
  brokerage b1
  JOIN brokerage b2 ON b1.id < b2.id;

-- Create an index on the temp_brokerage table to speed up query execution

CREATE INDEX temp_brokerage_index ON temp_brokerage (distance);

-- Delete duplicate brokerages by keeping the record with the lowest id

WITH duplicates AS (
  SELECT 
    id1,
    MIN(id2) AS duplicate_id
  FROM 
    temp_brokerage
  WHERE 
    distance <= 3
  GROUP BY 
    id1
)
DELETE FROM 
  brokerage
WHERE 
  id IN (SELECT duplicate_id FROM duplicates);

-- Drop the temp_brokerage table

DROP TABLE temp_brokerage;



--2.to identify and delete duplicate agents using fuzzy string matching algorithm

WITH duplicates AS (
  SELECT 
    id, 
    row_number() OVER (PARTITION BY 
      levenshtein(lower(first_name), lower(email)) + 
      levenshtein(lower(first_name), lower(state_license)) + 
      levenshtein(lower(first_name), lower(phone_numbers)) +
      levenshtein(lower(first_name), lower(street || ' ' || city || ' ' || state || ' ' || zipcode))
    ORDER BY id) AS row_num
  FROM agent_info
)
DELETE FROM agent_info 
WHERE id IN (SELECT id FROM duplicates WHERE row_num > 1);


--3.to identify and delete duplicate brokerage branches

-- Enable the pg_trgm extension

CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Create a temporary table to store the unique brokerage branches

CREATE TEMPORARY TABLE unique_brokerage AS
  SELECT DISTINCT ON (name, phone_numbers, street, city, state, zipcode) 
    *
  FROM 
    brokerage;

-- Drop the original brokerage table

DROP TABLE brokerage;

-- Rename the temporary table to the original table name

ALTER TABLE unique_brokerage RENAME TO brokerage;

--creating a new table to store the relationships between agents by joining the home_info and agent_listing tables based on the home_id column. This new table can have columns for the home_id, listing_agent_id, and selling_agent_id, which can be derived from the agent_listing table based on the deal_side column.

CREATE TABLE agent_relationships AS
SELECT home_id,
       MIN(CASE WHEN deal_side = 'listing' THEN agent_id END) AS listing_agent_id,
       MIN(CASE WHEN deal_side = 'selling' THEN agent_id END) AS selling_agent_id
FROM home_info
JOIN agent_listing
ON home_info.id = agent_listing.home_id
GROUP BY home_id;

CREATE TABLE agent_relationship_graph AS
SELECT DISTINCT a.listing_agent_id AS agent_a_id, b.selling_agent_id AS agent_b_id
FROM agent_relationships a
JOIN agent_relationships b
ON a.home_id = b.home_id AND a.listing_agent_id != b.selling_agent_id;

