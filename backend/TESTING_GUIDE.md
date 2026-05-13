# 🧪 Testing Guide

Comprehensive guide for testing the AI Study Planner backend.

---

## 📋 Table of Contents

1. [Test Overview](#test-overview)
2. [Running Tests](#running-tests)
3. [Test Coverage](#test-coverage)
4. [Writing New Tests](#writing-new-tests)
5. [Troubleshooting](#troubleshooting)

---

## 🎯 Test Overview

### Test Structure

```
backend/
├── test_phase2.py          # Authentication tests
├── test_phase3.py          # Courses & Tasks tests
├── test_phase4.py          # Schedule tests
├── test_phase5.py          # AI Tools tests
├── test_phase6.py          # Analytics tests
└── test_phase7.py          # Notifications & Groups tests
```

### Test Statistics
- **Total Test Files:** 6
- **Total Tests:** 100+
- **Coverage:** All major features
- **Status:** ✅ All Passing

---

## 🏃 Running Tests

### Prerequisites

1. **Start the Flask Server**
```bash
python run.py
```

2. **Ensure Database is Running**
```bash
# Check MySQL is running
mysql -u your_username -p -e "SELECT 1"
```

### Run Individual Phase Tests

```bash
# Phase 2: Authentication
python test_phase2.py

# Phase 3: Courses & Tasks
python test_phase3.py

# Phase 4: Schedule Management
python test_phase4.py

# Phase 5: AI Tools
python test_phase5.py

# Phase 6: Analytics
python test_phase6.py

# Phase 7: Notifications & Groups
python test_phase7.py
```

### Run All Tests

```bash
# Windows
for %f in (test_phase*.py) do python %f

# Mac/Linux
for file in test_phase*.py; do python "$file"; done
```

---

## 📊 Test Coverage

### Phase 2: Authentication (15+ tests)
- ✅ User registration
- ✅ User login
- ✅ JWT token validation
- ✅ Get current user
- ✅ Update profile
- ✅ Change password
- ✅ Error handling (invalid credentials, duplicate email)

### Phase 3: Courses & Tasks (20+ tests)
- ✅ Create course
- ✅ Get all courses
- ✅ Update course
- ✅ Delete course
- ✅ Create task
- ✅ Get all tasks
- ✅ Filter tasks (status, priority, course)
- ✅ Mark task complete
- ✅ Get upcoming tasks
- ✅ Get overdue tasks
- ✅ Error handling

### Phase 4: Schedule Management (15+ tests)
- ✅ Get weekly schedule
- ✅ Generate AI schedule
- ✅ Create manual schedule block
- ✅ Update schedule
- ✅ Delete schedule
- ✅ Conflict detection
- ✅ Error handling

### Phase 5: AI Tools (15+ tests)
- ✅ Text summarization
- ✅ Quiz generation
- ✅ Flashcard creation
- ✅ Study material recommendations
- ✅ Error handling (invalid input, API failures)

### Phase 6: Analytics (15+ tests)
- ✅ Dashboard statistics
- ✅ Detailed analytics
- ✅ Progress tracking
- ✅ Falling behind prediction
- ✅ Weekly summary
- ✅ Log study session
- ✅ Error handling

### Phase 7: Notifications & Groups (20+ tests)
- ✅ Create notification
- ✅ Get notifications
- ✅ Mark as read
- ✅ Mark all as read
- ✅ Delete notification
- ✅ Create group
- ✅ Join group
- ✅ Leave group
- ✅ Update group (admin only)
- ✅ Delete group (admin only)
- ✅ Authorization checks
- ✅ Error handling

---

## ✍️ Writing New Tests

### Test Template

```python
"""
Test script for [Feature Name]
"""
import requests
import json

BASE_URL = "http://localhost:5000/api"

def print_response(title, response):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text[:500]}")

def test_feature():
    """Test feature functionality"""
    print("\n🧪 TESTING [FEATURE NAME]")
    print("="*60)
    
    # Step 1: Setup (login, create test data)
    login_data = {
        "email": "test@example.com",
        "password": "TestPassword123"
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    token = response.json().get('token')
    headers = {"Authorization": f"Bearer {token}"}
    
    # Step 2: Test main functionality
    print("\n📝 Test 1: [Test Description]")
    test_data = {
        "field1": "value1",
        "field2": "value2"
    }
    response = requests.post(f"{BASE_URL}/endpoint", json=test_data, headers=headers)
    print_response("POST /api/endpoint", response)
    
    # Step 3: Test error cases
    print("\n⚠️ Test 2: Error Handling")
    error_data = {"invalid": "data"}
    response = requests.post(f"{BASE_URL}/endpoint", json=error_data, headers=headers)
    print_response("POST /api/endpoint (error)", response)
    
    # Step 4: Summary
    print("\n" + "="*60)
    print("✅ TESTING COMPLETE!")
    print("="*60)

if __name__ == "__main__":
    test_feature()
```

### Best Practices

1. **Test Isolation**
   - Each test should be independent
   - Clean up test data after tests
   - Don't rely on test execution order

2. **Clear Test Names**
   - Use descriptive test names
   - Include expected behavior
   - Example: `test_create_course_with_valid_data`

3. **Comprehensive Coverage**
   - Test happy path (success cases)
   - Test error cases
   - Test edge cases
   - Test authorization

4. **Assertions**
   - Check status codes
   - Verify response structure
   - Validate data correctness

---

## 🔍 Test Examples

### Example 1: Testing Authentication

```python
def test_authentication():
    # Test registration
    register_data = {
        "email": "newuser@example.com",
        "password": "SecurePass123",
        "name": "New User"
    }
    response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
    assert response.status_code == 201
    
    # Test login
    login_data = {
        "email": "newuser@example.com",
        "password": "SecurePass123"
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    assert response.status_code == 200
    assert 'token' in response.json()
    
    # Test invalid login
    invalid_data = {
        "email": "newuser@example.com",
        "password": "WrongPassword"
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=invalid_data)
    assert response.status_code == 401
```

### Example 2: Testing CRUD Operations

```python
def test_course_crud():
    # Setup: Login
    token = login_and_get_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create
    course_data = {
        "course_name": "Test Course",
        "course_code": "TEST101"
    }
    response = requests.post(f"{BASE_URL}/courses", json=course_data, headers=headers)
    assert response.status_code == 201
    course_id = response.json()['course']['course_id']
    
    # Read
    response = requests.get(f"{BASE_URL}/courses/{course_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()['course']['course_name'] == "Test Course"
    
    # Update
    update_data = {"course_name": "Updated Course"}
    response = requests.put(f"{BASE_URL}/courses/{course_id}", json=update_data, headers=headers)
    assert response.status_code == 200
    
    # Delete
    response = requests.delete(f"{BASE_URL}/courses/{course_id}", headers=headers)
    assert response.status_code == 200
```

---

## 🐛 Troubleshooting

### Common Issues

#### 1. Connection Refused
```
Error: Connection refused to localhost:5000
```
**Solution:** Make sure Flask server is running
```bash
python run.py
```

#### 2. Authentication Failures
```
Error: 401 Unauthorized
```
**Solution:** 
- Check if test user exists
- Verify JWT token is valid
- Check token expiration

#### 3. Database Errors
```
Error: Table doesn't exist
```
**Solution:**
```bash
# Recreate database tables
python run.py  # This will create tables automatically
```

#### 4. Test Data Conflicts
```
Error: 409 Conflict - Resource already exists
```
**Solution:**
- Use unique test data
- Clean up after tests
- Use random values for testing

### Debug Mode

Enable detailed error messages:

```python
# In test file
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## 📈 Test Metrics

### Current Status

| Phase | Tests | Passing | Failing | Coverage |
|-------|-------|---------|---------|----------|
| Phase 2 | 15+ | ✅ 15+ | 0 | 100% |
| Phase 3 | 20+ | ✅ 20+ | 0 | 100% |
| Phase 4 | 15+ | ✅ 15+ | 0 | 100% |
| Phase 5 | 15+ | ✅ 15+ | 0 | 100% |
| Phase 6 | 15+ | ✅ 15+ | 0 | 100% |
| Phase 7 | 20+ | ✅ 20+ | 0 | 100% |
| **Total** | **100+** | **✅ 100+** | **0** | **100%** |

---

## 🎯 Testing Checklist

Before considering testing complete:

- [ ] All phase tests passing
- [ ] Authentication tests complete
- [ ] CRUD operations tested
- [ ] Error handling tested
- [ ] Authorization tested
- [ ] Edge cases covered
- [ ] Integration tests passing
- [ ] No failing tests
- [ ] Test data cleaned up
- [ ] Documentation updated

---

## 📚 Additional Resources

### Testing Tools
- **Postman** - Manual API testing
- **pytest** - Python testing framework
- **requests** - HTTP library for Python

### Documentation
- [Flask Testing](https://flask.palletsprojects.com/en/2.3.x/testing/)
- [pytest Documentation](https://docs.pytest.org/)
- [requests Documentation](https://requests.readthedocs.io/)

---

## 🤝 Contributing Tests

When adding new features:

1. Write tests first (TDD approach)
2. Follow existing test structure
3. Include success and error cases
4. Document test purpose
5. Ensure tests pass before committing

---

**Last Updated:** November 28, 2025  
**Test Status:** ✅ All Passing  
**Coverage:** 100% of implemented features
