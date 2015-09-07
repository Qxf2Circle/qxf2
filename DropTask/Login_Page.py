"""
Page object model for the login page
"""
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from Page import Page


class Login_Page(Page):
    "Page object for the Login page"

    
    def start(self):
        self.url = "login"
        self.open(self.url) 
        # Assert Title of the Login Page and Login
        self.assertIn("DropTask - Login", self.driver.title)      

        "Xpath of all the field"
        #Login 
        self.login_username = "//input[@type='email']"
        self.login_password = "//input[@type='password']"
        self.login_submit = "//button[text()='Login']"


    def login(self, username, password):
        "Login using credentials provided"  
        self.set_text(self.login_username,username)
        self.set_text(self.login_password,password)
        self.click_element(self.login_submit)
        
        if (self.driver.current_url != "https://www.droptask.com/login"):
            self.write("Login Success")
            return True
        else:
            self.write("Login error")
            return False
        
