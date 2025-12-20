const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

app.get('/', (req, res) => {
    res.json({ message: 'GitHub Actions + Docker is working!', status: 'success' });
});

app.get('/health', (req, res) => {
    res.json({ status: 'up' });
});

if (require.main === module) {
    app.listen(PORT, () => {
        console.log(`Server running on port ${PORT}`);
    });
}

module.exports = app;
