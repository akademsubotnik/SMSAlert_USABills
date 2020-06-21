#!usr/bin/python


#There are 11,593 bills and resolutions that have been introduced or reported by committee and await further action. (https://www.govtrack.us/congress/bills/browse?status=1,3&sort=-current_status_date)
# A program to parse https://www.govtrack.us/congress/bills/browse?status=1,3&sort=-current_status_date for certain keywords which would then trigger a reply to senators and representatives.  If the bill supports Ukraine reply that you support the bill.  If the bill supports Russia reply that you do not suport the bill.

import smstest # class with function to send sms
import requests # library to get and parse webpages
import time # wait before pulling page
from bs4 import BeautifulSoup # selenium
from selenium import webdriver # selenium
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
import re # regular expressions

##################################
# Function Definitions #
##################################
str_sitename = 'https://www.govtrack.us/congress/bills/browse?status=1,3&sort=-current_status_date#current_status[]=1,3&text=Ukraine'
str_sitename2 = 'https://www.govtrack.us/congress/bills/'

#Function to access site (selenium)
def visitsite_selenium() :
    #To run without opening browser window
    options = Options()
    Options.headless = True

    #Get elements from webpage
    driver = webdriver.Firefox()
    driver.get(str_sitename)

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
    dict_di = dict (zipObj)

    #Write to file
    passtophonenumbers(dict_di)


    
    
#Function to write to file
def passtophonenumbers(arg_object) :
    try :
        #Iterate thru phone numbers and check if they have a file created for themselves, if not make a file name phonenumber_bills.txt with the contents of the dictionary.  
        
    except Exception :
        print ("Error", Exception)





##################################
# Main #
##################################
        
visitsite_selenium()
object_smstest = smstest.class_sendtophone()





#Obtain the # of messages sent out per day.  Do not exceed 3, have a counter for each phone number that resets to 0 at the start of each day
#Along with the name of the bill include a date of introuced/date of last activity (if it has)
