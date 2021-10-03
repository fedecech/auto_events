from abc import abstractmethod
from typing import Any, Callable, Optional
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement

from .MicrosoftFormComponentType import MicrosoftFormComponentType
from ..FormComponentType import FormComponentType
from ..FormComponent import FormComponent


class MicrosoftFormComponent(FormComponent):
    def __init__(self, web_element: 'WebElement' = None) -> None:
        super(MicrosoftFormComponent, self).__init__(web_element=web_element)

    @abstractmethod
    def fill_in(self, response: Any):
        ...

    def get_type(c: 'WebElement') -> FormComponentType:

        if MicrosoftFormComponent.try_find_element(c.find_element_by_xpath, './/*[contains(@class, "select-placeholder")]') != None:
            return MicrosoftFormComponentType.SELECT
        elif MicrosoftFormComponent.try_find_element(c.find_element_by_xpath, './/*[contains(@class, "office-form-date-time-picker")]') != None:
            return MicrosoftFormComponentType.DATE_PICKER
        elif MicrosoftFormComponent.try_find_element(c.find_element_by_xpath, './/*[contains(@class, "office-form-question-choice")]') != None:
            return MicrosoftFormComponentType.RADIO
        elif MicrosoftFormComponent.try_find_element(c.find_element_by_xpath, './/*[contains(@class, "office-form-textfield")]') != None:
            return MicrosoftFormComponentType.TEXT

    def try_find_element(f: Callable[[str], Any], arg: str) -> Optional[Any]:
        elem = None
        try:
            elem = f(arg)
        except NoSuchElementException:
            pass
        return elem
