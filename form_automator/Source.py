import os
from time import sleep
from dotenv.main import load_dotenv
from Event import Event
from typing import List, Optional
from Provider import Provider
from O365 import Account, MSGraphProtocol
import readline
from selenium import webdriver
from Util import Util
from selenium.webdriver.chrome.options import Options
import ast


class Source:
    def __init__(self, provider: Optional['Provider'] = None) -> None:
        self.provider = provider

    def load_events(self) -> List['Event']:
        return []
        # if self.provider == Provider.ICALENDAR:
        #     return self.__load_from_icalendar()
        # elif self.provider == Provider.MICROCALENDAR:
        #     return self.__load_from_microcalendar()
        # elif self.provider == Provider.MICROCALENDAR:
        #     return self.__load_from_googlecalendar()

    # def __load_from_icalendar(self):
    #     pass

    # def __load_from_microcalendar(self):
    #     protocol = MSGraphProtocol()
    #     scopes = ['Calendars.Read.Shared', 'Calendars.Read']

    #     # previous = open('scopes.txt', "r").read()
    #     authorise_app = False

    #     # if str(scopes) != previous:
    #     #     authorise_app = True
    #     #     open('scopes.txt', "w").write(scopes)

    #     account = Account(credentials)

    #     if account.authenticate(scopes=scopes, handle_consent=self.handle_consent):
    #         print("autheniticated")

    #     schedule = account.schedule()
    #     calendar = schedule.get_default_calendar()
    #     events = calendar.get_events(include_recurring=False)

    #     for event in events:
    #         print(event)
    #     return []

    # def handle_consent(self, consent_url: str) -> str:
    #     # chrome_options = Options()
    #     # chrome_options.add_experimental_option("detach", True)
    #     driver = webdriver.Chrome(
    #         '/Users/fedecech/Selenium Drivers/chromedriver')

    #     # if (len(driver.window_handles) >= 1 and driver.window_handles[0]):
    #     # driver.switch_to_window(driver.window_handles[0])

    #     driver.get(consent_url)

    #     with open('cookies.txt', "r") as f:
    #         txt_cookies = f.read()
    #         if txt_cookies != "":
    #             cookies = ast.literal_eval(txt_cookies)
    #             for c in cookies:
    #                 driver.add_cookie(c)
    #         f.close()

    #     sleep(2)

    #     current_url: str = driver.current_url

    #     if ("login" in current_url):
    #         Util.login_to_microsoft(email=email, password=psw, driver=driver)

    #     sleep(5)

    #     with open("cookies.txt", "w") as f:
    #         f.write(str(driver.get_cookies()))

    #     return driver.current_url

    # def __load_from_googlecalendar(self):
    #     pass
