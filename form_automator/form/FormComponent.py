from abc import abstractmethod
from typing import Any
from selenium.webdriver.remote.webelement import WebElement

from .FormComponentType import FormComponentType


class FormComponent:
    """Abstract class to create specific form components classes.

    Paramaters
    ----------
    web_element: `'WebElement'`
        selenium web element of the form field
    """

    def __init__(self, web_element: 'WebElement' = None) -> None:
        self.web_element = web_element

    @abstractmethod
    def fill_in(self, response: Any):
        """Complete the form component (for instance, fill in a text field)

        Paramaters
        ----------
        response: `Any`
            the response used to fill in the form component
        """
        ...

    @abstractmethod
    def get_type(c: 'WebElement') -> FormComponentType:
        """Gets the type of the web element (the types should be subclasses of `FormComponent`)

        Paramaters
        ----------
        c: `'WebElement'`
            web element to find the type of

        Returns
        -------
        `FormComponentType`
            the type of the form component
        """
        ...
