# E-Commerce BFF (Backend for Frontend)

Node.js Express server that orchestrates communication between the React frontend and Python microservices.

## 🚀 Tech Stack

- **Node.js 20** - Runtime
- **Express** - Web framework
- **Axios** - HTTP client for microservices
- **Winston** - Logging
- **Helmet** - Security headers
- **JWT** - Authentication
- **Rate Limiting** - DDoS protection

## 📦 Installation

```bash
npm install
```

## 🛠️ Development

```bash
# Start with hot reload
npm run dev

# Server runs on: http://localhost:3000
```

## 🏗️ Production

```bash
npm start
```

## 📁 Project Structure

```
src/
├── config/          # Configuration files
│   └── logger.js   # Winston logger setup
├── middleware/      # Express middleware
│   ├── correlationId.js  # Distributed tracing
│   ├── errorHandler.js   # Global error handling
│   └── rateLimiter.js    # Rate limiting
├── routes/          # API routes
│   └── index.js    # Main routes
├── services/        # Service layer (calls microservices)
├── utils/          # Utility functions
├── app.js          # Express app configuration
└── server.js       # Server entry point
```

## 🔌 API Endpoints

### Health & Status

- `GET /health` - Health check
- `GET /ready` - Readiness check
- `GET /` - API information

### Coming Soon

- `POST /api/auth/login` - User authentication
- `GET /api/products` - Get products
- `POST /api/orders` - Create order
- `GET /api/users/me` - Get current user

## 🌍 Environment Variables

Create a `.env` file:

```bash
NODE_ENV=development
PORT=3000
ALLOWED_ORIGINS=http://localhost:5173

# Microservices
USERS_SERVICE_URL=http://localhost:8001
ORDERS_SERVICE_URL=http://localhost:8002
INVENTORY_SERVICE_URL=http://localhost:8004
PAYMENTS_SERVICE_URL=http://localhost:8003

# JWT
JWT_SECRET=your-secret-key
JWT_EXPIRES_IN=7d
```

## 🔐 Security Features

- ✅ Helmet for security headers
- ✅ CORS configuration
- ✅ Rate limiting (100 req/15min by default)
- ✅ Input validation
- ✅ JWT authentication
- ✅ Correlation IDs for tracing

## 📊 Logging

All requests are logged with:

- Correlation ID
- Timestamp
- HTTP method and path
- Response status
- Processing time

Example log:

```json
{
  "level": "info",
  "message": "GET /api/products 200 45ms",
  "correlationId": "a1b2c3d4-e5f6-7890",
  "timestamp": "2025-11-02T12:00:00.000Z"
}
```

## 🔄 Request Flow

```
Frontend (React)
    ↓
BFF (Node.js) - Add correlation ID
    ↓
Microservices (Python FastAPI)
    ↓
MongoDB Atlas
```

## 🧪 Testing

```bash
# Health check
curl http://localhost:3000/health

# API info
curl http://localhost:3000/

# Test with correlation ID
curl -H "X-Correlation-ID: test-123" http://localhost:3000/health
```

## 🐛 Troubleshooting

### Port already in use

```bash
# Find process on port 3000
lsof -i :3000

# Kill it
kill -9 <PID>
```

### Module not found

```bash
rm -rf node_modules package-lock.json
npm install
```

## 📚 Key Patterns

### BFF Pattern

The BFF acts as an aggregation layer:

- Combines multiple microservice calls
- Transforms data for frontend needs
- Handles authentication/authorization
- Provides a single API contract

### Correlation ID

Every request gets a unique ID that flows through all services:

```javascript
X-Correlation-ID: 550e8400-e29b-41d4-a716-446655440000
```

### Error Handling

All errors are caught and returned consistently:

```json
{
  "success": false,
  "error": "Error message",
  "correlationId": "..."
}
```

---
