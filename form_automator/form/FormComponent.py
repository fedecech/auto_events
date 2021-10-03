from abc import abstractmethod
from typing import Any
from selenium.webdriver.remote.webelement import WebElement

from .FormComponentType import FormComponentType


class FormComponent:

    def __init__(self, web_element: 'WebElement' = None) -> None:
        self.web_element = web_element

    @abstractmethod
    def fill_in(self, response: Any):
        ...

    @abstractmethod
    def get_type(c: 'WebElement') -> FormComponentType:
        ...
