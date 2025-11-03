# Users Service

Python FastAPI microservice for user management and authentication.

## 🚀 Features

- User registration with email validation
- Password hashing with Argon2
- JWT authentication
- MongoDB Atlas integration
- Health and readiness checks
- Correlation ID for distributed tracing
- Interactive API documentation

## 📦 Tech Stack

- **Python 3.13**
- **FastAPI** - Modern async web framework
- **Motor** - Async MongoDB driver
- **Pydantic** - Data validation
- **Argon2** - Password hashing
- **PyJWT** - JWT tokens
- **MongoDB Atlas** - Cloud database

## 🛠️ Setup

```bash
# Create virtual environment
python -m venv venv
source venv/Scripts/activate  # Windows Git Bash

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your MongoDB Atlas connection string
```

## 🌍 Environment Variables

```bash
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/platform_db
MONGODB_DB_NAME=platform_db
SERVICE_NAME=users
LOG_LEVEL=INFO
JWT_SECRET=your-secret-key
```

## 🚀 Running

```bash
# Development with auto-reload
python -m app.main

# Production
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 🔌 API Endpoints

### Public Endpoints

- `GET /health` - Health check
- `GET /ready` - Readiness check (checks MongoDB connection)
- `POST /api/v1/users/register` - Register new user
- `POST /api/v1/users/login` - Login and get JWT token

### Protected Endpoints (require JWT)

- `GET /api/v1/users/me` - Get current user profile
- `PUT /api/v1/users/me` - Update user profile

## 📚 API Documentation

Interactive docs available at: http://localhost:8000/docs

## 🧪 Testing

### Register a User

```bash
curl -X POST http://localhost:8000/api/v1/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "name": "John Doe",
    "password": "securepass123",
    "phone": "+1234567890"
  }'
```

### Login

```bash
curl -X POST "http://localhost:8000/api/v1/users/login?email=user@example.com&password=securepass123"
```

### Get Profile (with JWT)

```bash
curl http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## 🏗️ Project Structure

```
services/users/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI app and startup
│   ├── config.py        # Configuration settings
│   ├── database.py      # MongoDB connection
│   ├── models.py        # Pydantic models
│   ├── routes.py        # API endpoints
│   └── auth.py          # Authentication logic
├── tests/
│   └── __init__.py
├── .env                 # Environment variables (not in git)
├── .env.example         # Example env file
├── Dockerfile          # Container definition
├── requirements.txt    # Python dependencies
└── README.md
```

## ✅ What's Working

- ✅ User registration with validation
- ✅ Secure password hashing (Argon2)
- ✅ JWT token generation
- ✅ MongoDB Atlas connection
- ✅ Health checks
- ✅ Correlation ID tracking
- ✅ Interactive API docs
- ✅ CORS configuration

## 🔐 Security Features

- Passwords hashed with Argon2 (never stored plain)
- JWT tokens with expiration
- Email validation
- Input validation with Pydantic
- CORS configured for known origins

## 🐛 Troubleshooting

### MongoDB Connection Issues

- Check your connection string in .env
- Verify IP whitelist in Atlas (Network Access)
- Ensure user credentials are correct

### Virtual Environment Issues

- Make sure you're using Python 3.13
- Activate venv before installing packages

---

**Built using Python + FastAPI**
