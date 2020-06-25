#!usr/bin/python


import smstest # class with function to send sms
import requests # library to get and parse webpages
import time # wait before pulling page
from bs4 import BeautifulSoup # selenium
from selenium import webdriver # selenium
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
import re # regular expressions
import phonenumber_determineaction #To determine what bills and how many bills a specific phone number should recieve (Pass the dict {Date Introduced : Bills} after pulling from govtrack.us) (Step 2)


class c_getbillstodict () :
    
    def f_getsitename (self) :
        s_sn = input ("Enter site name:")
        self.s_sn = s_sn
        print ("Site name is: ", s_sn)

    #Function to access site (selenium)
    def f_visitsite_selenium (self) :
        #To run without opening browser window
        options = Options()
        Options.headless = True

        #Get elements from webpage
        driver = webdriver.Firefox()
        driver.get(self.s_sn)

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


        #Get content of interest (bills)
        bills = driver.find_element_by_xpath("/html/body/div[1]/div[4]/div[2]/section/div/div[2]").text
        driver.quit()  

        #Now you have the whole bills section, all of them
        #Next Divide them up into sections [Bill | Date Introduced | ]
        #{ Date Introduced : Bill }
        #writetofile(bills)


        #Date Introduced : [3 letters][space][1 or 2 numbers][comma][space][four numbers]
        #Date Introduced
        #[Introduced][Date]
        re_dateintroduced = re.findall("Introduced\n\D{3}\s\d{1,2}\,\s\d{4}" , bills)

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
        classins = phonenumber_determineaction.class_phonenumbersdetermineaction()
        classins.method_actionfornumber(d_di)

##################################
# Main #
##################################

## Create class object ##
o_instance =  c_getbillstodict()
## Get Site Name ##
o_instance.f_getsitename()
## Visit Site/Move to Dict ##
o_instance.f_visitsite_selenium()
