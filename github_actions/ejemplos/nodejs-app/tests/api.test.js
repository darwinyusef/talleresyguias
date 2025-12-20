const request = require('supertest');
const app = require('../src/index');

describe('API Tests', () => {
    test('GET / should return success message', async () => {
        const res = await request(app).get('/');
        expect(res.statusCode).toEqual(200);
        expect(res.body.status).toEqual('success');
    });

    test('GET /health should return up', async () => {
        const res = await request(app).get('/health');
        expect(res.statusCode).toEqual(200);
        expect(res.body.status).toEqual('up');
    });
});
