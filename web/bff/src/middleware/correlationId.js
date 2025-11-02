const { v4: uuidv4 } = require('uuid');
const logger = require('../config/logger');

function correlationIdMiddleware(req, res, next) {
  const correlationId = req.headers['x-correlation-id'] || uuidv4();
  
  req.correlationId = correlationId;
  res.setHeader('X-Correlation-ID', correlationId);
  
  // Add to logger context
  req.log = logger.child({ correlationId });
  
  next();
}

module.exports = { correlationIdMiddleware };
