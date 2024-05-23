import regex as re
from import_manager import import_txt_pdf,import_file_manager
import_file_manager()
import_txt_pdf()
from txt_pdf.read_txt import read_txt
from file_manager.change_directory import chdir_txt

"[\w\d\s,öä\.]+\d$"  
"\s[\d,\.]+" 
"(\s[\d,\.]+)+"                                           
numbers_string="\s[\d,\.]+"
print(numbers_string)

pattern=re.compile("(\s[\d,\.]+)+")

#aktiva
aktiva_regex=re.compile("Aktiva"+numbers_string,flags=re.I)
anlagevermögen_regex=re.compile("Anlagevermögen"+numbers_string,flags=re.I) #oberkategorie von sachanlagen
sachanlagen_regex=re.compile("Sachanlagen"+numbers_string,flags=re.I)  
umlaufvermögen_regex=re.compile("umlaufvermögen"+numbers_string,flags=re.I)
#umlaufvermögen children
vorräte_regex=re.compile("vorräte"+numbers_string,flags=re.I)
forderungen_regex_string="forderungen"+numbers_string+"|forderungen und sonstige vermögensgegenstände"+numbers_string
forderungen_regex=re.compile(forderungen_regex_string,flags=re.IGNORECASE)
kassenbestand_regex=re.compile("kassenbestand"+numbers_string,flags=re.I)

chdir_txt()
text=read_txt("2tainment2019.txt")

def regex_test(pattern,text):
    for word in text:
        search=pattern.findall(word)
        if search!=[]:
            print(search)
    

regex_test(vorräte_regex,text)