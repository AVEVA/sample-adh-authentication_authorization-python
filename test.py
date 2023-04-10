"""This script uses Selenium to perform a test of the program.py script"""

import json
import time
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from program import main, get_appsettings


class AuthPKCEPythonSampleTests(unittest.TestCase):
    """Tests for the Authorization Code + PKCE Python script"""

    @classmethod
    def test_main(cls):
        """Tests the program.py script using a Selenium script for browser actions"""

        main(selenium_script)


def selenium_script(auth_url):
    """Automatically performs browser actions for login"""

    appsettings = get_appsettings()

    username = appsettings.get('Username')
    password = appsettings.get('Password')

    # Open Chrome Webdriver, go to Auth page
    print()
    print('Selenium 1: Open Chrome WebDriver')
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    browser = webdriver.Chrome(options=chrome_options)
    browser.get(auth_url)
    time.sleep(2)

    # Enter Username and Password then submit
    print()
    print('Selenium 2: Enter Username and Password then submit')
    browser.find_element(by=By.XPATH, value='//*[@id="email"]').send_keys(username)
    browser.find_element(by=By.XPATH, value='//*[@id="password"]').send_keys(password)
    browser.find_element(by=By.XPATH, value='//*[@id="submit"]').click()
    time.sleep(10)


if __name__ == '__main__':
    unittest.main()
