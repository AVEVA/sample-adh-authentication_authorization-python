"""This script uses Selenium to perform a test of the program.py script"""

import json
import time
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from .program import main, get_appsettings


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

    # Use Personal Account (Must be enabled on Tenant)
    print()
    print('Selenium 2: Choose Personal Account')
    browser.find_element(by=By.Xpath, value='descendant::a[@title="Personal Account"]').click()
    time.sleep(2)

    # Enter Username and submit
    print()
    print('Selenium 3: Enter Username')
    browser.find_element(by=By.Xpath, value='//*[@id="i0116"]').send_keys(username)
    browser.find_element(by=By.Xpath, value='//*[@id="idSIButton9"]').click()
    time.sleep(2)

    # Enter Password and submit
    print()
    print('Selenium 4: Enter Password')
    browser.find_element(by=By.Xpath, value='//*[@id="i0118"]').send_keys(password)
    elem = browser.find_element(by=By.Xpath, value='//*[@id="idSIButton9"]')
    try:
        browser.set_page_load_timeout(5)
        elem.click()

        # Login may or may not prompt to save credentials, try this inside try/catch
        time.sleep(2)
        browser.find_element(by=By.Xpath, value='//*[@id="idSIButton9"]').click()
    except Exception:
        print('Ignore time out, start the server...')


if __name__ == '__main__':
    unittest.main()
