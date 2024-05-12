#!/usr/bin/env node

import inquirer from 'inquirer'
import chalkAnimation from 'chalk-animation'
import http from 'http'

const clientData = {card: {}}

const sleep = (ms = 2000) => new Promise((r) => setTimeout(r, ms)) // timer 2s

async function welcome() {
    const pulseTitle = chalkAnimation.pulse(
        'Transaction Processing System' 
    )

    await sleep() // wait for 2 sec
    pulseTitle.stop() // kill animation
}

async function chooseReservation() {
    const choice = await inquirer.prompt({
        name: 'reservation',
        type: 'list',
        message: 'Choose the wanted reservation:',
        choices: [
            'Hotel', 
            'Flight Company'
        ],
    })

    clientData.reservationChoice = choice.reservation
}
await chooseReservation()

if (clientData.reservationChoice === "Hotel") {

    async function hotelGet() {
        const options = {
            host: "127.0.0.1",
            port: "3001",
            path: "/reservateHotel",
            method: "GET",
            headers: {
                'Content-Type': 'application/json'
            }
        }
        const get_req = http.request(options, (res)=> {
            console.log(`\nStatus code: ${res.statusCode}`)
        
            const data = ''
            res.on('data', chunk => {
                data += chunk
            })
            res.on('end', () => {
                console.log(`Available Reservations: ${data}`)
            })
        })
        get_req.on('error', (error) => {
            console.error(`\nError making HTTP request to the server: ${error.message}`)
        })
        get_req.end()
    }

    async function clientName() {
        const answers = await inquirer.prompt({
            name: 'client_name',
            type: 'input',
            message: 'Enter your Name:',
            default() {
                return 'Name'
            }
        })
    
        clientData.name = answers.client_name
    }

    async function clientEmail() {
        const answers = await inquirer.prompt({
            name: 'client_email',
            type: 'input',
            message: 'Enter your Email:',
            default() {
                return 'Email'
            }
        })
    
        clientData.email = answers.client_email
    }

    async function clientPhone() {
        const answers = await inquirer.prompt({
            name: 'client_phone',
            type: 'input',
            message: 'Enter your Phone Number:',
            default() {
                return 'Number'
            }
        })
    
        clientData.phone_number = answers.client_phone
    }

    async function roomType() {
        const answers = await inquirer.prompt({
            name: 'room_type',
            type: 'list',
            message: 'Choose a Room type:',
            choices: [
                "Standard Duplo",
                "Suíte Presidencial"
            ]
        })
    
        clientData.room_type = answers.room_type
    }

    // Room Number implementation
    // Check_in implementation
    // Check_out implementation
    // Status implementation

    await hotelGet()
    await clientName()
    await clientEmail()
    await clientPhone()
    await roomType()
}

async function typeCard() {
    const answers = await inquirer.prompt({
        name: 'card_type',
        type: 'list',
        message: 'Enter your credit card type:',
        choices: [
            'Visa',
            'Mastercard'
        ]
    })

    clientData.card.type = answers.card_type
}

async function cardName() {
    const answers = await inquirer.prompt({
        name: 'card_name',
        type: 'input',
        message: 'Enter your credit card holder name:',
        default() {
            return 'Card Name'
        }
    })

    clientData.card.name = answers.card_name
}

async function cardNumber() {
    const answers = await inquirer.prompt({
        name: 'card_number',
        type: 'input',
        message: 'Enter your credit card number:',
        default() {
            return 'Card Number'
        }
    })

    clientData.card.number = answers.card_number
}

async function cardDate() {
    const answers = await inquirer.prompt({
        name: 'card_date',
        type: 'input',
        message: 'Enter your credit card expire date (MM/AA):',
        default() {
            return 'Expire Date'
        }
    })

    clientData.card.date = answers.card_date
}

async function securityCode() {
    const answers = await inquirer.prompt({
        name: 'card_security_code',
        type: 'input',
        message: 'Enter your credit card security code:',
        default() {
            return 'Security Code'
        }
    })

    clientData.card.security = answers.card_security_code
}

await welcome()
await typeCard()
await cardName()
await cardNumber()
await cardDate()
await securityCode()

const postData = `${JSON.stringify(clientData)}`

const options = {
    host: "127.0.0.1",
    port: "3001",
    path: "/transaction",
    method: "POST",
    headers: {
        'Content-Type': 'application/json'
    }
}

const post_req = http.request(options, (res) => {
    console.log(`Status code: ${res.statusCode}`)

    var responseData = ""
    res.on('data', (chunk) => {
        responseData += chunk
    })
    res.on('end', () => {
        console.log(responseData)
    })
})
post_req.on('error', (error) => {
    console.log(`Error making request: ${error.message}`);
})
post_req.write(postData)
post_req.end()