
#!usr/bin/python


import smstest # class with function to send sms
import requests # library to get and parse webpages
import time # wait before pulling page
from bs4 import BeautifulSoup # selenium
from selenium import webdriver # selenium
from selenium.webdriver.firefox.options import Options #To fetch webpage headless
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re # regular expressions
import phonenumber_determineaction #To determine what bills and how many bills a specific phone number should recieve (Pass the dict {Date Introduced : Bills} after pulling from govtrack.us) (Step 2)


def f_getsitename (arg_sitename) :
    return arg_sitename
        
class c_getbillstodict () :

    def __init__ (self, arg_sitename) :
        self.s_sn = arg_sitename
        # https://stackoverflow.com/questions/5370762/how-to-hide-firefox-window-selenium-webdriver #
        # START #
        firefox_options = Options()
        firefox_options.add_argument('--headless')
        firefox_options.add_argument('--disable-gpu')
        self.driver = webdriver.Firefox(options=firefox_options)
        # END #

        self.bills = []

    def f_trytoaccesssite(self) :
        try :
            self.driver.get(self.s_sn)
        except Exception :
            print ("Unable to load page:", Exception)

    def f_dosomepagestuff (self) :
        
        ## TRY TO FETCH BILL RESULTS (Make sure page fully loads) ##
        # https://stackoverflow.com/questions/26566799/wait-until-page-is-loaded-with-selenium-webdriver-for-python #
        ## START ##
        timeout = 5
        try:
            element_present = EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[4]/div[2]/section/div/div[2]/div[1]'))
            WebDriverWait(self.driver, timeout).until(element_present)
        except TimeoutException:
            print ("Timed out waiting for page to load",TimeoutException)
        ## END ##
        
        #Go to bottom of page
        ## https://stackoverflow.com/questions/20986631/how-can-i-scroll-a-web-page-using-selenium-webdriver-in-python  ##
        SCROLL_PAUSE_TIME = 0.5

        #Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True :
            #Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            #Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            #Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height :
                break
            last_height = new_height

        ## END  ##

        ## Make Sure to Check to page was loaded, if not throw an exception ##
        self.bills = self.driver.find_element_by_xpath("/html/body/div[1]/div[4]/div[2]/section/div/div[2]").text
        self.driver.quit()


    def f_sanitizebills (self) :
        #{ Date Introduced : Bill }

        #Date Introduced
        re_dateintroduced = re.findall("Introduced\n\D{3}\s\d{1,2}\,\s\d{4}" , self.bills)
        # Start Sanitize #
        re_dateintroduced = re.sub('\'', '', str(re_dateintroduced)) # Remove ' character       
        ## START ##
        # https://stackoverflow.com/questions/25384333/python-re-sub-replace-substring-with-string
        re_dateintroduced = re.sub('\s(?=I)' , '', str(re_dateintroduced)) # A space followed by a I (Look ahead buffer)
        re_dateintroduced = re.sub("n(?=[A-Z])" , '', str(re_dateintroduced)) # A n followed by a capitol letter (Look ahead buffer)
        ## END ##
        re_dateintroduced = re.sub(r'\\' , ' ', str(re_dateintroduced)) # Replace \ with a space (https://bugs.python.org/issue29015)
        # End Sanitize #

        
        #Bills
        re_bills = re.findall("[A-Z]\..*\:.+\n+?(?=Sponsor)",self.bills)
        # Start Sanitize #
        re_bills = re.sub('\'', '', str(re_bills)) # Remove ' character
        re_bills = re.sub(r'\\' , ' ', str(re_bills)) # Replace \ with a space (https://bugs.python.org/issue29015)
        re_bills = re.sub("(?<= )n(?=\,)" , '', str(re_bills)) # Replace n with space before and , after with nothing
        re_bills = re.sub("(?<= )n(?=\])" , '', str(re_bills)) # Replace n with space before and ] after with nothing
        # End Sanitize #

        #THIS SHOULD BE ANOTHER FUNCTION?
        ## START ##
        #Join list re_dateintroduced and list re_bills
        ## re_dateintroduced and re_bills were strings making them lists again so that you can combine them into a single dicitonary with zip (list1,list2) function##
        re_dateintroduced = re_dateintroduced.split(",I")
        re_bills = re_bills.split(", ")
        
        zipObj = zip (re_dateintroduced, re_bills)
        d_di = dict (zipObj)
        print (d_di)
        ## END ##
        
    #Function to access site (selenium)
    #def f_visitsite_selenium (self) : 
        #Pass to phonenumber_determineaction file
        #classins = phonenumber_determineaction.c_phonenumbersdetermineaction()
        #classins.f_actionfornumber(d_di)
        #print ("f_visit_selenium")
        
##################################
# Main #
##################################

str_sitename = f_getsitename("https://www.govtrack.us/congress/bills/browse?status=1,3&sort=-current_status_date#current_status[]=1,3&text=Ukraine")

## Create class object ##
o_instance =  c_getbillstodict(str_sitename)

## Try to access site ##
o_instance.f_trytoaccesssite()
## Do Some Page stuff ##
o_instance.f_dosomepagestuff()
## Sanitize Bills ##
o_instance.f_sanitizebills()

