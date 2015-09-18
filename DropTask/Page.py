"""
Page class that all page models can inherit from
There are useful wrappers for common Selenium operations
"""

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import unittest,time,logging,os,inspect
from Base_Logging import Base_Logging
from inspect import getargspec

class Borg:
    #The borg design pattern is to share state
    #Src: http://code.activestate.com/recipes/66531/
    __shared_state = {}
    def __init__(self):
        self.__dict__ = self.__shared_state

    def is_first_time(self):
        "Has the child class been invoked before?"
        result_flag = False
        if len(self.__dict__)==0:
            result_flag = True

        return result_flag


class Page(Borg,unittest.TestCase):
    "Page class that all page models can inherit from"
    def __init__(self,selenium_driver,base_url='https://www-sandbox.socialtables.com/'):
        "Constructor"
        Borg.__init__(self)
        if self.is_first_time():
            #Do these actions if this the first time this class is initialized
            self.set_directory_structure() #Try and set the needed directory structure
            self.screenshot_counter = 1
            self.set_screenshot_dir()

        #We assume relative URLs start without a / in the beginning
        if base_url[-1] != '/': 
            base_url += '/' 
        self.base_url = base_url
        self.driver = selenium_driver
        self.log_obj = Base_Logging(level=logging.DEBUG)

        self.start() #Visit and initialize xpaths for the appropriate page


    def _screenshot(func):
        "Decorator for taking screenshot"
        def wrapper(*args,**kwargs):
            result = func(*args, **kwargs)
            screenshot_name = '%003d'%args[0].screenshot_counter + '_' + func.__name__
            args[0].screenshot_counter += 1
            args[0].save_screenshot(screenshot_name)
            return result
        return wrapper


    def _exceptionHandler(f):
        argspec = getargspec(f)
        def inner(*args,**kwargs):
            try:
                return f(*args,**kwargs)
            except Exception,e:
                args[0].write('You have this exception')
                args[0].write('Exception in method: %s'%str(f.__name__))
                args[0].write('PYTHON SAYS: %s'%str(e))
        return inner 
     

    def open(self,url):
        "Visit the page base_url + url"
        url = self.base_url + url
        if self.driver.current_url != url:
            self.driver.get(url)


    def get_calling_module(self):
        "Get the name of the calling module"
        calling_file = inspect.stack()[-1][1]
        calling_filename = calling_file.split(os.sep)

        #This logic bought to you by windows + cygwin + git bash 
        if len(calling_filename) == 1: #Needed for 
            calling_filename = calling_file.split('/')
        
        self.calling_module = calling_filename[-1].split('.')[0]

        return self.calling_module
    

    @_exceptionHandler
    def set_directory_structure(self):
        "Setup the required directory structure if it is not already present"
        screenshots_parent_dir = os.path.dirname(__file__) + os.sep + 'screenshots'
        if not os.path.exists(screenshots_parent_dir):
            os.makedirs(screenshots_parent_dir)


    @_exceptionHandler
    def set_screenshot_dir(self):
        "Set the screenshot directory"
        self.screenshot_dir = self.get_screenshot_dir()
        if not os.path.exists(self.screenshot_dir):
            os.makedirs(self.screenshot_dir)


    def get_screenshot_dir(self):
        "Get the name of the test"
        testname = self.get_calling_module()
        screenshot_dir = os.path.dirname(__file__) + os.sep + 'screenshots' + os.sep + testname
        if os.path.exists(screenshot_dir):
            for i in range(1,100):
                if os.path.exists(screenshot_dir + '_'+str(i)):
                    continue
                else:
                    os.rename(screenshot_dir,screenshot_dir +'_'+str(i))
                    break

        return screenshot_dir
            

    def get_page_xpaths(self,section):
        "open configurations file,go to right sections,return section obj"
        pass
        

    def get_xpath(self,xpath):
        "Return the DOM element of the xpath OR the 'None' object if the element is not found"
        dom_element = None
        try:
            dom_element = self.driver.find_element_by_xpath(xpath)
        except Exception,e:
            self.write(str(e),'debug')
        
        return dom_element

    
    def click_element(self,xpath,wait_seconds=0):
        "Click the button supplied"
        link = self.get_xpath(xpath)
        if link is not None:
            try:
                link.click()
                self.wait(wait_seconds)
            except Exception,e:
                self.write('Exception when clicking link with xpath: %s'%xpath,'debug')
                self.write(e)
            else:
                return True

        return False
    
               
    def set_text(self,xpath,value,clear_flag=True):
        "Set the value of the text field"
        text_field = self.get_xpath(xpath)
        try:
            if clear_flag is True:
                text_field.clear()
        except Exception, e:
            self.write('ERROR: Could not clear the text field: %s'%xpath,'debug')

        result_flag = False
        try:
            text_field.send_keys(value)
            result_flag = True
        except Exception,e:
            self.write('Unable to write to text field: %s'%xpath,debug)
            self.write(str(e),'debug')

        return result_flag

          
    def get_text(self,xpath):
        "Return the text for a given xpath or the 'None' object if the element is not found"
        text = ''
        try:
            text = self.get_xpath(xpath).text
        except Exception,e:
            self.write(e,'debug')
            return None
        else:
            return text.encode('utf-8')
        

    def get_dom_text(self,dom_element):
        "Return the text of a given DOM element or the 'None' object if the element has no attribute called text"
        text = ''
        try:
            text = dom_element.text
        except Exception, e:
            self.write(e,'debug')
            return None
        else:
            return text.encode('utf-8')
        

    def select_dropdown_option(self, select_locator, value=None):
        "Set the value of the dropdown (random pick if value=None)- return True"
        dropdown = self.driver.find_element_by_xpath(select_locator)
        option_found = False
        #If automation failed to locate the dropdown
        if dropdown is None:
            return
        elif value is None:
            choices = dropdown.find_elements_by_tag_name('option')
            random_index = int(random.uniform(1,len(choices))) 
            choices[random_index].click()
            self.wait(1)
            return True
        else:#You want to set the dropdown to a specific value
            for option in dropdown.find_elements_by_tag_name('option'):
                if option.text == value:
                    option_found = True
                    option.click()
                    break
            self.wait(1)
            return option_found


    def check_element_present(self,xpath):
        "This method checks if the web element is present in page or not and returns True or False accordingly"
        result_flag = False
        if self.get_xpath(xpath) is not None:
            result_flag = True

        return result_flag
    

    def save_screenshot(self,screenshot_name,extension='.png'):
        "Take a screenshot" 
        if os.path.exists(self.screenshot_dir + os.sep + screenshot_name + extension):
            for i in range(1,1000):
                if os.path.exists(self.screenshot_dir + os.sep + screenshot_name+'_' + str(i) + extension):
                    continue
                else:
                    os.rename(self.screenshot_dir + os.sep +screenshot_name + extension, self.screenshot_dir + os.sep + screenshot_name + '_' + str(i) + extension)
                    break
        self.driver.get_screenshot_as_file(self.screenshot_dir + os.sep+ screenshot_name + extension)


    def switch_to_iframe(self,frame_name):
        "Switch to iframe"
        result_flag = False
        try:
            self.driver.switch_to_frame(frame_name)
            result_flag = True
        except Exception:
            self.write(e,'debug')

        return result_flag


    def right_click(self,xpath):
        "Right click on xpath provided"
        result_flag = False
        self.actionChains = ActionChains(self.driver)
        elm = self.get_xpath(xpath)
        if elm is not None:
            self.actionChains.context_click(elm).perform()
            result_flag = True

        return result_flag


    def explicit_wait(self,xpath,wait_time=5):
        "Explicitly waits for the element for the specified time"
        result_flag = False
        try:
            element = WebDriverWait(self.driver, wait_time).until(EC.presence_of_element_located((By.XPATH,(xpath))))
            result_flag = True
        except Exception,e:
            self.write(str(e),'debug')

        return result_flag

    
    def switch_to_default(self):
        "Switch to default content"
        self.driver.switch_to_default_content()


    def teardown(self):
        "Tears down the driver"
        self.driver.quit()


    def write(self,msg,level='info'):
        "This method use the logging method"
        self.log_obj.write(msg,level)
        

    def conditional_write(self,flag,positive,negative,level='info',pre_format="  - "):
        "Write out either the positive or the negative message based on flag"
        if flag is True:
            self.write(pre_format + positive,level)
        if flag is False:
            self.write(pre_format + negative,level)


    def wait(self,wait_seconds=5):
        "Performs wait for time provided"
        time.sleep(wait_seconds)


    _screenshot = staticmethod(_screenshot)
    _exceptionHandler = staticmethod(_exceptionHandler)

