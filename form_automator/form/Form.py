from time import sleep
from typing import Any, List
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys

from ..MicrosoftSource import MicrosoftSource
from .FormComponent import FormComponent
from .Text import Text
from .Radio import Radio
from ..Source import Source
from .DatePicker import DatePicker
from .FormComponentType import FormComponentType
from .Select import Select


class Form:
    def __init__(self, url: str = "", components: List['FormComponent'] = None, source: 'Source' = None, email_confirmation: bool = True) -> None:

        self.url = url
        self.email_confirmation = email_confirmation

        if source != None:
            self.source = source

        if components != None:
            self.components = components
        else:
            self.login_if_needed()
            self.components = self.__find_components()

        # 2 approaches:
        #   - get passed the source and call source.handle_consent(url) with url = form_url
        #   - create driver for form class with same storage as Source (chrome_data)

    # class office-form-question-body (outer body)
        # childs class __question__ office-form-question

    def __find_components(self) -> List['FormComponent']:
        if isinstance(self.source, MicrosoftSource):

            form_container = self.source.driver.find_element_by_class_name(
                'office-form-question-body')
            childs = form_container.find_elements_by_xpath(
                './/*[contains(@class, "__question__")]')
            components = []
            for c in childs:
                type = FormComponent.get_type(c)

                if type == FormComponentType.SELECT:
                    components.append(Select(web_element=c))
                elif type == FormComponentType.DATE_PICKER:
                    components.append(DatePicker(web_element=c))
                elif type == FormComponentType.TEXT:
                    components.append(Text(web_element=c))
                elif type == FormComponentType.RADIO:
                    components.append(Radio(web_element=c))
            return components

    def login_if_needed(self):
        # check automatically if needs login instead of with var
        if isinstance(self.source, MicrosoftSource):
            self.source.driver.get(self.url)

            sleep(8)

            if "login" in self.source.driver.current_url:
                print('here')
                self.source.handle_consent()

            sleep(8)

    def fill_in(self, responses: List[Any]):
        for i, c in enumerate(self.components):
            c.fill_in(response=responses[i])
        if self.email_confirmation:
            self.__select_email_check_box()

        sleep(2)

        self.send()

    def send(self):
        # Select last component and send return key
        if isinstance(self.source, MicrosoftSource) and len(self.components) >= 1:
            submit_btn = self.source.driver.find_element_by_xpath(
                './/*[contains(@class, "__submit-button__")]')
            submit_btn.click()

    def __select_email_check_box(self):
        if isinstance(self.source, MicrosoftSource):
            try:
                container = self.source.driver.find_element_by_class_name(
                    'office-form-email-receipt-checkbox')
                check_box = container.find_element_by_css_selector(
                    'input[type=checkbox]')
                check_box.click()
            except:
                pass
