import regex as re

character_pattern=re.compile("[^\d,.\s]\w*")
single_number_pattern=re.compile("\d+[,.]\d*[,.]*\d*[,.]*")

def create_company_regex(name):
      company_string=str(name+"[\s*[\w\.\-]*]*") #vielleicht ohne klammern
      company_regex=re.compile(company_string) 
      return company_regex

def return_regex_hits(regex_search):
      if regex_search!=[]:
            hits=regex_search[0]
            return hits

