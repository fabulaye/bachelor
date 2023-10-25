
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