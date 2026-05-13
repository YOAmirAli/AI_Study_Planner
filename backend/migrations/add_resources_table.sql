-- Migration: Add Resources Table
-- Date: 2025-12-01
-- Description: Create resources table for storing student learning materials

CREATE TABLE IF NOT EXISTS resources (
    resource_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    course_id INTEGER,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    resource_type VARCHAR(50) NOT NULL DEFAULT 'document',
    file_path VARCHAR(500),
    url VARCHAR(500),
    file_size INTEGER,
    file_extension VARCHAR(10),
    tags VARCHAR(500),
    is_favorite BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_accessed TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE SET NULL
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_resources_user_id ON resources(user_id);
CREATE INDEX IF NOT EXISTS idx_resources_course_id ON resources(course_id);
CREATE INDEX IF NOT EXISTS idx_resources_type ON resources(resource_type);
CREATE INDEX IF NOT EXISTS idx_resources_favorite ON resources(is_favorite);

-- Trigger to update updated_at timestamp
CREATE TRIGGER IF NOT EXISTS update_resources_timestamp 
AFTER UPDATE ON resources
FOR EACH ROW
BEGIN
    UPDATE resources SET updated_at = CURRENT_TIMESTAMP WHERE resource_id = NEW.resource_id;
END;
