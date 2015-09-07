---------
1. SETUP
---------
a. Install Python 2.x
b. Install Selenium
c. Add both to your PATH environment variable
d. If you do not have it already, get pip 
e. 'pip install python-dotenv'
f. Update 'login.credentials' with your credentials
g. Update 'saucelabs.credentials' is you want to run on Sauce Labs
h. In case you have TestRail Integration update the testrail.conf with proper case ids. Also update the testrail.env with url,user,password.
i. To run mechanize scripts install mechanize (pip install mechanize)

-------
2.1 RUN SELENIUM
-------
a. python Demo_Test.py -b ff
b. For more options: python Demo_Test.py -h  

--------
2.2 RUN MECHANIZE
--------
a. eg: python Droptask_CreateGroup_Mechanize.py
b. Make sure you have appropriate Project, Groups and tasks created when you run these tests

-----------
3. ISSUES?
-----------
a. If Python complains about an Import exception, please 'pip install $module_name'
b. If you are not setup with the drivers for the web browsers, you will see a helpful error from Selenium telling you where to go and get them
c. If login fails, its likely that you forgot to update the login.credentials file
d. Exception? 'module object has no attribute load_dotenv'? You have the wrong dotenv module. So first 'pip uninstall dotenv' and then 'pip install python-dotenv'
e. Others: Contact mak@qxf2.com

