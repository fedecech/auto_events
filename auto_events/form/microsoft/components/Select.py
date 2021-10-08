from typing import Any, List
from selenium.webdriver.remote.webelement import WebElement

from ...FormComponentType import FormComponentType
from ..MicrosoftFormComponent import MicrosoftFormComponent


class Select(MicrosoftFormComponent):
    """Create a Microsoft form Select (drop down select) component

    Paramaters
    ----------
    web_element: `'WebElement'`, default `None`
        web element associated with form component    
    """

    def __init__(self, web_element: 'WebElement' = None) -> None:
        super().__init__(web_element=web_element)

    def fill_in(self, response: str):
        """Select the right answer

        Paramaters
        ----------
        response: `str`
            the right answer
            (if options are: `["Option1", "Option 2"] you will` pass `"Option 1"` if it is the right one)
        """
        to_open_container = self.web_element.find_element_by_xpath(
            './/*[contains(@class, "select-placeholder")]')

        to_open_container.click()

        answers_container = self.web_element.find_element_by_xpath(
            './/*[contains(@class, "select-option-menu-container")]')

        answer_box = answers_container.find_element_by_xpath(
            ".//*[contains(text(), '{}')]".format(response))

        answer_box.click()
