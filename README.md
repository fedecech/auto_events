# Form Automator

# TODO

- Create Query constructor form fetching API
- Add more docs on how to customise
- Add more customasiblity to package
- on update instead of setting the new fetached value to the events in Calendar, try to see if tehy already exists ore if they where modified and update the events array accordigly
- Some tasks do not get triggered beacuse of frequent updates (while updating trigger_time becomes bigger then date.now)
- on update login based on expiration of O356_token.txt:
  if expired login else do not (instead of passing always False). In initialisation always loggin

## Aim

Automate form submission providing an API to create custom tasks

## Warning

Ensure that 2FA is disabled or that you have an active session (logged in) in your browser.
Currently if you are not logged in you can create an `.env` file following `.env.example`

## API Usage

- Create Source
- Create Calendar
- listen to events

### Source

Class to retrieve events (`List[Event]`).

Supported cloud calendars: Microsoft Calendar.

You can create your own Source by inerithing from `Source` superclass.

## Task

A task is simply an object that runs a callback function (`to_run()`) you pass (which must return true/false on success/faliure).
It has a field id (16 char string) to process easily each task in the queue (genarted automatically but it can be passed in the object constructor).
A Task can have 2 other callbacks:

- on_success: Called if the `to_run` returns true
- on_failure: Called if the `to_run` returns false

```python
def to_run:()
  print("Task runned")

task = Task(to_run=to_run)
```

## Event

The main way to create an Event is by calling an API in this case the one powered by Microsoft.

```python
date = datetime.now()
date = date + timedelta(seconds=10)

event1 = Event(trigger_date=datestart_date=date,end_date=date,title="Event 1", tasks=[task])
```

## Calendar

A Calendar is just a container for events. A Calendar object can be initalised passing a source or a list of Events. If none of them is passed events will be initialised as an empty array.

The only interasting aspect of Calendar is the `def listen_for_events_triggering(self):` method, which waits for the first `event.trigger_date` to happen and runs `event.trigger_tasks()`.
The last one takes two arguments to customise its behaviour:

- `run_all: bool = True` if true will run all the tasks owned by that event, if false it will use the id parameter (shown below) to find the task to run.
- `id: Optional[str] = None` used to find the task to run

## Authentication

There are three possible instances and cases:

- 2FA not enabled -> No issue you just need to create the `.env` file with email and password variables
- 2FA enabled:
  - The first time you run the program you'll need to provide the OTP in the terminal
  - Every time you change how you interact whith the api you'll need to login again

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
