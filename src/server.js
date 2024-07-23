// server.js
const express = require('express');
const bodyParser = require('body-parser');
const { sendFallNotification } = require('./emailService');

const app = express();
const port = 3000;

app.use(bodyParser.json());

app.post('/send-fall-notification', async (req, res) => {
    const { toEmail, imagePath } = req.body;

    try {
        await sendFallNotification(toEmail, imagePath);
        res.status(200).send('Email sent successfully');
    } catch (error) {
        res.status(500).send('Error sending email');
    }
});

app.listen(port, () => {
    console.log(`Server running on http://localhost:${port}`);
});
