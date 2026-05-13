-- MySQL Database Setup Script for AI Study Planner
-- Run this script in MySQL Workbench before starting the Flask application

-- Create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS `vp-project` 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- Use the database
USE `vp-project`;

-- Show confirmation
SELECT 'Database vp-project created successfully!' AS Status;
