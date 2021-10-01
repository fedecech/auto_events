from time import sleep
from O365.account import Account
from selenium.webdriver.chrome import options
from selenium.webdriver.remote.webelement import WebElement
from Provider import Provider
from Event import Event
from typing import Any, Callable, Dict, List, Optional, Tuple, TypedDict, overload
from Source import Source
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import ast


class AccountCred(TypedDict):
    email: str
    password: str


class MicrosoftSource(Source):

    def __init__(self, api_credentials: Tuple[str, str], account_cred: 'AccountCred') -> None:
        super(MicrosoftSource, self).__init__(provider=Provider.MICROCALENDAR)
        self.scopes = ['Calendars.Read.Shared', 'Calendars.Read']
        options = Options()
        options.add_argument(
            "user-data-dir=/Users/fedecech/form_automator/chrome_data")
        self.driver = webdriver.Chrome(
            '/Users/fedecech/Selenium Drivers/chromedriver', options=options)

        self.api_credentials = api_credentials
        self.account_cred = account_cred

    def load_events(self, should_login: bool = True, filter: Optional[Callable[['Event'], bool]] = None, map: Optional[Callable[['Event'], 'Event']] = None) -> List['Event']:
        account = Account(credentials=self.api_credentials)

        if should_login:
            if not self.authenticate(account=account):
                return

        if should_login:
            print('****** Authenticated ******')

        schedule = account.schedule()
        calendar = schedule.get_default_calendar()
        events = calendar.get_events(include_recurring=False)

        parsed_events: List['Event'] = []
        for mic_event in events:
            event = Event.from_microsoft_event(mic_event)
            changed_event = event
            to_add = True
            if filter != None:
                if not filter(event):
                    to_add = False

            if map != None and to_add:
                changed_event = map(event)

            if to_add:
                parsed_events.append(changed_event)

        return parsed_events

    # Authenticate with API
    # __handle_consent is called by authenitcate passing current_url
    def authenticate(self, account: 'Account'):
        return account.authenticate(scopes=self.scopes, handle_consent=self.__handle_consent)

    # Opens url to verifiy account(login if not)
    # If data is stored from previous logins it will not login
    # Else it will login
    def __handle_consent(self, consent_url: str) -> str:
        self.driver.get(consent_url)
        # self.__add_cookies_from_store('cookies.txt')
        sleep(2)
        if self.__needs_login(self.driver.current_url):
            return self.__login()
        else:
            return self.driver.current_url

    # Input email and password in form
    # If 2FA is required it will ask to input the OTP
    def __login(self) -> str:
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
        return "/common/login" in current_url

    def __handle_app_permission(self) -> None:
        print('Here')
        confirm_btn = self.driver.find_element_by_id('idSIButton9')
        confirm_btn.click()

    def __complete_input_field(self, input: 'WebElement', input_text: str) -> None:
        input.clear()
        input.send_keys(input_text)
        input.send_keys(Keys.RETURN)

    def __select_account(self, account_selector: 'WebElement'):
        account_selector.find_elements_by_xpath(
            ".//*[contains(text(), '{}')]".format(self.account_cred['email']))
        account_selector.click()

    def __is2FA(self) -> bool:
        return "DeviceAuthTls" in self.driver.current_url

    def __handle_2FA(self) -> None:
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

    def __needs_login(self, current_url: str) -> bool:
        return "login" in current_url

    def __add_cookies_from_store(self, path):
        with open(path, "r") as f:
            txt_cookies = f.read()
            if txt_cookies != "":
                cookies = ast.literal_eval(txt_cookies)
                for c in cookies:
                    self.driver.add_cookie(c)
            f.close()
