from typing import Any
from selenium.webdriver.remote.webelement import WebElement

from .FormComponent import FormComponent
from .FormComponentType import FormComponentType


class Text(FormComponent):
    def __init__(self, web_element: 'WebElement' = None) -> None:
        super().__init__(web_element=web_element, type=FormComponentType.TEXT)

    def fill_in(self, response: Any):
        text_field = self.web_element.find_element_by_class_name(
            'office-form-textfield')
        input = text_field.find_element_by_xpath('.//input')
        input.clear()
        input.send_keys(response)
