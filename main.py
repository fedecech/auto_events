from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from dotenv import load_dotenv
import os
load_dotenv()

email = os.getenv('EMAIL')
psw = os.getenv('PASSWORD')
driver = webdriver.Chrome('/Users/fedecech/Selenium Drivers/chromedriver')

driver.get('https://forms.office.com/r/mVZKDrD0Rg')

# Wait page is loaded
time.sleep(5)

current_url: str = driver.current_url

print(current_url)
# user is not logged in
if ("login" in current_url):
    print("Logging in using credentials")
    email_input = driver.find_element_by_id("i0116")

    email_input.clear()
    email_input.send_keys(email)
    email_input.send_keys(Keys.RETURN)

    time.sleep(2)

    password_input = driver.find_element_by_id("i0118")

    password_input.clear()
    password_input.send_keys(psw)
    password_input.send_keys(Keys.RETURN)
time.sleep(10)

driver.close()
