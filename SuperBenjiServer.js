const bodyParser = require('body-parser')
const { exec } = require('child_process')
const cors = require('cors')
const express = require('express')
const port = process.env.PORT || 443
const app = express()
const Nylas = require('nylas')
const https = require('https')
const fs = require('fs')

require('dotenv').config()

const options = {
    key: fs.readFileSync('/appl/SuperBenji/certs/privkey.pem'),
    cert: fs.readFileSync('/appl/SuperBenji/certs/fullchain.pem')
}

const nylasConfig = {
    clientId : process.env.CLIENT_ID,
    callbackURI : process.env.CALLBACK_URI,
    apiKey: process.env.NYLAS_API_KEY,
    apiURI: process.env.NYLAS_API_URL,
}

const nylasInstance = new Nylas.default({
    apiKey: nylasConfig.apiKey,
    apiUri: nylasConfig.apiURI
})

app.use(bodyParser.json() , cors())
app.get('/.well-known/microsoft-identity-association.json', (req, res) => {
    res.setHeader('Content-Type', 'application/json');
    res.sendFile(__dirname + '/.well-known/microsoft-identity-association.json');
});

app.get('/health', (req, res) => {
    res.status(200).json({
        status: 'healthy',
        uptime: process.uptime(),
        memory: process.memoryUsage(),
        timestamp: new Date().toISOString()
    });
});

app.post('/crawl', (req, res) => {
    const { url } = req.body
    if (!url) {
        return res.status(400).json({ error: 'URL is required' })
    }
    const pythonProcess = exec(`cd /appl/SuperBenji && timeout 300 /appl/SuperBenji/myenv/bin/python3 webCrawler.py "${url}"`, { timeout: 300000 }, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error: ${error.message}`)
            return res.status(500).json({ error: 'Failed to execute Python script', details: error.message })
        }
        if (stderr) {
            console.error(`Stderr: ${stderr}`)
            return res.status(500).json({ error: 'Python script error', details: stderr })
        }
        res.status(200).json({ result: stdout.trim() })
    })
})

app.get('/nylas/auth', (req, res) => {
    const authURL = nylasInstance.auth.urlForOAuth2({
        clientId : nylasConfig.clientId,
        redirectUri: nylasConfig.callbackURI,
    })

    console.log('Redirecting to :', authURL)
    res.redirect(authURL)
})

app.get('/oauth/exchange', async (req, res) => {
    const code = req.query.code
    console.log(req)
    const fullUrl = `${req.protocol}://${req.get('host')}${req.originalUrl}`;
    console.log(fullUrl);

    if (!code) {
        res.status(400).send('No authorisation code returned by Nylas' + fullUrl)
        return
    }

    try {
        const response = await nylasInstance.auth.exchangeCodeForToken({
            clientId: nylasConfig.clientId,
            redirectUri: nylasConfig.callbackURI,
            code
        })

        const { grantId } = response
        console.log('Grant ID:', grantId)
        res.redirect('https://superbenji.softr.app/email-connection-success')
    } catch (error) {
        console.error('Error exchanging code for token:', error)
        res.status(500).send('Failed to exchange authorisation code for token')
    }
})

const nylasTestingConfig = {
    clientId: 'fdb5107e-c36b-4858-a105-a68a7198904f',
    callbackURI:'https://server.superbenji.net/oauth/exchange/microsoft',
    apiKey: 'nyk_v0_ByThuwL4BmXYPcrQrCBfOSR88yicoWukudh6UKPDCUQAokZXKcA41mCUTxjtkNxD',
    apiURI: 'https://api.eu.nylas.com'
}

const nylasTestingInstance = new Nylas.default({
    apiKey: nylasTestingConfig.apiKey,
    apiUri: nylasTestingConfig.apiURI
})

app.get('/nylas/auth/microsoft', (req, res) => {
    const testingAuthURL = nylasTestingInstance.auth.urlForOAuth2({
        clientId : nylasTestingConfig.clientId,
        redirectUri: nylasTestingConfig.callbackURI,
    })

    console.log('Redirecting to :', testingAuthURL)
    res.redirect(testingAuthURL)
})

app.get('/oauth/exchange/microsoft', async (req, res) => {
    const code = req.query.code

    if (!code) {
        res.status(400).send('No authorisation code returned by Nylas')
        return
    }

    try {
        const response = await nylasTestingInstance.auth.exchangeCodeForToken({
            clientId: nylasTestingConfig.clientId,
            redirectUri: nylasTestingConfig.callbackURI,
            code
        })

        const { grantId } = response
        console.log('Grant ID:', grantId)
        res.redirect('https://superbenji.softr.app/email-connection-success')
    } catch (error) {
        console.error('Error exchanging code for token:', error)
        res.status(500).send('Failed to exchange authorisation code for token' + error)
    }
})

app.get('/', (req, res) => {
    res.send('Welcome to Nodejs API Project')
})

app.get('/hello' , (req, res) => {
    res.send('Hello World!!')
})

https.createServer(options, app).listen(port,'0.0.0.0', () => {
    console.log('HTTPS server is running on port 443')
})
