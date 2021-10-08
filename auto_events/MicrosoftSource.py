import os
from time import sleep
from O365.account import Account
from O365.utils.token import FileSystemTokenBackend
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from typing import Callable, List, Optional, Tuple, TypedDict
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import json
from datetime import datetime


from .Event import Event
from .Source import Source
from .deafults import default_token_file, default_store_path


class AccountCred(TypedDict):
    email: str
    password: str


class MicrosoftSource(Source):
    """Create a source subclass that uses Microsoft graph API to fetch events

    Paramaters
    ----------
    path_to_driver: `str`
        required path to chrome driver (default one)
    api_credentials: `Tuple[str, str]`
        (client_id, api_secret) Microsoft API credentials
    account_cred: `'AccountCred'`
        (email, password) your Microsoft account credentials
    driver: `'WebDriver'`, default `None`
        optional driver used instead of the deafult one
    path_to_store: `str`, default: `""`
        path to file storage (folder storing tokens, driver data...).
        If not provided the store path will be `../` from this directory
    scopes: `List[str]`, default `[]`
        scopes used to call Microsoft API    
    """

    def __init__(self, path_to_driver: str, api_credentials: Tuple[str, str], account_cred: 'AccountCred', driver: 'WebDriver' = None, path_to_store: str = "", scopes: List[str] = []) -> None:
        super(MicrosoftSource, self).__init__(driver=driver,
                                              path_to_store=path_to_store, path_to_driver=path_to_driver)

        self.scopes = scopes
        self.api_credentials = api_credentials
        self.account_cred = account_cred

    def load_events(self, filter: Optional[Callable[['Event'], bool]] = None, map: Optional[Callable[['MicrosoftSource', 'Event'], 'Event']] = None) -> List['Event']:
        """Load events from API

        Paramaters
        ----------
        filter: `Optional[Callable[['Event'], bool]]`, default `None`
            callback function to filter not wanted events
        map: `Optional[Callable[['MicrosoftSource', 'Event'], 'Event']]`, default `None`
            callback function to modify previously filtered events (for instance to add a task based on the event)

        Returns
        -------
        `List['Event']`
            events fetched, filtered and mapped
        """
        token_backend = FileSystemTokenBackend(
            token_path=self.path_to_store, token_filename=default_token_file)
        account = Account(credentials=self.api_credentials,
                          token_backend=token_backend)
        should_login = not self.__is_in_session()

        if should_login:
            if not self.__api_authenticate(account=account):
                return

        if should_login:
            print('****** Authenticated ******')

        schedule = account.schedule()
        calendar = schedule.get_default_calendar()
        events = calendar.get_events(include_recurring=False)

        parsed_events: List['Event'] = []
        for i, mic_event in enumerate(events):
            event = Event.from_microsoft_event(mic_event)
            changed_event = event
            to_add = True
            if filter != None:
                if not filter(event):
                    to_add = False

            if map != None and to_add:
                changed_event = map(source=self, event=event)

            if to_add:
                parsed_events.insert(i + 1, changed_event)

        return parsed_events

    def __is_in_session(self) -> bool:
        """Find out if the current session is expired

        Returns
        -------
        `bool`
            `True` if valid session (logged in) 
        """

        in_session = False
        token_path = os.path.join(self.path_to_store, default_token_file)
        if os.path.exists(token_path):
            with open(token_path, "r") as f:
                token = json.load(f)
                token_expiration = token['expires_at']
                now = datetime.now().timestamp()
                in_session = token_expiration > now
                f.close()

        return in_session

    def __api_authenticate(self, account: 'Account') -> bool:
        """Uses O365 library to authenticate using scopes and handle_consent

        Returns
        -------

        `bool`
            `True` if authentication is successful
        """

        return account.authenticate(scopes=self.scopes, handle_consent=self.login)

    # change name to login (also in Source superclass)
    def login(self, consent_url: Optional[str] = None) -> str:
        """Logins to Microsoft account. 
        Called by `account.authenticate(scopes=scopes, handle_consent=self.handle_consent)` (O365 package) to login with command line.
        If consent_url is not passed it will login normally (calls `__selenium_login`)


        Paramaters
        ----------
        consent_url: `Optional[str]`, default `None`
            url used to command line login

        Returns
        -------
        `str`
            url after login
        """

        if consent_url != None:
            self.driver.get(consent_url)
        sleep(2)
        # find out if if stat is needed should't be cause if method runs should need authentication
        if self.needs_login(self.driver.current_url):
            return self.__selenium_login()
        else:
            return self.driver.current_url

    def __selenium_login(self) -> str:
        """Logins to Microsoft account using selenium automation

        Returns
        -------
        `str`
            url after login
        """

        print("Logging in using credentials")
        account_selector = None
        try:
            account_selector = self.driver.find_element_by_id('tilesHolder')
        except NoSuchElementException:
            pass

        if account_selector != None:
            self.__select_account(account_selector=account_selector)
        else:

            sleep(2)
            email_input = self.driver.find_element_by_id("i0116")
            self.__complete_input_field(
                input=email_input, input_text=self.account_cred['email'])

        sleep(2)

        password_input = self.driver.find_element_by_id("i0118")
        self.__complete_input_field(
            input=password_input, input_text=self.account_cred['password'])

        sleep(2)

        if self.__is2FA():
            self.__handle_2FA()

        sleep(2)

        if(self.__is_asking_app_permission(current_url=self.driver.current_url)):
            self.__handle_app_permission()

        sleep(2)

        return self.driver.current_url

    def __is_asking_app_permission(self, current_url: str) -> bool:
        """Returns boolean based on if microsoft is asking to give app (Azure app) permission to access profile.
        Usually asks only if is first time running the client (on specific account)

        Returns
        -------
        `bool`
            `True` if is asking to give permission to app
        """

        return "/common/login" in current_url

    def __handle_app_permission(self) -> None:
        """Gives permission to app

        Returns
        -------
        `None`
        """

        confirm_btn = self.driver.find_element_by_id('idSIButton9')
        confirm_btn.click()

    def __complete_input_field(self, input: 'WebElement', input_text: str) -> None:
        """Complete text field using selenium

        Paramaters
        ----------
        input: `'WebElement'`
            selenium element
        input_text: `str`
            string to be inputted in text field

        Returns
        -------
        `None`
        """

        input.clear()
        input.send_keys(input_text)
        input.send_keys(Keys.RETURN)

    def __select_account(self, account_selector: 'WebElement') -> None:
        """Selects account in account selector page (using selenium)

        Paramaters
        ----------
        account_selector: `'WebElement'`

        Returns
        -------
        `None`
        """

        account_selector.find_elements_by_xpath(
            ".//*[contains(text(), '{}')]".format(self.account_cred['email']))
        account_selector.click()

    def __is2FA(self) -> bool:
        """Retuned boolean based on if 2FA confirmation is required (after email and password inputted)

        Returns
        -------
        `bool`
            `True` if 2FA confirmation is required
        """

        return "DeviceAuthTls" in self.driver.current_url

    def __handle_2FA(self) -> None:
        """Handles 2FA using selenium. Asks to input the OTP in the terminal

        Returns 
        -------
        `None`
        """

        msg_box = self.driver.find_element_by_id(
            'idDiv_SAOTCC_Description')

        msg = msg_box.text
        code = input(msg + "\n")
        code_input = self.driver.find_element_by_id('idTxtBx_SAOTCC_OTC')

        code_input.clear()
        code_input.send_keys(code)

        disable_2fa_check_box = self.driver.find_element_by_id(
            'idChkBx_SAOTCC_TD')
        disable_2fa_check_box.click()

        code_input.send_keys(Keys.RETURN)

    # try using it in Form
    def needs_login(self, current_url: Optional[str] = None) -> bool:
        """Retuns boolen based on if login is required

        Paramaters
        ----------
        current_url: `Optional[str]`, default `None`
            driver url (if not passed uses self.driver.current_url)
        Returns
        -------
        `bool`
            `True` if login is required
        """

        return "login" in current_url if current_url != None else self.driver.current_url
