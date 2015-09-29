import unittest, os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class Selenium_Failure_Test(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_selenium_trial_page(self):
        driver = self.driver
        driver.get("http://qxf2.com/selenium-trial-main")
        os.makedirs('./screenshots')
        driver.save_screenshot('./screenshots/Qxf2_Tutorial_Failure.png')
        self.assertIn("Qxf2", driver.title)
        

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
