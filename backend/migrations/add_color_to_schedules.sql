-- Migration: Add color field to schedules table
-- Date: 2025-11-30
-- Description: Safely adds a color column to the schedules table with a default value

USE `vp-project`;

-- Add color column to schedules table
-- Using VARCHAR(7) to store hex color codes (e.g., #667eea)
-- Setting default value to #667eea (purple-blue color)
-- Making it nullable to avoid issues with existing data
ALTER TABLE schedules 
ADD COLUMN color VARCHAR(7) DEFAULT '#667eea' AFTER title;

-- Update existing records to have the default color if they don't have one
UPDATE schedules 
SET color = '#667eea' 
WHERE color IS NULL;

-- Verify the migration
SELECT 'Color column added successfully to schedules table' AS Status;
SELECT COUNT(*) AS total_schedules, 
       COUNT(color) AS schedules_with_color 
FROM schedules;
