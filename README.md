# Auto Events

- [Reasons](#reasons)
- [Aims](#aims)
- [Installation and setup](#installation-and-setup)
  - [Clone from Git](#clone-from-git)
  - [Use pip](#use-pip)
  - [Azure configuration](#azure-configuration)
- [Basic usage](#basic-usage)
  - [Creating a task](#creating-a-task)
  - [Creating an event](#creating-an-event)
  - [Creating a calendar without source](#creating-a-calendar-without-source)
  - [Creating a Microsoft source](#creating-a-microsoft-source)
  - [Creating a calendar with source](#creating-a-calendar-with-source)
  - [Fetching for new events](#fetching-for-new-events)
  - [Creating your own source](#creating-your-own-source)
- [Forms](#forms)
  - [Create a Microsoft form](#create-a-microsoft-form)
  - [Filling the form](#filling-the-form)
  - [Creating your own form class](#creating-your-own-form-class)

## Reasons

Isn't annoying to complete repetitive tasks each day?
Well with a bit of programming knowledge this package could make your life just a bit easier and less repetitive.

## Aims

Automate annoying ad repetitive tasks such as submitting forms to attest attendance, keep track of work hours and more generically just automate tasks based on when they need to be performed.

## Features

- Fetch events from the calendar (supported: Outlook)
- Run custom tasks based on trigger dates
- Submit forms automatically based on events/or not

## Authentication

When using the Microsoft API or submitting forms where login is needed, you might be prompted to the console to enter the OTP for 2FA (if enabled). With the default driver the browser (chrome) data is stored (so it should happen rarely).

## Installation and setup

### Clone from Git

To clone the repo just run the following command in your working directory:

```command
git clone https://github.com/fedecech/auto_events.git
```

### Use pip

Run the following:

```command
pip install auto_events
```

### Azure configuration

If you intend to use the Microsoft Graph API to fetch the events from your cloud calendar, you should follow these steps:

1. log in to Azure ([here](https://portal.azure.com/)) or create an account if you do not have one.
2. Under **Azure Services** search for **App Registration**
3. Click on **New Registration**
   - Give your app a name
   - Select **Multi-Tenant** under Supported account types
   - As **Redirect URI** select web and use the following link: `https://login.microsoftonline.com/common/oauth2/nativeclient`
4. Once the app registration is completed, you should be redirected to the main dashboard. There are few things you need to do.
   - Copy the Application (client) ID value somewhere safe. You will need it later.
   - Under **Api Permissions**-> **Add a permission**. You should add the followings: `Calendars.Read`, `Calendars.Read.Shared`, `offline_access`, `User.Read` (if not already selected).
   - The last step is to create a secret token. Click on **Certificates & secrets** -> **New client secret** -> give it a name and copy it somewhere safe immediately (You will not be able to see it again).

## Basic Usage

If you are using the Microsoft API to fetch your events you should create a `.env` file following the template in `.env.example`. EMAIL and PASSWORD are your Microsoft account credentials and CLIENT_ID and SECRET are the values retrieved following the [Azure configuration process](#azure-configuration).

### Creating a task

A task is simply an object which stores a callback function to run (`to_run`), at what time(`datetime`) it should run and 2 other callback functions in case the task fails or succeeds (`on_success`and`on_failure`).

```python
from form_automator.Task import Task as AutoTask

def to_run():
  print("The task is running")

def on_success():
  print("The task runned with no errors")

def on_failure():
  print("An error occured while running the task")

date = datetime.now()
date = date + timedelta(seconds=10)

task = AutoTask(run_date=date, to_run=to_run, on_success=on_success, on_failure=on_failure)
```

In this example, the task run date is set to be 20 seconds after the task is created.

### Creating an event

An event is an object that stores its start and end date, the title of the event, and a list of tasks to be run.

```python
from form_automator.Event import Event as AutoEvent

date = datetime.now()
start_date = date + timedelta(minutes=5)
end_date = date + timedelta(minutes=10)
event = AutoEvent(start_date=start_date,
                       end_date=end_date, title="Event 1", tasks=[task])
```

### Creating a calendar without source

A calendar object is responsible for storing the events and running their tasks when appropriate (based on each `run_date` of each task). When using an API, in this case, the Microsoft API, Calendar needs a Source to fetch the events (But we'll see that later on [here]()).

```python
from form_automator.Calendar import Calendar as AutoCalendar

calendar = AutoCalendar(from_source=False, source=source, events=[event1])

calendar.listen()
```

The listen method, activates the scheduler to listen for events happening (tasks to be run).

### Creating a Microsoft source

To fetch events from our Microsoft API we need to create a `MicrosoftSource` object and pass that to our calendar.
The source uses Selenium so you should install the driver for your preferred browser (the default is Chrome).

```python
from form_automator.MicrosoftSource import MicrosoftSource
from dotenv.main import load_dotenv

load_dotenv('your/path/to/.env')

client_id = os.getenv('CLIENT_ID')
secret = os.getenv('API_SECRET')
email = os.getenv('EMAIL')
psw = os.getenv('PASSWORD')

credentials = (client_id, secret)

# You could also pass a custom driver instead of using the default one (driver=your_driver)... But it still needs to be a selenium webdriver
source = MicrosoftSource(path_to_driver='your/path/to/driver',
                          api_credentials=credentials, scopes=[
                              'Calendars.Read.Shared', 'Calendars.Read'],
                          account_cred={'email': email, 'password': psw})
```

### Creating a calendar with source

When creating a calendar with a source we can use 2 additional functions: `filter` and `map`. After the events are fetched from the API, the first one allows us to filter the event (for instance by date). The second one allows us to modify the events (add tasks to them)

```python
from form_automator.MicrosoftSource import MicrosoftSource

def filter(event: 'AutoEvent') -> bool:
    # return true when we want to keep the event
    return "Test Automation" in event.title

def map(source: 'Source', event: 'AutoEvent') -> 'AutoEvent':
    task = AutoTask(run_date=date, to_run=to_run, on_success=on_success, on_failure=on_failure)
    event.add_task(task)
    # returns the modified event
    return event

calendar = AutoCalendar(
        source=source, filter=filter, map=map)
```

### Fetching for new events

When we are fetching events from our API we want to keep everything up to date. To do that we need to implement an infinite loop.

```python
# calendar with source
calendar.listen()

while True:
    print('Fetching new data...')
    calendar.update()
    sleep(SLEEP_TIME)
```

### Creating your own source

To create a custom source, for instance, that fetches events from the Google Calendar API, you just need to create a subclass of `Source` and implement the abstract methods.
The `MicrosoftSource` is the perfect example of it.

## Forms

The package also offers an easy way to automate form submissions (using selenium).

### Create a Microsoft form

Currently, the only implementation available is for Microsoft forms.
When creating the object it will automatically find the from components (the questions: date pickers, text fields...). In case it does not work for your specific form you could do that manually using your implementation of selenium and pass a list of FormComponent to the form.

```python
from form_automator.form.microsoft.MicrosoftForm import MicrosoftForm

# the source is used to login into your microsoft account (find components automatically)
form = MicrosoftForm(url='https://your_form_url',
                         email_confirmation=True, source=source)

# retireving web element using selenium driver
date_picker_el = driver.find_element_by_id('date_picker')
# (passing components manually)
form = MicrosoftForm(url='https://your_form_url', source=source, components=[DatePicker(web_element=date_picker_el)])
```

### Filling the form

To fill in the form we need the answers to each question.
To do that we can call the `fill_in` function on the form, passing an array of answers.

```python
form.fill_in(['Answer1', '22/07/2022', 'Option1', 'Text field answer'])
```

### Creating your own form class

To create your custom form you just need to create a new subclass of `Form` and implement the abstract methods. `MicrosoftForm` is an example of it.
Other than that you also need to implement your own `FormComponent` class (by creating a subclass of `FormComponent`). For instance, `MicrosoftFromComponent` is an example of it.
If you also want to distinguish between each component you can create subclasses of your custom `FormComponent` class (for instance, `MyCustomDatePicker` which is a subclass of `MyCustomFormComponent`).
