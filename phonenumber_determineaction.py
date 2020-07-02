
#!/usr/bin/python

import os
import re

# Recieve bills from {billparser.py} > Remove last bill > Send to phone {sendtophone.py} > Write to #.txt

class c_phonenumbersdetermineaction :

    def __init__ (self) :
        list_phonenumbers = [19145821666, 19145824751, 19147037991]
        self.list_phonenumbers = list_phonenumbers
    
    def f_actionfornumber (self, arg_stringmessage) :
        
        self.string_message = arg_stringmessage
        for i in self.list_phonenumbers :
            #If File #.txt exists
            if (os.path.exists("/home/greg/Projects/Projects/python/BillParser_Project/phonenumber_files/{0}.txt".format(i)) ) :
                try :
                    file_obj = open ("/home/greg/Projects/Projects/python/BillParser_Project/phonenumber_files/{0}.txt".format(i), "r")
                    str_fromfile = file_obj.read()
                    l_fromfile = str_fromfile.split('", "')
                    l_lastelement = l_fromfile.pop()
                    file_obj.close()
                    #sendtophonefile (l_lastelement, l_phonenumber, carrier) # <-- contains the last bill # You should also send the phone number as well #Send carrier also

                    # Delete File #
                    os.remove("/home/greg/Projects/Projects/python/BillParser_Project/phonenumber_files/{0}.txt".format(i))
                    # Create File #
                    file_objwrite = open ("/home/greg/Projects/Projects/python/BillParser_Project/phonenumber_files/{0}.txt".format(i), "w")                 
                    file_objwrite.write(str(l_fromfile).replace("\\","")) # Remove \
                    file_objwrite.close()
                                        
                except IOError :
                    print ("Error! Problem Opening File", IOError)

            #If file does not exist for number create a neew file that contains all of the bills with the format of #.txt
            else:
                list_stringmessage = str(self.string_message).split("', '") # Split the variable into a list and get the last element of the list
                l_lastelement0 = list_stringmessage.pop()                
                #sendtophonefile (l_lastelement0) # <-- contains the last bill
                #Create a file #.txt
                try :
                    file_obj0 = open("/home/greg/Projects/Projects/python/BillParser_Project/phonenumber_files/{0}.txt".format(i), "w")
                    #Write to File
                    try :                        
                        file_obj0.write(str(list_stringmessage)) # list_stringmessage contains the bills (minus last bill)
                    except IOError :
                        print ("Error! Problem Writing To File", IOError)
                        file_obj0.close()
                except IOError :
                    print ("Error! Problem Creating File", IOError)


## Main () ##
