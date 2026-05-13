-- Migration: Add join_code column to groups table
-- Date: 2025-12-01
-- Description: Add join_code column for group invitation functionality

USE `vp-project`;

-- Add join_code column to groups table
ALTER TABLE `groups` 
ADD COLUMN join_code VARCHAR(10) NULL AFTER description;

-- Create unique index on join_code
CREATE UNIQUE INDEX idx_groups_join_code ON `groups`(join_code);

-- Generate join codes for existing groups (if any)
-- This will create unique 6-character codes for groups that don't have one
UPDATE `groups` 
SET join_code = CONCAT(
    CHAR(65 + FLOOR(RAND() * 26)),
    CHAR(65 + FLOOR(RAND() * 26)),
    FLOOR(RAND() * 10),
    CHAR(65 + FLOOR(RAND() * 26)),
    FLOOR(RAND() * 10),
    CHAR(65 + FLOOR(RAND() * 26))
)
WHERE join_code IS NULL;

-- Make join_code NOT NULL after populating existing records
ALTER TABLE `groups` 
MODIFY COLUMN join_code VARCHAR(10) NOT NULL;

-- Verify the change
SELECT 'join_code column added successfully!' AS Status;
DESCRIBE `groups`;
