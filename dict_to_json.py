import os
import json
def dict_to_json(dict,title,directory="C:/Users/lukas/Desktop/bachelor/data"):
      os.chdir(directory)
      with open(title+".json", "w") as outfile:
            json_file=json.dumps(dict)
            outfile.write(json_file)
            print("file changed")
