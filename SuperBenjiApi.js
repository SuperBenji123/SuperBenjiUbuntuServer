const bodyParser = require('body-parser')
const { exec } = require('child_process')
const cors = require('cors')
const express = require('express')
const port = process.env.PORT || 8080
const app = express()
const Nylas = require('nylas')
const https = require('https')
const fs = require('fs')

const options = {
    key: fs.readFileSync('/etc/letsencrypt/live/server.superbenji.net/privkey.pem'),
    cert: fs.readFileSync('/etc/letsencrypt/live/server.superbenji.net/cert.pem'),
    ca: fs.readFileSync('/etc/letsencrypt/live/server.superbenji.net/chain.pem')
}

const nylasConfig = {
    clientId: '46d347f8-7c14-4cb3-a4ad-fa29bfeebbff',
    callbackURI:'https://server.superbenji.net:8080/oauth/exchange',
    apiKey: 'nyk_v0_IVXV8oCs6cGNMk3hLXb09Osu2mRP1zoZmKO6m3j2Uw6dnZZxZSVYCKUuUuH1zAlt',
    apiURI: 'https://api.eu.nylas.com'
}

const nylasInstance = new Nylas.default({
    apiKey: nylasConfig.apiKey,
    apiUri: nylasConfig.apiURI
})

app.use(bodyParser.json() , cors())

app.post('/crawl', (req, res) => {
    const { url } = req.body

    if (!url) {
        return res.status(400).json({ error: 'URL is required' })
    }

    const pythonProcess = exec(`python3 webCrawler.py ${url}`, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error: ${error.message}`)
            return res.status(500).json({ error: 'Failed to execute Python script' })
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

    if (!code) {
        res.status(400).send('No authorisation code returned by Nylas')
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

app.get('/', (req, res) => {
    res.send('Welcome to Nodejs API Project')
})

app.get('/hello' , (req, res) => {
    res.send('Hello World!!')
})

https.createServer(options, app).listen(port, () => {
    console.log('HTTPS server is running on port 8080')
})
