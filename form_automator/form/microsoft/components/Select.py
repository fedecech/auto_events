from typing import Any, List
from selenium.webdriver.remote.webelement import WebElement

from ...FormComponentType import FormComponentType
from ..MicrosoftFormComponent import MicrosoftFormComponent


class Select(MicrosoftFormComponent):
    def __init__(self, web_element: 'WebElement' = None) -> None:
        super().__init__(web_element=web_element)

    def fill_in(self, response: Any):
        to_open_container = self.web_element.find_element_by_xpath(
            './/*[contains(@class, "select-placeholder")]')

        to_open_container.click()

        answers_container = self.web_element.find_element_by_xpath(
            './/*[contains(@class, "select-option-menu-container")]')

        answer_box = answers_container.find_element_by_xpath(
            ".//*[contains(text(), '{}')]".format(response))

        answer_box.click()
