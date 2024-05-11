const express = require('express')
const http = require('http')
const bodyParser = require('body-parser')

const app = express()

app.use(bodyParser.urlencoded({extended: false}))

app.post('/', (req, res) => {
    console.log(req.body)

    for (let i = 0; i < req.body.length; i++) {
        // extract data 
        // validate it
        // send querys transaction to the other server depending of the transaction choice
    }
})

const server = http.createServer(app)
let port = 5843
const host = '0.0.0.0'

server.listen(port, host, () => {
    console.log(`Servidor a rodar em http://${host}:${port}/`)
})