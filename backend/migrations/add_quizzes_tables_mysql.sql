-- Migration: Add Quizzes Tables (MySQL)
-- Date: 2025-12-01
-- Description: Create tables for quiz system

USE `vp-project`;

-- Quizzes Table
CREATE TABLE IF NOT EXISTS quizzes (
    quiz_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    task_id INT NOT NULL,
    course_id INT DEFAULT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    total_questions INT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP NULL DEFAULT NULL,
    completed_at TIMESTAMP NULL DEFAULT NULL,
    
    INDEX idx_quizzes_user_id (user_id),
    INDEX idx_quizzes_task_id (task_id),
    INDEX idx_quizzes_course_id (course_id),
    INDEX idx_quizzes_status (status),
    
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (task_id) REFERENCES tasks(task_id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Quiz Questions Table
CREATE TABLE IF NOT EXISTS quiz_questions (
    question_id INT AUTO_INCREMENT PRIMARY KEY,
    quiz_id INT NOT NULL,
    question_number INT NOT NULL,
    question_text TEXT NOT NULL,
    option_a VARCHAR(500) NOT NULL,
    option_b VARCHAR(500) NOT NULL,
    option_c VARCHAR(500) NOT NULL,
    option_d VARCHAR(500) NOT NULL,
    correct_answer VARCHAR(1) NOT NULL,
    explanation TEXT,
    user_answer VARCHAR(1) DEFAULT NULL,
    is_correct BOOLEAN DEFAULT NULL,
    
    INDEX idx_quiz_questions_quiz_id (quiz_id),
    
    FOREIGN KEY (quiz_id) REFERENCES quizzes(quiz_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Quiz Results Table
CREATE TABLE IF NOT EXISTS quiz_results (
    result_id INT AUTO_INCREMENT PRIMARY KEY,
    quiz_id INT NOT NULL UNIQUE,
    user_id INT NOT NULL,
    score INT NOT NULL,
    total_questions INT NOT NULL,
    percentage FLOAT NOT NULL,
    time_taken INT DEFAULT NULL,
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_quiz_results_quiz_id (quiz_id),
    INDEX idx_quiz_results_user_id (user_id),
    
    FOREIGN KEY (quiz_id) REFERENCES quizzes(quiz_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
