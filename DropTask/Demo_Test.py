"""
Test case for DropTask functionality.

Our automated test will do the following:
    #1. Login
    #2. Create Project
    #3. Update email preferences
"""
import os,PageFactory,Test_Rail,Conf_Reader
from optparse import OptionParser
from DriverFactory import DriverFactory


def check_file_exists(file_path):
    #Check if the config file exists and is a file
    conf_flag = True
    if os.path.exists(file_path):
        if not os.path.isfile(file_path):
            print '\n****'
            print 'Config file provided is not a file: '
            print file_path
            print '****'
            conf_flag = False
    else:
        print '\n****'
        print 'Unable to locate the provided config file: '
        print file_path
        print '****'
        conf_flag = False

    return conf_flag


def check_options(options):
    "Check if the command line options are valid"
    options.config_file = os.path.abspath(options.config_file)
    return check_file_exists(options.config_file)


def run_demo_test(browser,conf,tconf,base_url,test_run_id=None,sauce_flag=None,browser_version=None,platform=None):
    "Demo Test Run"
    #Setup a driver
    driver_obj = DriverFactory()
    driver = driver_obj.get_web_driver(browser,sauce_flag,browser_version,platform)
    driver.implicitly_wait(10) # Some elements are taking long to load
    driver.maximize_window()

    #Result flag which will check if testrail.conf is present
    tconf_flag = check_file_exists(tconf)

    #Result flag used by TestRail
    result_flag = False
    
    #1. Create a login page object and login
    #Get the test account credentials from the login.credentials file
    credentials_file = os.path.join(os.path.dirname(__file__),'login.credentials')
    username = Conf_Reader.get_value(credentials_file,'LOGIN_USER')
    password = Conf_Reader.get_value(credentials_file,'LOGIN_PASSWORD')
 
    #Create a login page object
    login_obj = PageFactory.get_page_object("login",driver)
    login_obj.write(username)
    result_flag = login_obj.login(username,password)
    if (result_flag):
        msg = "Login was successful for user: %s url: %s"%(username,base_url)
    else:
        msg = "Login failed for user: %s url: %s"%(username,base_url)
    login_obj.write(msg)
    
    #Update TestRail
    #Get the case id from tesrail.conf file
    if tconf_flag:
        case_id = Conf_Reader.get_value(tconf,'VERIFY_LOGIN')
        Test_Rail.update_testrail(case_id,test_run_id,result_flag,msg=msg)

    #2. Create a project with given project name
    #Get the project name from the data.conf file
    project_name = Conf_Reader.get_value(conf,'PROJECT_NAME')

    #Create a project page object
    project_obj = PageFactory.get_page_object("project",driver)
    result_flag = project_obj.create_project(project_name)
    project_obj.wait(5)

    if (result_flag):
        msg = "Created project: %s "%project_name
    else:
        msg = "Create project failed for: %s "%project_name
    project_obj.write(msg)
    
    #Update TestRail
    #Get the case id from tesrail.conf file
    if tconf_flag:
        case_id = Conf_Reader.get_value(tconf,'CREATE_PROJECT')
        Test_Rail.update_testrail(case_id,test_run_id,result_flag,msg=msg)
    
    #3. Edit Notifications Email Preferences
    #Get the Email notification details from the data.conf file
    email_notification = Conf_Reader.get_value(conf,'EMAIL_NOTIFICATION')
    email_notification_frequency = Conf_Reader.get_value(conf,'EMAIL_NOTIFICATION_FREQUENCY')

    #Create a preferences page object
    pref_obj = PageFactory.get_page_object("preferences",driver)
    pref_obj.wait(3)
    result_flag = pref_obj.change_email_preference(email_notification,email_notification_frequency)

    if (result_flag):
        msg = "Email notification enabled and preferences set to %s"%email_notification_frequency
    else:
        msg = "Not able to set email notification"
    pref_obj.write(msg)
    
    #Update TestRail
    #Get the case id from tesrail.conf file
    if tconf_flag:
        case_id = Conf_Reader.get_value(tconf,'CHANGE_PREFERENCES')
        Test_Rail.update_testrail(case_id,test_run_id,result_flag,msg=msg)
        
    #Teardown
    pref_obj.wait(3)
    pref_obj.teardown() #You can use any page object to teardown  
    
#---START OF SCRIPT
if __name__=='__main__':
    print "Script start"
    #This script takes an optional command line argument for the TestRail run id
    usage = "\n----\n%prog -b <OPTIONAL: Browser> -c <OPTIONAL: configuration_file> -u <OPTIONAL: APP URL> -r <Test Run Id> -t <OPTIONAL: testrail_configuration_file> -s <OPTIONAL: sauce flag>\n----\nE.g.: %prog -b FF -c .conf -u https://app.fiscalnote.com -r 2 -t testrail.conf -s Y\n---"
    parser = OptionParser(usage=usage)

    parser.add_option("-b","--browser",
                      dest="browser",
                      default="firefox",
                      help="Browser. Valid options are firefox, ie and chrome")                      
    parser.add_option("-c","--config",
                      dest="config_file",
                      default=os.path.join(os.path.dirname(__file__),'data.conf'),
                      help="The full or relative path of the test configuration file")
    parser.add_option("-u","--app_url",
                      dest="url",
                      default="https://www.droptask.com",
                      help="The url of the application")
    parser.add_option("-r","--test_run_id",
                      dest="test_run_id",
                      default=None,
                      help="The test run id in TestRail")
    parser.add_option("-s","--sauce_flag",
                      dest="sauce_flag",
                      default="N",
                      help="Run the test in Sauce labs: Y or N")
    parser.add_option("-v","--version",
                      dest="browser_version",
                      help="The version of the browser: a whole number",
                      default=None)
    parser.add_option("-p","--platform",
                      dest="platform",
                      help="The operating system: Windows 7, Linux",
                      default="Windows 7")
    parser.add_option("-t","--testrail_caseid",
                      dest="testrail_config_file",
                      default=os.path.join(os.path.dirname(__file__),'testrail.conf'),
                      help="The full or relative path of the testrail configuration file")

    (options,args) = parser.parse_args()
    if check_options(options): 
        #Run the test only if the options provided are valid
        run_demo_test(browser=options.browser,
                    conf=os.path.abspath(options.config_file),
                    base_url=options.url,
                    test_run_id=options.test_run_id,
                    sauce_flag=options.sauce_flag,
                    browser_version=options.browser_version,
                    platform=options.platform,
                    tconf=os.path.abspath(options.testrail_config_file))
    else:
        print 'ERROR: Received incorrect input arguments'
        print parser.print_usage()
