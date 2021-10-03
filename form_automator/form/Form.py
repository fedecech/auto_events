from abc import abstractmethod
from typing import List

from .FormComponent import FormComponent
from ..Source import Source


class Form:
    """Abstract class to create subclass and inherit needed methods and instance variables

    Paramaters
    ----------
    url: `str`, default `""`
        url of form
    source: `'Source'`
        source to login and have other functionality (if needed)
    components: `List['FormComponent']`
        components composing form
    """

    def __init__(self, url: str = "", source: 'Source' = None, components: List['FormComponent'] = []) -> None:
        self.url = url
        self.source = source
        self.components = components

    @abstractmethod
    def find_components(self, *args, **kwargs) -> List['FormComponent']:
        """Find and parse automatically form components

        Returns
        -------
        `List['FormComponent']`
            list of parsed components
        """
        ...

    @abstractmethod
    def fill_in(self, *args, **kwargs) -> None:
        """Fill in form

        Returns
        -------
        `None`
        """
        ...

    @abstractmethod
    def send(self, *args, **kwargs) -> None:
        """Sends form

        Returns
        -------
        `None`
        """
        ...
