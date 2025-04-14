const bodyParser = require('body-parser')
const { exec } = require('child_process')
const cors = require('cors')
const express = require('express')
const port = process.env.PORT || 8080
const app = express()
const https = require('https')
const fs = require('fs')

const options = {
    key: fs.readFileSync('/etc/letsencrypt/live/api.superbenji.net/privkey.pem'),
    cert: fs.readFileSync('/etc/letsencrypt/live/api.superbenji.net/fullchain.pem')
}

app.use(bodyParser.json(), cors())

// POST /crawl route - already existing
app.post('/crawl', (req, res) => {
    const { url } = req.body;

    if (!url) {
        return res.status(400).json({ error: 'URL is required' });
    }

    const pythonProcess = exec(`/appl/SuperBenjiAPIServer/SuperBenjiUbuntuServer/env/bin/python3 /appl/SuperBenjiAPIServer/SuperBenjiUbuntuServer/webCrawler.py "${url}"`, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error: ${error.message}`);
            return res.status(500).json({ error: 'Failed to execute Python script', details: error.message });
        }
        if (stderr) {
            console.error(`Stderr: ${stderr}`);
            return res.status(500).json({ error: 'Python script error', details: stderr });
        }
        res.status(200).json({ result: stdout.trim() });
    });
});

// ✅ New POST /benji route
app.post('/benji', (req, res) => {
    const inputData = req.body.data || '';

    const nodeProcess = exec(`node /appl/SuperBenjiAPIServer/SuperBenjiUbuntuServer/benji_call_API_server.js "${inputData}"`, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error: ${error.message}`);
            return res.status(500).json({ error: 'Failed to execute benji_call_API_server.js', details: error.message });
        }
        if (stderr) {
            console.error(`Stderr: ${stderr}`);
            return res.status(500).json({ error: 'benji_call_API_server.js error', details: stderr });
        }
        res.status(200).json({ result: stdout.trim() });
    });
});

// You can add logic to /query here if needed
app.post('/query', (req, res) => {
    res.status(200).json({ message: 'Query endpoint placeholder' });
});

app.get('/', (req, res) => {
    res.send('Welcome to Nodejs API Project');
});

app.get('/hello', (req, res) => {
    res.send('Hello World!!');
});

// Start HTTPS server
https.createServer(options, app).listen(port, () => {
    console.log('HTTPS server is running on port ' + port);
});
