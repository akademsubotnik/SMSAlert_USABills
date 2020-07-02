#!/usr/bin/python


#In this file you will send the single bill to the phone
import smtplib
import re

class c_sendtophone :

    # def send(self,message):
    #     carriers = carriers = {
    #         'att':    '@mms.att.net',
    #         'tmobile':' @tmomail.net',
    #         'verizon':  '@vtext.com',
    #         'vzpix' : '@vzwpix.com',
    #         'sprint':   '@page.nextel.com'
    #     }

    def __init__(self, arg_bill, arg_phonenumber, arg_phonecarrier) :
        self.bill = arg_bill
        self.phonenumber = arg_phonenumber
        self.phonecarrier = arg_phonecarrier        

    def f_sendtophone (self) :
        ## STUB ##
        # Replace the number with your own, or consider using an argument\dict for multiple people.
        #to_number = '9145821666{}'.format(carriers['vzpix'])
        str_phonenumber = str(self.phonenumber) + '{}'
        to_number = str_phonenumber.format(self.phonecarrier) # <-- You may need to change the format, to match the above
        auth = ('{email}@gmail.com', '{password}')
        
        # Establish a secure session with gmail's outgoing SMTP server using your gmail account
        server = smtplib.SMTP( "smtp.gmail.com", 587 )
        server.starttls()
        server.login(auth[0], auth[1])

        # Send text message through SMS gateway of destination number
        server.sendmail( auth[0], to_number, self.bill)
        

