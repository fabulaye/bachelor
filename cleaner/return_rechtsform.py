import regex as re

rechtsform_regex=re.compile("UG \(haftungsbeschränkt\)|UG|AG|eG|Unternehmensgesellschaft|e\.k|GmbH & Co\. KG|mbH|PartG|GbR|PartG|StGes|SE|KGaA|Handelsgesellschaft mit beschränkter Haftung|Gesellschaft mit beschränkter Haftung|KG|GmbH",flags=re.I)


def return_rechtsform(company_name):
      rechtsform=rechtsform_regex.findall(company_name)
      if rechtsform !=[]:
            rechtsform=rechtsform[0]
            return rechtsform