# Form Automator

## Aim

Automate form submission providing an API to create custom tasks

## Features

- Take events from calander (supported: Apple Calandar, Outlook, Google)
- Run custom tasks when event is finished/started/during the event
- More specific tasks:
  - Submit forms automatically based on event (attandance forms/HR forms to claim hours)
  - Keep a record of actions runned and if they were succesful or not
  - Store data submitted in a excel/csv file to check

## Example 1

A module requires to signin/out on every working our:

- When event happens triggers a task to submit the form:
- Sends email confirmation that the task was succesful
- Updates the presence excel

## Example 2

Every time hours of work are done need to claim hours:

- When event happens triggers a task to submit the form:
- Sends email confirmation that the task was succesful
- Updates the calimed hours excel
