const request = require('supertest');
const app = require('../src/index');

describe('API Tests', () => {
    describe('GET /', () => {
        it('should return API information', async () => {
            const response = await request(app).get('/');

            expect(response.status).toBe(200);
            expect(response.body).toHaveProperty('message');
            expect(response.body).toHaveProperty('version');
            expect(response.body).toHaveProperty('endpoints');
        });
    });

    describe('GET /health', () => {
        it('should return healthy status', async () => {
            const response = await request(app).get('/health');

            expect(response.status).toBe(200);
            expect(response.body.status).toBe('healthy');
            expect(response.body).toHaveProperty('timestamp');
            expect(response.body).toHaveProperty('uptime');
        });
    });

    describe('GET /api/users', () => {
        it('should return all users', async () => {
            const response = await request(app).get('/api/users');

            expect(response.status).toBe(200);
            expect(response.body.success).toBe(true);
            expect(response.body).toHaveProperty('data');
            expect(Array.isArray(response.body.data)).toBe(true);
            expect(response.body.count).toBeGreaterThan(0);
        });
    });

    describe('GET /api/users/:id', () => {
        it('should return a user by ID', async () => {
            const response = await request(app).get('/api/users/1');

            expect(response.status).toBe(200);
            expect(response.body.success).toBe(true);
            expect(response.body.data).toHaveProperty('id');
            expect(response.body.data).toHaveProperty('name');
            expect(response.body.data).toHaveProperty('email');
        });

        it('should return 404 for non-existent user', async () => {
            const response = await request(app).get('/api/users/9999');

            expect(response.status).toBe(404);
            expect(response.body.success).toBe(false);
        });
    });

    describe('POST /api/users', () => {
        it('should create a new user', async () => {
            const newUser = {
                name: 'Test User',
                email: 'test@example.com',
                role: 'user'
            };

            const response = await request(app)
                .post('/api/users')
                .send(newUser);

            expect(response.status).toBe(201);
            expect(response.body.success).toBe(true);
            expect(response.body.data).toHaveProperty('id');
            expect(response.body.data.name).toBe(newUser.name);
            expect(response.body.data.email).toBe(newUser.email);
        });

        it('should return 400 for missing required fields', async () => {
            const response = await request(app)
                .post('/api/users')
                .send({ name: 'Test' });

            expect(response.status).toBe(400);
            expect(response.body.success).toBe(false);
        });
    });

    describe('PUT /api/users/:id', () => {
        it('should update an existing user', async () => {
            const updates = {
                name: 'Updated Name'
            };

            const response = await request(app)
                .put('/api/users/1')
                .send(updates);

            expect(response.status).toBe(200);
            expect(response.body.success).toBe(true);
            expect(response.body.data.name).toBe(updates.name);
        });

        it('should return 404 for non-existent user', async () => {
            const response = await request(app)
                .put('/api/users/9999')
                .send({ name: 'Test' });

            expect(response.status).toBe(404);
            expect(response.body.success).toBe(false);
        });
    });

    describe('DELETE /api/users/:id', () => {
        it('should delete an existing user', async () => {
            const response = await request(app).delete('/api/users/2');

            expect(response.status).toBe(200);
            expect(response.body.success).toBe(true);
        });

        it('should return 404 for non-existent user', async () => {
            const response = await request(app).delete('/api/users/9999');

            expect(response.status).toBe(404);
            expect(response.body.success).toBe(false);
        });
    });

    describe('404 Handler', () => {
        it('should return 404 for unknown routes', async () => {
            const response = await request(app).get('/unknown-route');

            expect(response.status).toBe(404);
            expect(response.body.success).toBe(false);
        });
    });
});
