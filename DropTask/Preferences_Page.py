"""
Page object model for the preferences page
"""
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from Page import Page


class Preferences_Page(Page):
    "Page object for the Preferences page"
    
    def start(self):
        self.url = "preferences"
        self.open(self.url) 
        # Assert Title of the Project Page
        self.assertIn("DropTask", self.driver.title)      

        #Xpath of all the fields in preferences page
        self.email_link = "//a[text()='Emails']"
        self.notification_button = "//section[@id='user-preferences-notifications']/descendant::button[text()='%s']"
        self.notification_frequency_radio = "//input[@id='notification-emails-%s']"

    def set_notification(self,email_notification):
        "Set Notification to On"
        self.click_element(self.notification_button%email_notification)
        

    def set_notification_frequency(self,email_notification_frequency):
        "Set Notification frequency to daily or immediately"
        notification_frequency_radio_elem = self.get_xpath(self.notification_frequency_radio%email_notification_frequency.lower())
        if notification_frequency_radio_elem is None:
            return False
        else:
            if notification_frequency_radio_elem.is_selected():
                self.write("%s  is already Clicked"%email_notification_frequency)
                return True
            else:
                return (self.click_element(self.notification_frequency_radio%email_notification_frequency.lower()))
        
            
    def change_email_preference(self,email_notification,email_notification_frequency):
        "Method to update email preferences"
        #Click on Emails Link to change email preference
        self.click_element(self.email_link)
        #Set Notification to On or Off 
        self.set_notification(email_notification)
        self.wait(2)
        #Set Notification Frequency 
        return self.set_notification_frequency(email_notification_frequency)


