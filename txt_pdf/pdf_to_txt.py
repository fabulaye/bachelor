import os
import pdf2image
from import_manager import import_file_manager
import_file_manager()
from file_manager.del_jpg import del_jpg
import pytesseract as pyt
from file_manager.change_directory import chdir_txt

pyt.pytesseract.tesseract_cmd = 'E:/tesseract/tesseract' #nneds to point to .exe
tesserect_link="https://tesseract-ocr.github.io/tessdoc/ImproveQuality.html"

def pdf_to_txt(pdf_name,pdf_path="C:/Users/lukas/Desktop/bachelor/pdf",txt_path="C:/Users/lukas/Desktop/bachelor/pdf"): #create jpgs from the pdf, create txt from the pictures, and delete the pictures
      os.chdir(pdf_path)
      pages=pdf2image.pdf2image.convert_from_path(pdf_name+".pdf",poppler_path="C:/Users/lukas/Desktop/bachelor/pdf/poppler-23.05.0/Library/bin")
      pdf_string=""
      for i in range(len(pages)):
            pages[i].save("page"+str(i)+".jpg","JPEG")
            page_string=pyt.image_to_string("page"+str(i)+".jpg",lang="deu",config="--psm 4")
            pdf_string=pdf_string+" "+page_string  
      del_jpg()         
      chdir_txt()          
      with open(pdf_name+".txt","w") as f:
            f.write(pdf_string) 
               
