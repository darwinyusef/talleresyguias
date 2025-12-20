const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const logger = require('./utils/logger');

const app = express();
const PORT = process.env.PORT || 3000;
const NODE_ENV = process.env.NODE_ENV || 'development';

// Middleware
app.use(helmet());
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(morgan('combined', { stream: { write: message => logger.info(message.trim()) } }));

// In-memory database (para ejemplo)
let users = [
    { id: 1, name: 'Juan Pérez', email: 'juan@example.com', role: 'admin' },
    { id: 2, name: 'María García', email: 'maria@example.com', role: 'user' },
    { id: 3, name: 'Carlos López', email: 'carlos@example.com', role: 'user' }
];

// Routes

// Root endpoint
app.get('/', (req, res) => {
    res.json({
        message: 'API de Usuarios - Jenkins CI/CD Demo',
        version: '1.0.0',
        environment: NODE_ENV,
        endpoints: {
            health: '/health',
            users: '/api/users',
            user: '/api/users/:id'
        }
    });
});

// Health check
app.get('/health', (req, res) => {
    res.json({
        status: 'healthy',
        timestamp: new Date().toISOString(),
        uptime: process.uptime(),
        environment: NODE_ENV
    });
});

// Get all users
app.get('/api/users', (req, res) => {
    logger.info('GET /api/users - Fetching all users');
    res.json({
        success: true,
        count: users.length,
        data: users
    });
});

// Get user by ID
app.get('/api/users/:id', (req, res) => {
    const id = parseInt(req.params.id);
    const user = users.find(u => u.id === id);

    if (!user) {
        logger.warn(`GET /api/users/${id} - User not found`);
        return res.status(404).json({
            success: false,
            message: 'Usuario no encontrado'
        });
    }

    logger.info(`GET /api/users/${id} - User found`);
    res.json({
        success: true,
        data: user
    });
});

// Create user
app.post('/api/users', (req, res) => {
    const { name, email, role } = req.body;

    // Validación básica
    if (!name || !email) {
        return res.status(400).json({
            success: false,
            message: 'Nombre y email son requeridos'
        });
    }

    const newUser = {
        id: users.length + 1,
        name,
        email,
        role: role || 'user'
    };

    users.push(newUser);
    logger.info(`POST /api/users - User created: ${newUser.id}`);

    res.status(201).json({
        success: true,
        message: 'Usuario creado exitosamente',
        data: newUser
    });
});

// Update user
app.put('/api/users/:id', (req, res) => {
    const id = parseInt(req.params.id);
    const userIndex = users.findIndex(u => u.id === id);

    if (userIndex === -1) {
        logger.warn(`PUT /api/users/${id} - User not found`);
        return res.status(404).json({
            success: false,
            message: 'Usuario no encontrado'
        });
    }

    const { name, email, role } = req.body;

    users[userIndex] = {
        ...users[userIndex],
        ...(name && { name }),
        ...(email && { email }),
        ...(role && { role })
    };

    logger.info(`PUT /api/users/${id} - User updated`);

    res.json({
        success: true,
        message: 'Usuario actualizado exitosamente',
        data: users[userIndex]
    });
});

// Delete user
app.delete('/api/users/:id', (req, res) => {
    const id = parseInt(req.params.id);
    const userIndex = users.findIndex(u => u.id === id);

    if (userIndex === -1) {
        logger.warn(`DELETE /api/users/${id} - User not found`);
        return res.status(404).json({
            success: false,
            message: 'Usuario no encontrado'
        });
    }

    users.splice(userIndex, 1);
    logger.info(`DELETE /api/users/${id} - User deleted`);

    res.json({
        success: true,
        message: 'Usuario eliminado exitosamente'
    });
});

// 404 handler
app.use((req, res) => {
    res.status(404).json({
        success: false,
        message: 'Endpoint no encontrado'
    });
});

// Error handler
app.use((err, req, res, next) => {
    logger.error(`Error: ${err.message}`);
    res.status(500).json({
        success: false,
        message: 'Error interno del servidor',
        error: NODE_ENV === 'development' ? err.message : undefined
    });
});

// Start server
if (require.main === module) {
    app.listen(PORT, () => {
        logger.info(`🚀 Server running on port ${PORT}`);
        logger.info(`📝 Environment: ${NODE_ENV}`);
        logger.info(`🔗 Health check: http://localhost:${PORT}/health`);
    });
}

module.exports = app;
