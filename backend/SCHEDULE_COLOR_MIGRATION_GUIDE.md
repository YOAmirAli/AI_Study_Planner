# Schedule Color Field Migration Guide

## Issue
The schedule page shows "Failed to save schedule entry" because the `color` column doesn't exist in the database yet.

## Solution
Run the database migration to add the color column to the schedules table.

## Steps to Fix

### Option 1: Run Migration SQL (Recommended)
1. Open MySQL Workbench
2. Connect to your database
3. Open the file: `backend/migrations/add_color_to_schedules.sql`
4. Execute the SQL script

OR manually run these commands:

```sql
USE `vp-project`;

-- Add color column
ALTER TABLE schedules 
ADD COLUMN color VARCHAR(7) DEFAULT '#667eea' AFTER title;

-- Update existing records
UPDATE schedules 
SET color = '#667eea' 
WHERE color IS NULL;

-- Verify
SELECT 'Migration complete!' AS Status;
```

### Option 2: Drop and Recreate (If no important data)
If you don't have important schedule data, you can drop and recreate the table:

```sql
USE `vp-project`;

DROP TABLE IF EXISTS schedules;

CREATE TABLE schedules (
    schedule_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    task_id INT NULL,
    date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    block_type ENUM('class', 'study', 'break') NOT NULL DEFAULT 'study',
    title VARCHAR(255) NULL,
    color VARCHAR(7) DEFAULT '#667eea',
    is_auto_generated BOOLEAN NOT NULL DEFAULT FALSE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_id (user_id),
    INDEX idx_task_id (task_id),
    INDEX idx_date (date),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (task_id) REFERENCES tasks(task_id) ON DELETE SET NULL
);
```

## Verify the Fix

After running the migration:

1. Restart your Flask backend server
2. Open the Schedule page in your browser
3. Open browser console (F12)
4. Try to create a new schedule block
5. Check the console logs for detailed error messages

## Debugging

If you still see errors, check:

1. **Backend Console**: Look for "SCHEDULE CREATE ERROR" messages
2. **Browser Console**: Look for "SAVING SCHEDULE" and error details
3. **Database**: Verify the color column exists:
   ```sql
   DESCRIBE schedules;
   ```

## What Changed

### Backend
- `backend/app/models/schedule.py` - Added color field
- `backend/app/services/schedule_service.py` - Updated to handle color
- `backend/app/routes/schedule_routes.py` - Added color to API

### Frontend
- `frontend/src/pages/Schedule.jsx` - Added color picker in dialog

### Database
- Added `color VARCHAR(7)` column with default value '#667eea'
