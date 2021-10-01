from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.safari.webdriver import WebDriver


class Util:
    # chrom edriver type
    def login_to_microsoft(email: str, password: str, driver: 'WebDriver') -> None:
        print("Logging in using credentials")
        email_input = driver.find_element_by_id("i0116")

        email_input.clear()
        email_input.send_keys(email)
        email_input.send_keys(Keys.RETURN)

        sleep(2)

        password_input = driver.find_element_by_id("i0118")

        password_input.clear()
        password_input.send_keys(password)
        password_input.send_keys(Keys.RETURN)

        sleep(5)

        if(("login" in driver.current_url) and not (("code" in driver.current_url))):
            msg_box = driver.find_element_by_id(
                'idDiv_SAOTCC_Description')

            msg = msg_box.text
            code = input(msg + "\n")
            code_input = driver.find_element_by_id('idTxtBx_SAOTCC_OTC')

            code_input.clear()
            code_input.send_keys(code)

            disable_2fa_check_box = driver.find_element_by_id(
                'idChkBx_SAOTCC_TD')
            disable_2fa_check_box.click()

            code_input.send_keys(Keys.RETURN)
