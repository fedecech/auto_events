from typing import Any
from selenium.webdriver.remote.webelement import WebElement

from ..MicrosoftFormComponent import MicrosoftFormComponent


class Radio(MicrosoftFormComponent):
    """Create a Microsoft form Radio (select with no dropdown) component

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
        answers_container = self.web_element.find_element_by_class_name(
            'office-form-question-element')
        answer = answers_container.find_element_by_xpath(
            ".//*[contains(text(), '{}')]".format(response))
        answer.click()
