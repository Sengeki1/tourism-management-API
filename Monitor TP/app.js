const express = require('express')
const valid = require('card-validator')
const http = require('http')
const bodyParser = require('body-parser')

const app = express()

app.use(bodyParser.urlencoded({extended: false}))

function countingDigits(num) {
    return parseInt(String(num).split('').reduce(
        (count, digit) => count + 1, 0
    ))
}

app.post('/transaction', (req, res) => {
    console.log(req.body)

    Object.keys(req.body).forEach(key => {
        if (typeof req.body[key] != 'number') { // check for filled scopes
            if (typeof req.body[key] === "string" && req.body[key].trim() === "") {
                res.statusCode = 406
                return res.json({status: "error: missing fields"})
            }
        }

        if (key === age) {
            if (countingDigits(req.body[key]) >= 3 || countingDigits(req.body[key]) < 1) {
                res.statusCode = 406
                return res.json({status: "error: invalid age"})
            }
        }
    })

    if (req.body.card) {
        Object.keys(req.body.card).forEach(key => {
            if (key === "expiration_date") {
                if (req.body.card[key].includes('/')) {
                    const validation = req.body.card[key].split('/')
                    for (let i = 0; i < validation.length; i++) {
                        let value = parseInt(validation[i])
                        if (validation.length < 2 && typeof value != "number" || validation.length > 2 && typeof value != "number" || typeof value != "number") {
                            res.statusCode = 406
                            return res.json({status: "error: wrong validation date"})
                        }
                    }
                } else {
                    res.statusCode = 403
                    return res.json({status: "error: invalid operation"})
                }
            }
            if (key === "number") {
                var numberValid = valid.number(req.body.card[key])
                if (!numberValid.isValid) {
                    res.statusCode = 406
                    return res.json({status: "error: card invalid"})
                }
            }
        }) 
    }
    
    var options, post_data, options_get
    Object.keys(req.body).forEach(key => {
        if (key === "transactionChoice" && req.body[key] === "Hotel") {
            post_data = {
                nome_cliente: req.body.name,
                email_client: req.body.email,
                telefone_cliente: req.body.phone,
                tipo_quarto: req.body.room,
                check_in: req.body.check_in,
                check_out: req.body.check_out,
                status: req.body.status
            }
            options = {
                host: "127.0.0.1",
                port: "8000",
                path: "/reservas/",
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                    'Content-Length': Buffer.byteLength(JSON.stringify(post_data)) 
                }
            }
            options_get = {
                host: "127.0.0.1",
                port: "8000",
                path: "/reservas/",
                method: "GET",
            }
        } else {
            // Flight header options
        }
    })

    // send HTTP POST request to Database Server
    const post_req = http.request(options, (response) => {
        console.log(`Status code: ${res.statusCode}`)

        response.on('data', (data) => { // listen on data
            console.log(`Response from DataBase: ${data}`)
            res.status(200).send() // Successful Status Code to Client
        })
    })
    post_req.on('error', (error) => { // in case of an error
        console.log(`Error sending request: ${error.message}`)
    })
    post_req.write(post_data) // Send reservation data in the request body
    post_req.end()

    // get a HTTP GET request from Database Server 
    const get_req = http.request(options_get, (response) => {
        let responseData = ''
        response.on('data', (chunk) => { // collect the data from the response
            responseData += chunk
        })
        response.on('end', () => { // when the entire response has been received
            res.status(200).json(JSON.parse(responseData))
        })
    })
    get_req.on('error', (error) => {
        console.error(`Error making HTTP request to other server: ${error.message}`)
        res.status(500).json({error: 'Internal Server Error'})
    })
    get_req.end() // End the request to the other server
})

const server = http.createServer(app)
let port = 5843
const host = '0.0.0.0'

server.listen(port, host, () => {
    console.log(`Servidor a rodar em http://${host}:${port}/`)
})