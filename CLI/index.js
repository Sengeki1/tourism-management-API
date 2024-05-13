#!/usr/bin/env node

import inquirer from 'inquirer'
import chalkAnimation from 'chalk-animation'
import { createSpinner } from 'nanospinner'
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

    async function chooseRoom() {
        const answers = await inquirer.prompt({
            name: 'room',
            type: 'list',
            message: 'Choose Room Type:',
            choices: [
                "A",
                "B",
                "C"
            ]
        })

        clientData.room = answers.room
    }

    async function getRoom() {
        let available_rooms = '';

        return new Promise((resolve, reject) => {
            const options = {
                host: "127.0.0.1",
                port: "3001",
                path: "/reservateroom",
                method: "GET",
                headers: {
                    'Content-Type': 'application/json'
                }
            }
            const get_req = http.request(options, (res)=> {
                //console.log(`\nStatus code: ${res.statusCode}`)
                
                res.on('data', chunk => {
                    available_rooms += chunk
                })
                res.on('end', () => {
                    const jsonData = JSON.parse(available_rooms)
                    Object.keys(jsonData["Quartos disponíveis"]).forEach(key => {
                        const value = jsonData["Quartos disponíveis"][key]
                        console.log(`Available  Rooms: ${key}: ${value}`)
                    })
                    resolve()
                })
            })
            get_req.on('error', (error) => {
                console.log(`\nError making HTTP request to the server: ${error.message}`)
                reject(error)
            })
            get_req.end()
        })
    }

    async function getCheck_in() {
        let today = new Date()

        let dd = today.getDate()
        let mm = today.getMonth() + 1
        let yyyy = today.getFullYear()

        let day = `${dd}${mm}${yyyy}`

        clientData.check_in = parseInt(day)
    }

    async function getCheck_out() {
        let today = new Date()

        let dd = today.getDate() + 5
        let mm = today.getMonth() + 6
        let yyyy = today.getFullYear()

        let day = `${dd}${mm}${yyyy}`

        clientData.check_out = parseInt(day)
    }

    async function clientName() {
        const answers = await inquirer.prompt({
            name: 'client_name',
            type: 'input',
            message: 'Enter your Name:'
        })
    
        clientData.name = answers.client_name
    }

    async function clientEmail() {
        const answers = await inquirer.prompt({
            name: 'client_email',
            type: 'input',
            message: 'Enter your Email:'
        })
    
        clientData.email = answers.client_email
    }

    async function clientPhone() {
        const answers = await inquirer.prompt({
            name: 'client_phone',
            type: 'input',
            message: 'Enter your Phone Number:'
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

    // TO-DO 
    /*
        * Operation Choose Delete Reservation
        * Make Reservation
    */

    await getRoom()
    await chooseRoom()
    await getCheck_in()
    await getCheck_out()
    await clientName()
    await clientEmail()
    await clientPhone()
    await roomType()

} else { // Flight
    async function clientName() {
        const answers = await inquirer.prompt({
            name: 'client_name',
            type: 'input',
            message: 'Enter your Name:'
        })
    
        clientData.name = answers.client_name
    }

    async function clientEmail() {
        const answers = await inquirer.prompt({
            name: 'client_email',
            type: 'input',
            message: 'Enter your Email:'
        })
    
        clientData.email = answers.client_email
    }

    async function clientPhone() {
        const answers = await inquirer.prompt({
            name: 'client_phone',
            type: 'input',
            message: 'Enter your Phone Number:'
        })
    
        clientData.phone_number = answers.client_phone
    }

    await clientName()
    await clientEmail()
    await clientPhone()
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
        message: 'Enter your credit card holder name:'
    })

    clientData.card.name = answers.card_name
}

async function cardNumber() {
    const answers = await inquirer.prompt({
        name: 'card_number',
        type: 'input',
        message: 'Enter your credit card number:'
    })

    clientData.card.number = answers.card_number
}

async function cardDate() {
    const answers = await inquirer.prompt({
        name: 'card_date',
        type: 'input',
        message: 'Enter your credit card expire date (MM/AA):'
    })

    clientData.card.date = answers.card_date
}

async function securityCode() {
    const answers = await inquirer.prompt({
        name: 'card_security_code',
        type: 'input',
        message: 'Enter your credit card security code:'
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

let responseData = ""
let mensagem;
const post_req = http.request(options, (res) => {
    //console.log(`Status code: ${res.statusCode}`)
    
    res.on('data', (chunk) => {
        responseData += chunk
    })
    res.on('end', () => {
        const data = JSON.parse(responseData) // receive JSON file and convert it to an object
        mensagem = data.mensagem
    })
})
post_req.on('error', (error) => {
    console.log(`Error making request: ${error.message}`);
})
post_req.write(postData)
post_req.end()

async function final() {
    const spinner = createSpinner("...").start()
    await sleep()
    if (mensagem === "Reserva feita com sucesso!") {
        spinner.success({text: mensagem})
    } else {
        spinner.error({text: mensagem})
    }
}
await final()