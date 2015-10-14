"""
Selenium Test to login to Qxf2 Tutorial Page and assert the title
"""

import os
from selenium import webdriver

# Create an instance of Firefox WebDriver
driver = webdriver.Firefox()
# The driver.get method will navigate to a page given by the URL
driver.get("http://localhost/selenium-tutorial-main.html")
# Assert the Page Title
assert "Qxf2 Services: Selenium training main" in driver.title
# Close the browser window
driver.close()
