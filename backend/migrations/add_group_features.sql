-- Migration: Add Group Features (Messages, Resources, Challenges)
-- Date: 2025-12-01
-- Description: Add tables for group chat, shared resources, and challenges

USE `vp-project`;

-- Group Messages Table
CREATE TABLE IF NOT EXISTS group_messages (
    message_id INT AUTO_INCREMENT PRIMARY KEY,
    group_id INT NOT NULL,
    user_id INT NOT NULL,
    message_text TEXT NOT NULL,
    message_type VARCHAR(20) DEFAULT 'text',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    edited_at TIMESTAMP NULL DEFAULT NULL,
    
    INDEX idx_group_messages_group_id (group_id),
    INDEX idx_group_messages_user_id (user_id),
    INDEX idx_group_messages_created_at (created_at),
    
    FOREIGN KEY (group_id) REFERENCES `groups`(group_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Group Resources Table
CREATE TABLE IF NOT EXISTS group_resources (
    resource_id INT AUTO_INCREMENT PRIMARY KEY,
    group_id INT NOT NULL,
    shared_by_user_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    resource_type VARCHAR(50) NOT NULL,
    resource_url VARCHAR(500),
    content TEXT,
    tags VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_group_resources_group_id (group_id),
    INDEX idx_group_resources_user_id (shared_by_user_id),
    
    FOREIGN KEY (group_id) REFERENCES `groups`(group_id) ON DELETE CASCADE,
    FOREIGN KEY (shared_by_user_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
