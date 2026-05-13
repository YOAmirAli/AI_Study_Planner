# 🔐 Environment Variables Documentation

Complete guide to all environment variables used in the AI Study Planner backend.

---

## 📋 Required Variables

### Flask Configuration

#### `FLASK_ENV`
- **Description:** Application environment mode
- **Values:** `development` | `production` | `testing`
- **Default:** `development`
- **Example:** `FLASK_ENV=development`
- **Notes:** 
  - Use `development` for local development (enables debug mode)
  - Use `production` for deployed application (disables debug)
  - Use `testing` for running tests

#### `SECRET_KEY`
- **Description:** Flask secret key for session management and security
- **Type:** String (32+ random characters recommended)
- **Required:** Yes
- **Example:** `SECRET_KEY=your-super-secret-key-change-this-in-production`
- **Security:** 
  - NEVER commit this to version control
  - Use different keys for development and production
  - Generate with: `python -c "import secrets; print(secrets.token_hex(32))"`

#### `JWT_SECRET_KEY`
- **Description:** Secret key for JWT token generation and validation
- **Type:** String (32+ random characters recommended)
- **Required:** Yes
- **Example:** `JWT_SECRET_KEY=your-jwt-secret-key-change-this-too`
- **Security:**
  - Must be different from `SECRET_KEY`
  - NEVER commit to version control
  - Generate with: `python -c "import secrets; print(secrets.token_hex(32))"`

---

### Database Configuration

#### `DATABASE_URL`
- **Description:** MySQL database connection string
- **Format:** `mysql+pymysql://username:password@host:port/database`
- **Required:** Yes
- **Examples:**
  - Local: `DATABASE_URL=mysql+pymysql://root:password@localhost:3306/ai_study_planner`
  - Remote: `DATABASE_URL=mysql+pymysql://user:pass@db.example.com:3306/dbname`
- **Notes:**
  - Ensure MySQL server is running
  - Database must exist before running application
  - Use strong passwords in production

---

### AI API Configuration

You need **ONE** of the following AI API keys:

#### `OPENAI_API_KEY`
- **Description:** OpenAI API key for GPT-4 access
- **Required:** Yes (if not using Groq)
- **Example:** `OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx`
- **Get Key:** https://platform.openai.com/api-keys
- **Features:**
  - Text summarization
  - Quiz generation
  - Flashcard creation
  - Topic extraction
- **Cost:** Pay-per-use (check OpenAI pricing)

#### `GROQ_API_KEY`
- **Description:** Groq API key for fast AI inference
- **Required:** Yes (if not using OpenAI)
- **Example:** `GROQ_API_KEY=gsk_xxxxxxxxxxxxx`
- **Get Key:** https://console.groq.com/keys
- **Features:**
  - Same as OpenAI but faster
  - Free tier available
  - Lower latency
- **Cost:** Free tier + paid plans

---

### CORS Configuration

#### `CORS_ORIGINS`
- **Description:** Allowed origins for Cross-Origin Resource Sharing
- **Type:** Comma-separated list of URLs
- **Required:** Yes
- **Examples:**
  - Development: `CORS_ORIGINS=http://localhost:3000`
  - Multiple: `CORS_ORIGINS=http://localhost:3000,http://localhost:3001`
  - Production: `CORS_ORIGINS=https://yourdomain.com`
- **Security:**
  - NEVER use `*` in production
  - Only list trusted frontend domains
  - Include protocol (http/https)

---

## 📧 Optional Variables

### Email Configuration (for notifications)

#### `MAIL_SERVER`
- **Description:** SMTP server hostname
- **Required:** No (optional feature)
- **Examples:**
  - Gmail: `MAIL_SERVER=smtp.gmail.com`
  - Outlook: `MAIL_SERVER=smtp-mail.outlook.com`
  - SendGrid: `MAIL_SERVER=smtp.sendgrid.net`

#### `MAIL_PORT`
- **Description:** SMTP server port
- **Required:** No
- **Common Values:**
  - TLS: `587`
  - SSL: `465`
- **Example:** `MAIL_PORT=587`

