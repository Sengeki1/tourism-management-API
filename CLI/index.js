#!/usr/bin/env node

import inquirer from 'inquirer'
import chalkAnimation from 'chalk-animation'
import { createSpinner } from 'nanospinner'
import http from 'http'

const clientData = {}

const sleep = (ms = 2000) => new Promise((r) => setTimeout(r, ms)) // timer 2s

async function welcome() {
    const pulseTitle = chalkAnimation.pulse(
        'Transaction Processing System' 
    )

    await sleep() // wait for 2 sec
    pulseTitle.stop() // kill animation
}

async function chooseTransaction() {
    const choice = await inquirer.prompt({
        name: 'transaction',
        type: 'list',
        message: 'Choose the wanted transaction',
        choices: [
            'Hotel', 
            'Flight Company'
        ],
    })

    clientData.transaction = choice.transaction
}

async function askName() {
    const answers = await inquirer.prompt({
        name: 'client_name',
        type: 'input',
        message: 'What is your name?',
        default() {
            return 'Client'
        }
    })

    clientData.name = answers.client_name
}

async function askAge() {
    const answers = await inquirer.prompt({
        name: 'client_age',
        type: 'input',
        message: 'How old are you?',
        default() {
            return 'Client'
        }
    })

    return handleAge(answers.client_age)
}

async function handleAge(age) {
    const int = parseInt(age)
    const spinner = createSpinner('Validating input...').start()
    await sleep()

    if (!(Number.isNaN(int))) {
        spinner.success({text: `...`})
        clientData.age = int
    } else {
        spinner.error({text: `The following age is not acceptable, retry again!`})
        askAge()
    }
}

//  TO-DO (Ask for transaction questions then save the answers in obj)
/*

    * What type of transaction are you initiating? (e.g., purchase, withdrawal, transfer)
    * What is the monetary amount or quantity associated with this transaction?
    * Who is the recipient or beneficiary of this transaction? (e.g., account number, recipient's name)
    * Can you provide a brief description or reason for this transaction? (optional)
    * In which currency should this transaction be processed? (if applicable)
    * When should this transaction be processed? (current date/time, future date/time, etc.)
    * Do you confirm your request to proceed with this transaction?

*/

await welcome()
await chooseTransaction()
await askName()
await askAge()

console.log(clientData)

// TO-DO (send a http POST request to the Monitor TP server containing the obj)

// TO-DO (get http STATUS CODE from the Monitor TP server)