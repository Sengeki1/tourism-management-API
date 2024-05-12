const express = require('express')
const http = require('http')
const bodyParser = require('body-parser')

const app = express()

app.use(bodyParser.urlencoded({extended: false}))

app.post('/transaction', (req, res) => {
    console.log(req.body)

    Object.keys(req.body).forEach(key => {
        // extract data 
        // validate it
        // send querys transaction to the other server depending of the transaction choice
    })
})

// send STATUS CODE to the client refering if the transaction was successfull

const server = http.createServer(app)
let port = 5843
const host = '0.0.0.0'

server.listen(port, host, () => {
    console.log(`Servidor a rodar em http://${host}:${port}/`)
})