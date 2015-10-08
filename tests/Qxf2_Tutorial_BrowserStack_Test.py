"""
Selenium Test to login to Qxf2 Tutorial Page and assert the title
"""

import unittest, time, os
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class Qxf2_Tutorial_BrowserStack_Test(unittest.TestCase):
    "Example class written to run Selenium tests on BrowserStack"
    def setUp(self):
        desired_cap = {'os': 'Windows', 'os_version' : '7', 'browser': 'Firefox', 'browser_version':'36', 'browserstack.debug': 'true', 'browserstack.local':'true' }
        self.driver = webdriver.Remote(command_executor='http://avinashshetty:ppAo6mDXzyZ18M5e7hbi@hub.browserstack.com:80/wd/hub',desired_capabilities=desired_cap)
       
    def test_qxf2_selenium_tutorial(self):
        "An example test: Visit Qxf2 Tutorial Page and assert the title "
        # The driver.get method will navigate to a page given by the URL
        self.driver.get("http://localhost/selenium-tutorial-main.html")
        # Create a screenshots directory if not present
        if not (os.path.exists('./tests/screenshots')):
            os.makedirs('./tests/screenshots')
        # Save screenshot in the created directory
        self.driver.save_screenshot('./tests/screenshots/Qxf2_Tutorial_page.png')
        # Assert the Page Title
        self.assertIn ("Qxf2 Services: Selenium training main", self.driver.title)
        # Close the browser window
        self.driver.close()

    def tearDown(self):
        self.driver.quit()
 
if __name__ == '__main__':
    unittest.main()
