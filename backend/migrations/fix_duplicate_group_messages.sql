-- Migration: Fix Duplicate group_messages Tables
-- Date: 2025-12-01
-- Description: Remove duplicate group_messages tables and ensure correct structure

USE `vp-project`;

-- Step 1: Check if there are duplicate tables
SELECT TABLE_NAME, TABLE_SCHEMA 
FROM information_schema.TABLES 
WHERE TABLE_NAME LIKE '%group_message%' 
AND TABLE_SCHEMA = 'vp-project';

-- Step 2: Drop all group_messages related tables to start fresh
DROP TABLE IF EXISTS group_message_reads;
DROP TABLE IF EXISTS group_messages;

-- Step 3: Recreate group_messages table with correct structure
CREATE TABLE group_messages (
    message_id INT AUTO_INCREMENT PRIMARY KEY,
    group_id INT NOT NULL,
    user_id INT NOT NULL,
    message_text TEXT NOT NULL,
    message_type VARCHAR(20) DEFAULT 'text' NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    edited_at TIMESTAMP NULL DEFAULT NULL,
    
    INDEX idx_group_messages_group_id (group_id),
    INDEX idx_group_messages_user_id (user_id),
    INDEX idx_group_messages_created_at (created_at),
    
    FOREIGN KEY (group_id) REFERENCES `groups`(group_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Step 4: Create group_message_reads table for read tracking
CREATE TABLE group_message_reads (
    message_id INT NOT NULL,
    user_id INT NOT NULL,
    read_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    
    PRIMARY KEY (message_id, user_id),
    INDEX idx_message_reads_user (user_id),
    INDEX idx_message_reads_read_at (read_at),
    
    FOREIGN KEY (message_id) REFERENCES group_messages(message_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Step 5: Verify tables were created correctly
SELECT 'Duplicate tables fixed successfully!' AS Status;

SELECT TABLE_NAME, TABLE_ROWS, CREATE_TIME
FROM information_schema.TABLES 
WHERE TABLE_NAME IN ('group_messages', 'group_message_reads') 
AND TABLE_SCHEMA = 'vp-project';

-- Show table structures
DESCRIBE group_messages;
DESCRIBE group_message_reads;
