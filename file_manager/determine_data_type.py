import regex as re


datatype_regex=re.compile("pdf|json|txt|xlsx")

def determine_data_type(file_name): #vielleicht in einem anderen module?
      datatype=re.search(datatype_regex,file_name).group()
      return datatype