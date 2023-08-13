import os
def chdir_bachelor():
      os.chdir("C:/Users/lukas/Desktop/bachelor")

def chdir_data():
      os.chdir("C:/Users/lukas/Desktop/bachelor/data")

def chdir_pdf():
      os.chdir("C:/Users/lukas/Desktop/bachelor/pdf") 

def chdir_auth():
      os.chdir("C:/Users/lukas/Desktop/bachelor/auth")      

def switch_dir(type):
      if type =="pdf":
            chdir_pdf()
      if type == "json":
            chdir_data()