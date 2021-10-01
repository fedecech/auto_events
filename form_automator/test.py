from datetime import datetime, timedelta, timezone
from time import sleep
from Task import Task
from Event import Event
from MicrosoftSource import MicrosoftSource
import os
from dotenv.main import load_dotenv
from Calendar import Calendar

load_dotenv('/Users/fedecech/form_automator/.env')

client_id = os.getenv('CLIENT_ID')
secret = os.getenv('API_SECRET')
email = os.getenv('EMAIL')
psw = os.getenv('PASSWORD')
SLEEP_TIME = 10

credentials = (client_id, secret)


def to_run():
    print("[MicrosoftSource] 1 . Task runned from inside map func")
    return True


def add_task_to_test_events(event: 'Event') -> 'Event':
    task = Task(to_run=to_run, on_success=lambda: print(
        "[MicrosoftSource] 2 . success callback"))
    event.add_task(task)
    return event


def filter(e: 'Event'):
    LOCAL_TIMEZONE = datetime.now(timezone.utc).astimezone().tzinfo
    localised_date = datetime.now().replace(tzinfo=LOCAL_TIMEZONE)
    return "Test Automation" in e.title and e.trigger_date + timedelta(seconds=SLEEP_TIME/2) > localised_date


def main():
    source = MicrosoftSource(credentials, account_cred={
                             'email': email, 'password': psw})

    calendar = Calendar(
        source=source, filter=filter, map=add_task_to_test_events)

    while True:
        print('Fetching new data...')
        sleep(SLEEP_TIME)  # update very 10 secs
        calendar.update()

    source.driver.close()


if __name__ == "__main__":
    main()
