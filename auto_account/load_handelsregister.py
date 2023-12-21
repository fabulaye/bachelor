import jsonlines
from import_manager import import_file_manager
import_file_manager()
from file_manager.dict_to_json import dict_to_json
def load_handelsregister():
      handelsregister=jsonlines.open('C:/Users/lukas/Desktop/bachelor/data/handelsregister.jsonl')
      return handelsregister
handelsregister=load_handelsregister()


