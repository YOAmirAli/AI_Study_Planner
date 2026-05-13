-- Migration: Verify and Fix CASCADE DELETE for Group Tables
-- Date: 2025-12-01
-- Description: Ensure all group-related tables have proper CASCADE DELETE

USE `vp-project`;

-- Check current foreign key constraints
SELECT 
    TABLE_NAME,
    CONSTRAINT_NAME,
    REFERENCED_TABLE_NAME,
    DELETE_RULE
FROM information_schema.REFERENTIAL_CONSTRAINTS
WHERE CONSTRAINT_SCHEMA = 'vp-project'
AND (TABLE_NAME LIKE '%group%' OR REFERENCED_TABLE_NAME LIKE '%group%');

-- Drop and recreate foreign keys with CASCADE DELETE if needed

-- For group_members table
ALTER TABLE group_members DROP FOREIGN KEY IF EXISTS group_members_ibfk_1;
ALTER TABLE group_members DROP FOREIGN KEY IF EXISTS group_members_ibfk_2;

ALTER TABLE group_members
ADD CONSTRAINT group_members_ibfk_1 
FOREIGN KEY (group_id) REFERENCES `groups`(group_id) ON DELETE CASCADE;

ALTER TABLE group_members
ADD CONSTRAINT group_members_ibfk_2 
FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE;

-- For group_messages table
ALTER TABLE group_messages DROP FOREIGN KEY IF EXISTS group_messages_ibfk_1;
ALTER TABLE group_messages DROP FOREIGN KEY IF EXISTS group_messages_ibfk_2;

ALTER TABLE group_messages
ADD CONSTRAINT group_messages_ibfk_1 
FOREIGN KEY (group_id) REFERENCES `groups`(group_id) ON DELETE CASCADE;

ALTER TABLE group_messages
ADD CONSTRAINT group_messages_ibfk_2 
FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE;

-- For group_resources table
ALTER TABLE group_resources DROP FOREIGN KEY IF EXISTS group_resources_ibfk_1;
ALTER TABLE group_resources DROP FOREIGN KEY IF EXISTS group_resources_ibfk_2;

ALTER TABLE group_resources
ADD CONSTRAINT group_resources_ibfk_1 
FOREIGN KEY (group_id) REFERENCES `groups`(group_id) ON DELETE CASCADE;

ALTER TABLE group_resources
ADD CONSTRAINT group_resources_ibfk_2 
FOREIGN KEY (shared_by_user_id) REFERENCES users(user_id) ON DELETE CASCADE;

-- For group_message_reads table
ALTER TABLE group_message_reads DROP FOREIGN KEY IF EXISTS group_message_reads_ibfk_1;
ALTER TABLE group_message_reads DROP FOREIGN KEY IF EXISTS group_message_reads_ibfk_2;

ALTER TABLE group_message_reads
ADD CONSTRAINT group_message_reads_ibfk_1 
FOREIGN KEY (message_id) REFERENCES group_messages(message_id) ON DELETE CASCADE;

ALTER TABLE group_message_reads
ADD CONSTRAINT group_message_reads_ibfk_2 
FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE;

-- Verify the changes
SELECT 'CASCADE DELETE constraints updated successfully!' AS Status;

SELECT 
    TABLE_NAME,
    CONSTRAINT_NAME,
    REFERENCED_TABLE_NAME,
    DELETE_RULE
FROM information_schema.REFERENTIAL_CONSTRAINTS
WHERE CONSTRAINT_SCHEMA = 'vp-project'
AND (TABLE_NAME LIKE '%group%' OR REFERENCED_TABLE_NAME LIKE '%group%')
ORDER BY TABLE_NAME;
