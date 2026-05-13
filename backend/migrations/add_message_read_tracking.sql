-- Migration: Add Message Read Tracking
-- Date: 2025-12-01
-- Description: Add table to track which messages have been read by which users

USE `vp-project`;

-- Message Read Status Table
CREATE TABLE IF NOT EXISTS group_message_reads (
    message_id INT NOT NULL,
    user_id INT NOT NULL,
    read_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    
    PRIMARY KEY (message_id, user_id),
    INDEX idx_message_reads_user (user_id),
    INDEX idx_message_reads_read_at (read_at),
    
    FOREIGN KEY (message_id) REFERENCES group_messages(message_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Verify table was created
SELECT 'Message read tracking table created successfully!' AS Status;
DESCRIBE group_message_reads;
