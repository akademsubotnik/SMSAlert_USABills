
#!/usr/bin/python

import os
import re
import sendtophone

# Recieve bills from {billparser.py} > Remove last bill > Send to phone {sendtophone.py} > Write to #.txt

class c_phonenumbersdetermineaction :

    # def send(self,message):
    #     carriers = carriers = {
    #         'att':    '@mms.att.net',
    #         'tmobile':' @tmomail.net',
    #         'verizon':  '@vtext.com',
    #         'vzpix' : '@vzwpix.com',
    #         'sprint':   '@page.nextel.com'
    #     }
          
    
    def __init__ (self) :
        dict_numbercarrier = {19145821666 : "@vzpix.com", 19145824751 : "@redpocketmobile.com", 19147037991 : "@vzpix.com"}
        self.dict_numbercarrier = dict_numbercarrier
    
    def f_actionfornumber (self, arg_stringmessage) :
        
        self.string_message = arg_stringmessage
        for i in self.dict_numbercarrier :
            #If File #.txt exists
            if (os.path.exists("/home/greg/Projects/Projects/python/BillParser_Project/phonenumber_files/{0}.txt".format(i)) ) :
                try :
                    file_obj = open ("/home/greg/Projects/Projects/python/BillParser_Project/phonenumber_files/{0}.txt".format(i), "r")
                    str_fromfile = file_obj.read()
                    l_fromfile = str_fromfile.split('", "')
                    l_lastelement = l_fromfile.pop()
                    file_obj.close()

                    #Send to phone
                    classins = sendtophone.c_sendtophone()
                    classins.f_sendtophone(l_lastelement, i, self.dict_numbercarrier[i])
                    #print (l_lastelement, i, self.dict_numbercarrier[i])

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
                #print (l_lastelement0, i, self.dict_numbercarrier[i])
                #sendtophonefile (l_lastelement0, i, self.dict_numbercarrier[i]) # <-- contains the last bill/phonenumber/phonecarrier
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
