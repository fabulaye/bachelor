from pdf_to_txt import pdf_to_txt
import os
def create_text_for_all_files_in_dir():
      dir_list=os.listdir("C:/Users/lukas/Desktop/bachelor/pdf")
      for file in dir_list:
            if file.endswith(".pdf"):
                  file=file.rstrip(".pdf")
                  text_name=file+".txt"
                  if text_name not in dir_list:
                        print("new pdf found")
                        pdf_to_txt(file) #hier werden die texdokumente erstellt etc.
create_text_for_all_files_in_dir()