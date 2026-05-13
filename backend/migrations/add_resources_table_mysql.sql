-- Migration: Add Resources Table (MySQL)
-- Date: 2025-12-01
-- Description: Create resources table for storing student learning materials

USE `vp-project`;

CREATE TABLE IF NOT EXISTS resources (
    resource_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    course_id INT DEFAULT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    resource_type VARCHAR(50) NOT NULL DEFAULT 'document',
    file_path VARCHAR(500) DEFAULT NULL,
    url VARCHAR(500) DEFAULT NULL,
    file_size INT DEFAULT NULL,
    file_extension VARCHAR(10) DEFAULT NULL,
    tags VARCHAR(500) DEFAULT NULL,
    is_favorite BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    last_accessed TIMESTAMP NULL DEFAULT NULL,
    
    INDEX idx_resources_user_id (user_id),
    INDEX idx_resources_course_id (course_id),
    INDEX idx_resources_type (resource_type),
    INDEX idx_resources_favorite (is_favorite),
    
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
