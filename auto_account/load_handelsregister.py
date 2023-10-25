import jsonlines
def load_handelsregister():
      handelsregister=jsonlines.open('C:/Users/lukas/Desktop/bachelor/data/handelsregister.jsonl')
      return handelsregister
handelsregister=load_handelsregister()