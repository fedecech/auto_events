from abc import abstractmethod
from typing import Any, Callable, Optional
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement

from ..FormComponentType import FormComponentType
from .MicrosoftFormComponentType import MicrosoftFormComponentType
from ..FormComponent import FormComponent


class MicrosoftFormComponent(FormComponent):
    """Used as a super class to create more specific class components

    Paramaters
    ----------
    web_element: `'WebElement'`, default `None`
        web element associated with the form component
    """

    def __init__(self, web_element: 'WebElement' = None) -> None:
        super(MicrosoftFormComponent, self).__init__(web_element=web_element)

    @abstractmethod
    def fill_in(self, response: Any):
        """Abstract method, used to be ovveride by more specific components"""
        ...

    def get_type(c: 'WebElement') -> FormComponentType:
        """Get the element type

        Paramaters
        ----------
        c: `'WebElement'`
            web element to find the type of

        Returns
        -------
        `FormComponent`
            component type for `FormComponent`
        """
        if MicrosoftFormComponent.try_find_element(c.find_element_by_xpath, './/*[contains(@class, "select-placeholder")]') != None:
            return MicrosoftFormComponentType.SELECT
        elif MicrosoftFormComponent.try_find_element(c.find_element_by_xpath, './/*[contains(@class, "office-form-date-time-picker")]') != None:
            return MicrosoftFormComponentType.DATE_PICKER
        elif MicrosoftFormComponent.try_find_element(c.find_element_by_xpath, './/*[contains(@class, "office-form-question-choice")]') != None:
            return MicrosoftFormComponentType.RADIO
        elif MicrosoftFormComponent.try_find_element(c.find_element_by_xpath, './/*[contains(@class, "office-form-textfield")]') != None:
            return MicrosoftFormComponentType.TEXT

    def try_find_element(f: Callable[[str], Any], arg: str) -> Optional[Any]:
        """Try to find an element

        Paramaters
        ----------
        f: `Callable[[str], Any]`
            function called to find element
        arg: `str`
            argument passed to f

        Returns
        -------
        `Optional[Any]`
            the element if found
        """
        elem = None
        try:
            elem = f(arg)
        except NoSuchElementException:
            pass
        return elem
