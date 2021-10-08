import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

default_store_path = os.path.join(os.getcwd(), 'store')
default_token_file = 'o365_token.txt'


def default_driver(path_to_store: str, path_to_driver: str):
    options = Options()
    options.add_argument(
        "user-data-dir={}/chrome_data".format(path_to_store))
    return webdriver.Chrome(
        path_to_driver, options=options)


def default_callback():
    return True
