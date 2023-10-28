import regex as re

rechtsform_regex=re.compile("GmbH|UG|AG|KG|Unternehmensgesellschaft")


def return_rechtsform(company_name):
      rechtsform=rechtsform_regex.findall(company_name)
      if rechtsform !=[]:
            rechtsform=rechtsform[0]
            return rechtsform