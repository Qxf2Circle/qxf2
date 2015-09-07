"""
PageFactory uses the factory design pattern. 
get_page_object() returns the appropriate page object.
Add elif clauses as and when you implement new pages.
Pages implemented so far:
1. Login
2. Project
3. Preferences 

"""
from selenium import webdriver
from Login_Page import Login_Page
from Project_Page import Project_Page
from Preferences_Page import Preferences_Page

def get_page_object(page_name,driver,base_url='https://www.droptask.com/'):
    "Return the appropriate page object based on page_name"
    test_obj = None
    page_name = page_name.lower()
    if page_name == "login":
        test_obj = Login_Page(driver,base_url=base_url)
    elif page_name == "project":
        test_obj = Project_Page(driver,base_url=base_url)
    elif page_name == "preferences":
        test_obj = Preferences_Page(driver,base_url=base_url)
        
    
    
    return test_obj
