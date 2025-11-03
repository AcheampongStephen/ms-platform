const express = require('express');
const router = express.Router();

// Health check
router.get('/health', (req, res) => {
  res.json({ 
    status: 'healthy',
    timestamp: new Date().toISOString(),
    service: 'bff'
  });
});

// Readiness check
router.get('/ready', async (req, res) => {
  // TODO: Check connectivity to backend services
  res.json({ 
    status: 'ready',
    timestamp: new Date().toISOString(),
    service: 'bff'
  });
});

// API info
router.get('/', (req, res) => {
  res.json({
    name: 'E-Commerce BFF API',
    version: '1.0.0',
    description: 'Backend for Frontend - Orchestrates microservices',
    endpoints: {
      health: '/health',
      ready: '/ready',
      api: '/api/*'
    }
  });
});

module.exports = router;
