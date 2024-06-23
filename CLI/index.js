#!/usr/bin/env node

import inquirer from 'inquirer'
import chalkAnimation from 'chalk-animation'
import { createSpinner } from 'nanospinner'
import http from 'http'

const clientData = {card: {}}
const loginData = {}
const registerData = {}
let loginState;
let statusCode


const sleep = (ms = 2000) => new Promise((r) => setTimeout(r, ms)) // timer 2s

async function welcome() {
    const pulseTitle = chalkAnimation.pulse(
        'Transaction Processing System' 
    )

    await sleep() // wait for 2 sec
    pulseTitle.stop() // kill animation
}

async function login() {
    const username = await inquirer.prompt({
        name: 'username',
        type: 'input',
        message: 'username:'
    })
    const password = await inquirer.prompt({
        name: 'password',
        type: 'input',
        message: 'password:'
    })

    loginData.username = username.username
    loginData.password = password.password
    loginData.reservationChoice = clientData.reservationChoice
}

async function register() {
    const username = await inquirer.prompt({
        name: 'username',
        type: 'input',
        message: 'username:'
    })
    const email = await inquirer.prompt({
        name: 'email',
        type: 'input',
        message: 'email:'
    })
    const password = await inquirer.prompt({
        name: 'password',
        type: 'input',
        message: 'password:'
    })

    registerData.username = username.username
    registerData.email = email.email
    registerData.password = password.password
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

async function Operation() {

    const choice = await inquirer.prompt({
        name: 'operation',
        type: 'list',
        message: 'Choose the following Operation:',
        choices: [
            "Cancel Reservation",
            "Make Reservation"
        ]
    })

    clientData.operation = choice.operation
}

await chooseReservation()

async function loginOperation() {

    const choice = await inquirer.prompt({
        name: 'operation',
        type: 'list',
        message: 'Login or Register:',
        choices: [
            "Login",
            "Register"
        ]
    })

    loginState = choice.operation
}

await loginOperation()

async function validateOperation() {
    if (loginState === "Login") {
        await login()
        const postData = `${JSON.stringify(loginData)}`

        const options = {
            host: "127.0.0.1",
            port: "3001",
            path: "/login",
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            }
        }

        let responseData = ""
        const post_req = http.request(options, (res) => {
            
            res.on('data', (chunk) => {
                responseData += chunk
            })
            res.on('end', () => {
                const data = JSON.parse(responseData) // receive JSON file and convert it to an object
                mensagemLogin = data.message
                statusCode = data.statusCode
            })
        })
        post_req.on('error', (error) => {
            console.log(`Error making request: ${error.message}`);
        })
        post_req.write(postData)
        post_req.end()
        
    } else {
        await register()
        const postData = `${JSON.stringify(registerData)}`

        const options = {
            host: "127.0.0.1",
            port: "3001",
            path: "/register",
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            }
        }

        let responseData = ""
        const post_req = http.request(options, (res) => {
            
            res.on('data', (chunk) => {
                responseData += chunk
            })
            res.on('end', () => {
                const data = JSON.parse(responseData) // receive JSON file and convert it to an object
                mensagemLogin = data.message
                statusCode = data.statusCode
            })
        })
        post_req.on('error', (error) => {
            console.log(`Error making request: ${error.message}`);
        })
        post_req.write(postData)
        post_req.end()
    }
}

await validateOperation()

if (statusCode === 200) {

    if (clientData.reservationChoice === "Hotel") {

        await Operation()

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

        if (clientData.operation === "Cancel Reservation") {
            await clientName()
            await clientEmail()
            await clientPhone()

            async function cancelReservation() {
                //
            }
            await cancelReservation()

        } else {
            await getRoom()
            await chooseRoom()
            await getCheck_in()
            await getCheck_out()
            await clientName()
            await clientEmail()
            await clientPhone()
            await roomType()
        }

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

    if (clientData.operation != "Cancel Reservation") {
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
        let mensagem, status
        const post_req = http.request(options, (res) => {
            status = res.statusCode
            
            res.on('data', (chunk) => {
                responseData += chunk
            })
            res.on('end', () => {
                const data = JSON.parse(responseData) // receive JSON file and convert it to an object
                mensagem = data.message
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
            if (clientData.reservationChoice === "Hotel" && mensagem === "Reserva feita com sucesso!" && status === 200) {
                spinner.success({text: mensagem})
            } else if (clientData.reservationChoice === "Hotel" && mensagem === "Reserva feita com sucesso!" && status != 200){
                spinner.error({text: "Não há quartos disponíveis desta classe."})
            } else if(clientData.reservationChoice === "Hotel" && status != 200) {
                spinner.error({text: "Reserva não pode ser concluida"})
            }else if (clientData.reservationChoice === "Flight Company" && status === 200){
                spinner.success({text: "Reserva feita com sucesso!"})
            } else {
                spinner.error({text: "Reserva não pode ser concluida"})
            }
        }
        await final()

        if (clientData.reservationChoice === "Hotel" && status === 200) {
            let reservations = ''

            async function showDescription() {
                return new Promise((resolve, reject) => {
                    const options = {
                        host: "127.0.0.1",
                        port: "3001",
                        path: "/showReservation",
                        method: "GET",
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    }
                    const get_req = http.request(options, (res)=> {
                        //console.log(`\nStatus code: ${res.statusCode}`)
                        
                        res.on('data', chunk => {
                            reservations += chunk
                        })
                        res.on('end', () => {
                            const jsonData = JSON.parse(reservations)
                            Object.values(jsonData['reservas']).forEach(value => {
                                if (clientData.email === value[2]) {
                                    console.log(`Reservation Description: ${value}`)
                                }
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
            await showDescription()
        } else if (clientData.reservationChoice === "Flight Company" && status === 200){
            let reservations = ''

            async function showDescription() {
                return new Promise((resolve, reject) => {
                    const options = {
                        host: "127.0.0.1",
                        port: "3001",
                        path: "/showReservationtravel",
                        method: "GET",
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    }
                    const get_req = http.request(options, (res)=> {
                        //console.log(`\nStatus code: ${res.statusCode}`)
                        
                        res.on('data', chunk => {
                            reservations += chunk
                        })
                        res.on('end', () => {
                            const jsonData = JSON.parse(reservations)
                            jsonData.forEach(element => {
                                if (clientData.email === element.email) {
                                    console.log(`Booking: Reservation sented to ${element.email}`)
                                }
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
            await showDescription()
        }
    }
}