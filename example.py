from datetime import datetime, timedelta, timezone
from time import sleep
import os
from dotenv.main import load_dotenv

from auto_events.Calendar import Calendar as AutoCalendar
from auto_events.Event import Event as AutoEvent
from auto_events.MicrosoftSource import MicrosoftSource
from auto_events.Source import Source
from auto_events.Task import Task as AutoTask
from auto_events.form.microsoft.MicrosoftForm import MicrosoftForm


load_dotenv('path/to/.env')

client_id = os.getenv('CLIENT_ID')
secret = os.getenv('API_SECRET')
email = os.getenv('EMAIL')
psw = os.getenv('PASSWORD')
SLEEP_TIME = 10

credentials = (client_id, secret)


def to_run(source: 'Source'):
    form = MicrosoftForm(url='form_url',
                         email_confirmation=True, source=source)
    form.fill_in(responses=["Option 1", "Option 2", "22/02/2021",
                            "Option 4", "Hey there, it's working"])
    print("[MicrosoftSource] 1 . Task runned from inside map func")
    return True


def add_task_to_test_events(source: 'Source', event: 'AutoEvent') -> 'AutoEvent':
    # task = AutoTask(run_date=event.start_date, to_run=lambda: to_run(source=source), on_success=lambda: print(
    #     "[MicrosoftSource] 2 . success callback"))
    task1 = AutoTask(run_date=event.end_date, to_run=lambda: to_run(source=source), on_success=lambda: print(
        "[MicrosoftSource] 2 . success callback"))
    # event.add_task(task)
    event.add_task(task1)
    return event


def filter(e: 'AutoEvent'):
    LOCAL_TIMEZONE = datetime.now(timezone.utc).astimezone().tzinfo
    localised_date = datetime.now().replace(tzinfo=LOCAL_TIMEZONE)
    return "Test Automation" in e.title and e.end_date + timedelta(seconds=SLEEP_TIME/2) > localised_date


def main():
    source = MicrosoftSource(path_to_driver='path/to/chrome/driver',
                             api_credentials=credentials, scopes=[
                                 'Calendars.Read.Shared', 'Calendars.Read'],
                             account_cred={'email': email, 'password': psw})

    calendar = AutoCalendar(
        source=source, filter=filter, map=add_task_to_test_events)

    # date = datetime.now()
    # date = date + timedelta(seconds=10)

    # task = AutoTask(to_run=lambda: to_run(source), run_date=date)
    # event1 = AutoEvent(start_date=date,
    #                    end_date=date, title="Event 1", tasks=[task])

    # calendar = AutoCalendar(from_source=False, source=source, events=[event1])
    calendar.listen()

    while True:
        print('Fetching new data...')
        calendar.update()
        sleep(SLEEP_TIME)  # update very 10 secs

    source.driver.close()


if __name__ == "__main__":
    main()
