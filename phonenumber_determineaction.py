#!/usr/bin/python

import os
import re

#Use this class to create what you will send to the phonenumbers dictionary
#Store what you will send the 3 bills in a list
#(These numbers should contain the bills/what you pulled from govtrack.us)


class c_phonenumbersdetermineaction :

    def __init__ (self) :
        list_phonenumbers = [19145821666, 19145824751, 19147037991]
        self.list_phonenumbers = list_phonenumbers
    
    #Method to determine what do
    def f_actionfornumber (self, arg_stringmessage) :
        
        self.string_message = arg_stringmessage
        for i in self.list_phonenumbers :
            #If File #.txt exists
            if (os.path.exists("/home/greg/Projects/Projects/python/BillParser_Project/phonenumber_files/{0}.txt".format(i)) ) :
                try :
                    #Send the top 3 from that file and then remove them
                    file_obj = open ("/home/greg/Projects/Projects/python/BillParser_Project/phonenumber_files/{0}.txt".format(i), "r")
                    #Contains txt file
                    str_fromfile = file_obj.read()
                    #Move into list, remove first element and send to phone and return to list with the one element removed
                    l_fromfile = str_fromfile.split("', '")
                    l_lastelement = l_fromfile.pop()
                    file_obj.close()
                    print(l_lastelement)
                    

                    # Delete File #
                    os.remove("/home/greg/Projects/Projects/python/BillParser_Project/phonenumber_files/{0}.txt".format(i))
                    # Create File #
                    file_objwrite = open ("/home/greg/Projects/Projects/python/BillParser_Project/phonenumber_files/{0}.txt".format(i), "w")
                    # Write to File List minus last element #
                    file_objwrite.write(str(l_fromfile))
                    file_objwrite.close()
                    # Send to phone the last list element #
                    
                    
                except IOError :
                    print ("Error! Problem Opening File", IOError)

            #If file does not exist for number create a neew file that contains all of the bills with the format of #.txt
            else:
                #Create a file #.txt
                try :
                    #Create File Here FOLLOW DICTIONARY WRITING TO FILE RULES
                    with open ("/home/greg/Projects/Projects/python/BillParser_Project/phonenumber_files/{0}.txt".format(i), "w") as file_obj:
                        #Write to File
                        try :
                            print (self.string_message, file=file_obj)
                        except IOError :
                            print ("Error! Problem Writing To File", IOError)
                        file_obj.close()
                except IOError :
                    print ("Error! Problem Creating File", IOError)


## Main () ##
