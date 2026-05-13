-- Database Optimization: Add Indexes for Better Performance
-- Phase 8: Testing, Optimization & Documentation
-- Run this SQL script to add indexes to improve query performance

-- Users table indexes
CREATE INDEX idx_users_email ON users(email);

-- Courses table indexes
CREATE INDEX idx_courses_user_id ON courses(user_id);

-- Tasks table indexes
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_deadline ON tasks(deadline);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_course_id ON tasks(course_id);
CREATE INDEX idx_tasks_user_deadline ON tasks(user_id, deadline);

-- Schedules table indexes
CREATE INDEX idx_schedules_user_id ON schedules(user_id);
CREATE INDEX idx_schedules_date ON schedules(date);
CREATE INDEX idx_schedules_user_date ON schedules(user_id, date);
CREATE INDEX idx_schedules_task_id ON schedules(task_id);

-- Analytics table indexes
CREATE INDEX idx_analytics_user_id ON analytics(user_id);
CREATE INDEX idx_analytics_task_id ON analytics(task_id);
CREATE INDEX idx_analytics_recorded_at ON analytics(recorded_at);

-- Notifications table indexes
CREATE INDEX idx_notifications_user_id ON notifications(user_id);
CREATE INDEX idx_notifications_is_read ON notifications(is_read);
CREATE INDEX idx_notifications_user_read ON notifications(user_id, is_read);
CREATE INDEX idx_notifications_created_at ON notifications(created_at);
CREATE INDEX idx_notifications_type ON notifications(type);

-- Groups table indexes
CREATE INDEX idx_groups_admin_user_id ON `groups`(admin_user_id);

-- Group Members table indexes
CREATE INDEX idx_group_members_user_id ON group_members(user_id);
CREATE INDEX idx_group_members_group_id ON group_members(group_id);

-- Performance Notes:
-- These indexes will significantly improve query performance for:
-- 1. User login (email lookup)
-- 2. Fetching user's courses, tasks, schedules
-- 3. Filtering tasks by deadline and status
-- 4. Calendar queries (date-based lookups)
-- 5. Notification filtering (unread, by type)
-- 6. Analytics queries (user-specific data)
-- 7. Group membership lookups

-- To verify indexes are created:
-- SHOW INDEX FROM users;
-- SHOW INDEX FROM tasks;
-- etc.
