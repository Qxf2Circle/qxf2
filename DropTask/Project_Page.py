"""
Page object model for the project page
"""
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from Page import Page


class Project_Page(Page):
    "Page object for the Project page"
    
    def start(self):
        self.url = "projects"
        self.open(self.url) 
        # Assert Title of the Project Page
        self.assertIn("DropTask", self.driver.title)      

        "Xpath of all the field"
        #Create project
        self.project_link = "//a[@class='projects']"
        self.new_project_button = "//button[@id='walkthrough-highlight-create-project']"
        self.project_name_text = "//input[@placeholder='Project name']"
        self.create_project_button = "//button[text()='Create Project']"
        self.project_title = "//div[@class='name' and text()='%s']"

    def create_project(self,project_name):
        " Click on Projects Link to create new Project"
        self.click_element(self.project_link)
        " Click on New Project button"
        self.click_element(self.new_project_button)
        " Set the project_name as the text in the project name field"
        self.set_text(self.project_name_text, project_name)
        self.click_element(self.create_project_button)
        " Get the name of the created Project to assert Project created or failure"
        project_title = self.get_text(self.project_title%project_name)
        " Assert that the title of the project created is as specified."
        if project_title == project_name:
            self.write("Added Project successfully")
            return True
        else:
            self.write("There was some Issue while adding Project")
            return False
        

