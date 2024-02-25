from file_manager.list_to_string import list_to_string

def txt_to_str(path):
  with open(path,"r",encoding="utf-8") as f:
      text=f.readlines()
  text=list_to_string(text)
  return text