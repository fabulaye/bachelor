from json_to_dict import json_to_dict
from change_directory import chdir_data
def create_gaming_company_names_underscored_json():
      chdir_data()
      dict={}
      dict["names"]=[]
      names=json_to_dict("gaming_company_names.json")
      names=names["names"]
      for name in names:
            new_name=name.replace(" ","_")
            dict["names"].append(new_name) 
      json_to_dict(dict,"gaming_company_names_underscored_dict")  