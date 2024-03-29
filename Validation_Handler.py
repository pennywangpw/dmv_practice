import datetime
from datetime import datetime

class ValidationHandler:
    def __init__(self):
        pass


    #check if the each word in user_input can be changed to number
    def check_is_num(self,user_input):
        for word in user_input:
            try:
                int(word)
            except:
                return False
        return True

    #check if the word can be changed to number
    def check_convert_into_num(self,word):
        res = False
        try:
            int(word)
            res =  True
        except:
            return res
        return res

    #check if the length of zipcode is correct
    def check_length_zipcode_input_validtion(self,word):
        if len(word) == 5:
            return True
        return False

    #check if datetime formate
    def check_datetime_formate_validation(self,word):
        try:
            date_obj = datetime.strptime(word, "%Y%m%d")
            return True
        except:
            return False

    #date and zipcode input validation
    def date_zipcode_input_validation(self,input_date,input_zipcode):
        if not isinstance(input_date,str):

            return "The input_date should be a string type with YYYY-MM-DD"
        elif not isinstance(input_zipcode, int):

            return "Invalid zipcode"
        else:
            try:
                date_obj = datetime.strptime(input_date, "%Y-%m-%d")

            except ValueError as e:
                return e

    # V2 - date and zipcode input validation- check datetime formate & zipcode formate with correct length
    def date_zipcode_input_validation_V2(self,user_input):
        print(f"傳入function user_input list  {user_input} {type(user_input)}")
        if_date = False
        if_zipcode = False
        for word in user_input:
            if self.check_datetime_formate_validation(word):
                if_date = True
                continue
            elif self.check_convert_into_num(word) and self.check_length_zipcode_input_validtion(word):
                if_zipcode = True
                continue

        if if_date and if_zipcode:
            return "pass"

        return "NOT PASS VALIDATION. This is invalid input.\nPlease provide the date you have (YYYY-MM-DD) and zipcode (i.e. 98087)"

    def check_zipcode_datetime_provided_and_valid(self,user_input):
        input_zipcode= None
        input_datetime= None
        for word in user_input:
            if self.check_length_zipcode_input_validtion(word):
                input_zipcode = word
            elif self.check_datetime_formate_validation(word):
                input_datetime = word

        if input_zipcode != None and input_datetime != None:
            return input_zipcode,input_datetime




    def find_mile_range(self,user_input):
        mile_range = False
        for word in user_input:
            print("user intput word: ",word)
            #check if mile in word
            if "mile" in word and not word.startswith("m"):
                mile_range = word[0:word.find("mile")]
                break

            elif "mile" in word and word.startswith("m"):
                print("word word.find()): ",word, word.find("mile"))
                mile_range = user_input[user_input.index(word)-1]
                break


        return mile_range
