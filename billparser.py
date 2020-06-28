
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


class c_getbillstodict () :
    
    def f_getsitename (self) :
        #s_sn = input ("Enter site name:")
        s_sn = "https://www.govtrack.us/congress/bills/browse?status=1,3&sort=-current_status_date#current_status[]=1,3&text=Ukraine"
        #s_sn = "asdfasdfasdf"
        self.s_sn = s_sn

    #Function to access site (selenium)
    def f_visitsite_selenium (self) :
        #To run without opening browser window
        # https://stackoverflow.com/questions/5370762/how-to-hide-firefox-window-selenium-webdriver #
        # START #
        firefox_options = Options()
        firefox_options.add_argument('--headless')
        firefox_options.add_argument('--disable-gpu')
        driver = webdriver.Firefox(options=firefox_options)
        # END #
        
        #Try to connect to website
        try :
            #Get elements from webpage
            driver.get(self.s_sn)
        except Exception :
            print ("Unable to load page:", Exception)

        ## TRY TO FETCH BILL RESULTS (Make sure page fully loads) ##
        # https://stackoverflow.com/questions/26566799/wait-until-page-is-loaded-with-selenium-webdriver-for-python #
        ## START ##
        timeout = 5
        try:
            element_present = EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[4]/div[2]/section/div/div[2]/div[1]'))
            WebDriverWait(driver, timeout).until(element_present)
        except TimeoutException:
            print ("Timed out waiting for page to load",TimeoutException)
        ## END ##
        
        #Go to bottom of page
        ## https://stackoverflow.com/questions/20986631/how-can-i-scroll-a-web-page-using-selenium-webdriver-in-python  ##
        SCROLL_PAUSE_TIME = 0.5

        #Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True :
            #Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            #Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            #Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height :
                break
            last_height = new_height

        ## END  ##

        ## Make Sure to Check to page was loaded, if not throw an exception ##
        #Get content of interest (bills)
        bills = driver.find_element_by_xpath("/html/body/div[1]/div[4]/div[2]/section/div/div[2]").text
        driver.quit()  

        #Now you have the whole bills section, all of them
        #Next Divide them up into sections [Bill | Date Introduced | ]
        #{ Date Introduced : Bill }
        #Date Introduced : [3 letters][space][1 or 2 numbers][comma][space][four numbers]
        #Date Introduced
        #[Introduced][Date]
        re_dateintroduced = re.findall("Introduced\n\D{3}\s\d{1,2}\,\s\d{4}" , bills)
        re_dateintroduced = re.sub('\'', '', str(re_dateintroduced)) # Remove ' character
        
        ## START ##
        # https://stackoverflow.com/questions/25384333/python-re-sub-replace-substring-with-string
        re_dateintroduced = re.sub('\s(?=I)' , '', str(re_dateintroduced)) # A space followed by a I (Look ahead buffer)
        re_dateintroduced = re.sub("n(?=[A-Z])" , '', str(re_dateintroduced)) # A n followed by a capitol letter (Look ahead buffer)
        ## END ##

        re_dateintroduced = re.sub(r'\\' , ' ', str(re_dateintroduced)) # Replace \ with a space (https://bugs.python.org/issue29015)
        
        
        print (re_dateintroduced)

        
        
        #Bills
        #[1 letter][dot][0 to 3 letters][NOTHING or dot][space][#][colon]
        #zn = re.findall("[A-Z]\..*\:", bills) # This print H.Res. #:
        re_bills = re.findall("[A-Z]\..*\:.+\n+?(?=Sponsor)",bills)


        #Join list re_dateintroduced and list re_bills
        zipObj = zip (re_dateintroduced, re_bills)
        #Create a dictionary from zip object
        #{ Date Introduced : Bill }
        d_di = dict (zipObj)

        #Pass to phonenumber_determineaction file
        #classins = phonenumber_determineaction.c_phonenumbersdetermineaction()
        #classins.f_actionfornumber(d_di)

##################################
# Main #
##################################

## Create class object ##
o_instance =  c_getbillstodict()
## Get Site Name ##
o_instance.f_getsitename()
## Visit Site/Move to Dict ##
o_instance.f_visitsite_selenium()
