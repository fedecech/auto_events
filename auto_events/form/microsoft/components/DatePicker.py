from selenium.webdriver.remote.webelement import WebElement

from ..MicrosoftFormComponent import MicrosoftFormComponent


class DatePicker(MicrosoftFormComponent):
    """Create a Microsoft form date picker component

    Paramaters
    ----------
    web_element: `'WebElement'`, default `None`
        web element associated with form component    
    """

    def __init__(self, web_element: 'WebElement' = None) -> None:
        super().__init__(web_element=web_element)

    def fill_in(self, response: str):
        """Select the date passed

        Paramaters
        ----------
        response: `str`
            the date to select in string format
        """
        input = self.web_element.find_element_by_xpath('.//input')
        input.click()
        input.click()
        input.clear()
        input.send_keys(response)

        body = self.web_element.find_element_by_xpath('//body')
        body.click()
