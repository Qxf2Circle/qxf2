import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class Selenium_Success_Test(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_selenium_trial_page(self):
        driver = self.driver
        driver.get("http://qxf2.com/selenium-trial-main")
        self.assertIn("Qxf2 Services: Selenium training main", driver.title)
        

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
