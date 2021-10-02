from abc import abstractmethod
from typing import Any, Callable, List, Optional
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement

from .FormComponentType import FormComponentType


class FormComponent:

    def __init__(self, web_element: 'WebElement' = None, type: 'FormComponentType' = FormComponentType.BASE) -> None:
        self.web_element = web_element
        self.type = type

    @abstractmethod
    def fill_in(self, response: Any):
        ...

    def get_type(c: 'WebElement') -> FormComponentType:

        if FormComponent.try_find_element(c.find_element_by_xpath, './/*[contains(@class, "select-placeholder")]') != None:
            return FormComponentType.SELECT
        elif FormComponent.try_find_element(c.find_element_by_xpath, './/*[contains(@class, "office-form-date-time-picker")]') != None:
            return FormComponentType.DATE_PICKER
        elif FormComponent.try_find_element(c.find_element_by_xpath, './/*[contains(@class, "office-form-question-choice")]') != None:
            return FormComponentType.RADIO
        elif FormComponent.try_find_element(c.find_element_by_xpath, './/*[contains(@class, "office-form-textfield")]') != None:
            return FormComponentType.TEXT

    def try_find_element(f: Callable[[str], Any], arg: str) -> Optional[Any]:
        elem = None
        try:
            elem = f(arg)
        except NoSuchElementException:
            pass
        return elem
