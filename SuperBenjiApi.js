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

app.use(bodyParser.json() , cors())

app.post('/crawl', (req, res) => {
    const { url } = req.body;

    if (!url) {
        return res.status(400).json({ error: 'URL is required' });
    }

    // Pass the URL to the Python script
    const pythonProcess = exec(`/appl/SuperBenjiAPIServer/SuperBenjiUbuntuServer/env/bin/python3 /application/SuperBenjiUbuntuServer/webCrawler.py "${url}"`, (error, stdout, stderr) => {
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

app.post('/query', (req, res) => {
    
})

app.get('/', (req, res) => {
    res.send('Welcome to Nodejs API Project')
})

app.get('/hello' , (req, res) => {
    res.send('Hello World!!')
})

https.createServer(options, app).listen(port, () => {
    console.log('HTTPS server is running on port 8080')
})