#### `MAIL_USERNAME`
- **Description:** Email account username
- **Required:** No
- **Example:** `MAIL_USERNAME=your-email@gmail.com`

#### `MAIL_PASSWORD`
- **Description:** Email account password or app password
- **Required:** No
- **Example:** `MAIL_PASSWORD=your-app-specific-password`
- **Notes:**
  - For Gmail, use App Password (not regular password)
  - Enable 2FA and generate app password in Google Account settings

#### `MAIL_USE_TLS`
- **Description:** Use TLS encryption
- **Values:** `True` | `False`
- **Default:** `True`
- **Example:** `MAIL_USE_TLS=True`

#### `MAIL_USE_SSL`
- **Description:** Use SSL encryption
- **Values:** `True` | `False`
- **Default:** `False`
- **Example:** `MAIL_USE_SSL=False`

---

## 🔧 Development vs Production

### Development Environment (.env)
```env
FLASK_ENV=development
SECRET_KEY=dev-secret-key-not-for-production
JWT_SECRET_KEY=dev-jwt-key-not-for-production
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/ai_study_planner
GROQ_API_KEY=gsk_your_groq_key_here
CORS_ORIGINS=http://localhost:3000
```

### Production Environment
```env
FLASK_ENV=production
SECRET_KEY=<generate-strong-random-key>
JWT_SECRET_KEY=<generate-different-strong-key>
DATABASE_URL=mysql+pymysql://user:strong_pass@prod-db.com:3306/ai_study_planner
OPENAI_API_KEY=sk-proj-your_production_key
CORS_ORIGINS=https://yourdomain.com
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=noreply@yourdomain.com
MAIL_PASSWORD=<app-specific-password>
MAIL_USE_TLS=True
```

---

## 🛡️ Security Best Practices

### 1. Never Commit .env Files
```bash
# Add to .gitignore
.env
.env.local
.env.production
```

### 2. Use Strong Keys
```bash
# Generate secure keys
python -c "import secrets; print(secrets.token_hex(32))"
```

### 3. Different Keys Per Environment
- Development keys ≠ Production keys
- Each environment should have unique secrets

### 4. Rotate Keys Regularly
- Change production keys every 90 days
- Rotate immediately if compromised

### 5. Limit Access
- Only authorized personnel should have production keys
- Use environment variable management tools (AWS Secrets Manager, etc.)

---

## 📝 Setting Environment Variables

### Local Development (.env file)
```bash
# Create .env file
cp .env.example .env

# Edit with your values
nano .env  # or use any text editor
```

### Production (Platform-specific)

#### Render.com
1. Go to Dashboard → Your Service
2. Click "Environment"
3. Add each variable as Key-Value pair

#### Railway.app
1. Go to Project → Variables
2. Click "New Variable"
3. Add each variable

#### Heroku
```bash
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=your-secret-key
# etc.
```

#### Docker
```bash
docker run -e FLASK_ENV=production \
           -e SECRET_KEY=your-key \
           your-image
```

---

## ✅ Verification Checklist

Before deploying, verify:

- [ ] All required variables are set
- [ ] Keys are strong and unique
- [ ] Database connection string is correct
- [ ] AI API key is valid and has credits
- [ ] CORS origins match your frontend domain
- [ ] Email configuration is tested (if using)
- [ ] No sensitive data in version control
- [ ] Production uses different keys than development

---

## 🧪 Testing Configuration

```bash
# Test database connection
python -c "from app.config.database import db; print('DB OK')"

# Test environment loading
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('FLASK_ENV'))"

# Verify all required vars
python verify_setup.py
```

---

## 📞 Troubleshooting

### "Missing environment variable" error
- Check .env file exists
- Verify variable name spelling
- Ensure no extra spaces around `=`

### Database connection fails
- Verify DATABASE_URL format
- Check MySQL server is running
- Test credentials with mysql client

### AI features not working
- Verify API key is correct
- Check API key has credits/quota
- Test key with curl or Postman

---

**Last Updated:** November 28, 2025  
**Version:** 1.0.0
