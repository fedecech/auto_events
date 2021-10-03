from typing import Any
from selenium.webdriver.remote.webelement import WebElement

from ..MicrosoftFormComponent import MicrosoftFormComponent


class Radio(MicrosoftFormComponent):
    def __init__(self, web_element: 'WebElement' = None) -> None:
        super().__init__(web_element=web_element)

    def fill_in(self, response: Any):
        answers_container = self.web_element.find_element_by_class_name(
            'office-form-question-element')
        answer = answers_container.find_element_by_xpath(
            ".//*[contains(text(), '{}')]".format(response))
        answer.click()
