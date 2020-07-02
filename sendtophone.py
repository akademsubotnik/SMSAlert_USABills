#!/usr/bin/python


#In this file you will send the single bill to the phone

class c_sendtophone :

    def f_sendtophone (self, arg_bill, arg_phonenumber, arg_phonecarrier) :
        self.arg_bill = arg_bill
        self.arg_phonenumber = arg_phonenumber
        self.arg_phonecarrier = arg_phonecarrier

        print ("AB", self.arg_bill)
        print ("APN", self.arg_phonenumber)
        print ("APC", self.arg_phonecarrier)
