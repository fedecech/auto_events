from typing import Any
from selenium.webdriver.remote.webelement import WebElement

from ..MicrosoftFormComponent import MicrosoftFormComponent


class Text(MicrosoftFormComponent):
    """Create a Microsoft form Text field component

    Paramaters
    ----------
    web_element: `'WebElement'`, default `None`
        web element associated with form component    
    """

    def __init__(self, web_element: 'WebElement' = None) -> None:
        super().__init__(web_element=web_element)

    def fill_in(self, response: str):
        """Fills in the text field

        Paramaters
        ----------
        response: `str`
            the text to fill in the text field with
        """
        text_field = self.web_element.find_element_by_class_name(
            'office-form-textfield')
        input = text_field.find_element_by_xpath('.//input')
        input.clear()
        input.send_keys(response)
