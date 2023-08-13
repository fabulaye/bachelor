import os
def del_jpg():
      for file in os.listdir("C:/Users/lukas/Desktop/bachelor/pdf"):
            if file.endswith(".jpg"):
                  os.remove(file)