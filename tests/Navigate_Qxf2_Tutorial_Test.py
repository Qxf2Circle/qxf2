"""
Selenium Test to login to Qxf2 Tutorial Page and assert the title
"""

import os
from selenium import webdriver

# Create an instance of Firefox WebDriver
driver = webdriver.Firefox()
# The driver.get method will navigate to a page given by the URL
driver.get("http://qxf2.com/selenium-tutorial-main")
# Create a screenshots directory if not present
if (os.path.exists('./screenshots')):
    pass
else:
    os.makedirs('./screenshots')
# Save screenshot in the created directory
driver.save_screenshot('./screenshots/Qxf2_Tutorial_success.png')
# Assert the Page Title
assert "Qxf2 Services: Selenium training main" in driver.title
# Close the browser window
driver.close()
