#!/usr/bin/env node

import inquirer from 'inquirer'
import chalkAnimation from 'chalk-animation'
import { createSpinner } from 'nanospinner'

let client 

const sleep = (ms = 2000) => new Promise((r) => setTimeout(r, ms)) // timer 2s

async function welcome() {
    const pulseTitle = chalkAnimation.pulse(
        'Transaction Processing System' 
    )

    await sleep() // wait for 2 sec
    pulseTitle.stop() // kill animation
}

await welcome()

async function askName() {
    const answers = await inquirer.prompt({
        name: 'client_name',
        type: 'input',
        message: 'What is your name?',
        default() {
            return 'Client'
        }
    })

    client = answers.client_name
}

await askName()

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
    } else {
        spinner.error({text: `The following age is not acceptable, retry again!`})
    }
}

await askAge()

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
}

await chooseTransaction()