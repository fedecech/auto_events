from abc import abstractmethod
from typing import List
from selenium.webdriver.chrome.webdriver import WebDriver
from .deafults import default_driver, default_store_path

from .Event import Event


class Source:
    """Abstract class used as super class and to create custom sources classes

    Paramaters
    ----------
    path_to_driver: `str`
        required path to chrome driver (default)
    driver: `'WebDriver'`, default `None`
        optional driver used instead of the deafult one
    path_to_store: `str`, default `""`
        path to file storage (folder storing tokens, driver data...)        
    """

    def __init__(self, path_to_driver: str, driver: 'WebDriver' = None, path_to_store: str = "") -> None:
        if path_to_store == "":
            self.path_to_store = default_store_path
        else:
            self.path_to_store = path_to_store

        self.path_to_driver = path_to_driver
        if driver == None:
            self.driver = default_driver(
                path_to_store=self.path_to_store, path_to_driver=self.path_to_driver)
        else:
            self.driver = driver

    @abstractmethod
    def load_events(self, *args, **kwargs) -> List['Event']:
        """Load events from external source (an API for instance)

        Returns
        `List['Event']`
            list of parsed events
        """
        ...

    @abstractmethod
    def login(self, *args, **kwargs) -> str:
        """Handle authentication to API/External Source.

        Returns
        -------
        str
            new url when authenticated
        """
        ...
