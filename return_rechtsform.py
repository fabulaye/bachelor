import regex as re

rechtsform_regex=re.compile("UG\s*\(haftungsbeschränkt\)|UG|AG|eG|Unternehmensgesellschaft|e\.k|GmbH & Co\. KG|mbH|PartG|GbR|PartG|StGes|SE|KGaA|Handelsgesellschaft mit beschränkter Haftung|Gesellschaft mit beschränkter Haftung|KG|GmbH") #wir müssen es case sensitive machen, möglicherweise sind wir jetzt zu restriktiv #flags=re.I


def return_rechtsform(company_name):
      rechtsform=rechtsform_regex.findall(company_name)
      if rechtsform !=[]:
            rechtsform=rechtsform[0]
            return rechtsform
      
def strip_rechtsform(company_name):
    rechtsform_regex_search=rechtsform_regex.findall(company_name)[0]
    if rechtsform_regex_search!="":
        company_name=company_name.rstrip(rechtsform_regex_search).lower().rstrip()
    return company_name     

test=return_rechtsform("TSG Ludwigshafen-Friesenheim Bundesliga-Handball GmbH")
print(test)