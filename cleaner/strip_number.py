import regex as re

single_number_pattern=re.compile("\d+[,.]\d*[,.]*\d*[,.]*")

def clean_numbers(list):
      new_list=[]
      for entry in list:
            if single_number_pattern.findall(entry)!=[]:
                  split=entry.split()
                  for string in split:
                        try: #wir haben hier anscheinend auch strings drin
                              string=string.replace(".","")
                              string=string.replace(",",".") #deutsche schreibeweise zur englischen
                              string=float(string)
                              new_list.append(string)
                        except:
                              None      
      return new_list   

def strip_number(number):
      counter=0
      number=number.replace(".","")
      for character in number:
            if character==",":
                  counter+=1
      if counter>=2:
            return "FormatError"           
      if counter<=1:
            number=number.replace(",",".") #deutsche schreibeweise zur englischen
            print(number)
            number=float(number) 
            return number
   