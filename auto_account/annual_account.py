import regex as re
from import_manager import import_cleaner
import_cleaner()
from cleaner.strip_number import strip_number

class flag():
      def __init__(self) -> None:
            self.status=False
            self.logical_error=False
            self.recognized_value_missing=False
            self.multiple_values=False
            self.format_error=False
            self.recognized_values=[]

class account_item():
      def __init__(self,name,regex,values=[],items=[],children=[],account_id=None):
            self.name=name
            self.regex=regex
            self.items=items
            self.has_children=False  
            self.flag=flag()
            self.values=[] 
            self.recognized_value=0 
            self.theoretical_value=0
            self.children=children
            self.account_id=account_id
      def update_data(self):
            if len(self.values)>=1: #eigentlich sollten wir bei len 0 nen non haben aber passt nicht
                  self.recognized_value=self.values[0]
            if len(self.children)>=1:
                  sum=0
                  #self.theoretical_value=[sum,[]]
                  for child in self.children:
                        try:	
                              sum+=child.recognized_value
                        except:
                              print("couldnt sum children")      
                  self.theoretical_value=sum             
      def flag_entry(self):
            if self.theoretical_value!=self.recognized_value and self.theoretical_value!=0:
                  self.flag.logical_error=True
                  self.flag.status=True        
            if len(self.values)==0:
                  self.flag.recognized_value_missing=True
                  self.flag.status=True 
            if  len(self.values)>1:
                  self.flag.multiple_values=True      
                  self.flag.status=True  
      def update_recognized_values(self):
            number_pattern=re.compile("\d+[\.,\d]*")
            recognized=[]
            for string in self.account_id.text:
                  if self.regex.findall(string)!=[]:
                        item=self.regex.findall(string)[0] #return immer eine liste mit nur einem eintrag
                        recognized.append(item)   
            if len(recognized)>=1:
                  for value in recognized:
                        number=number_pattern.findall(value)[0]
                        try:
                              number=strip_number(number)
                        except:
                              print("something wrong with the numbers")      
                        if number=="FormatError":
                              self.flag.format_error=True
                        else:      
                              self.values.append(number)            
      def __str__(self) -> str:
            return self.name      
         


class annual_account():
      def __init__(self,):
            self.text=""
            
            #children umlaufvermögen
            self.vorräte=account_item("vorräte",vorräte_regex,account_id=self)
            self.forderungen=account_item("forderungen",forderungen_regex,account_id=self)
            self.kassenbestand=account_item("kassenbestand",kassenbestand_regex,account_id=self)
            self.wertpapiere=account_item("wertpapiere",wertpapiere_regex,account_id=self)
            #self.jahresfehlbetrag=account_item("jahresfehlbetrag",jahresfehlbetrag_regex)
            self.fehlbetrag=account_item("fehlbetrag",fehlbetrag_regex,account_id=self)
            #children aktiva
            self.umlaufvermögen=account_item("umlaufvermögen",umlaufvermögen_regex,children=[self.vorräte,self.forderungen,self.kassenbestand,self.wertpapiere],account_id=self)

            self.sachanlagen=account_item("sachanlagen",sachanlagen_regex,account_id=self)
            self.finanzanlagen=account_item("fehlbetrag",finanzanlagen_regex,account_id=self)
            self.immaterielle_vermögensgegenstände=account_item("immaterielle_vermögensgegenstände",immaterielle_vermögensgegenstände_regex,account_id=self)
            self.anlagevermögen=account_item("anlagevermögen",anlagevermögen_regex,children=[self.sachanlagen,self.finanzanlagen,self.immaterielle_vermögensgegenstände],account_id=self)
            self.rechnungsabgrenzungsposten=account_item("rechnungsabgrenzungsposten",rechnungsabgrenzungsposten_regex,account_id=self)
            
            

            self.aktiva=account_item("aktiva",aktiva_regex,children=[self.anlagevermögen,self.umlaufvermögen,self.rechnungsabgrenzungsposten,self.fehlbetrag],account_id=self)
            #children passiva
            self.gewinnrücklage=account_item("gewinnrücklage",gewinnrücklage_regex,account_id=self)
            self.kapitalrücklage=account_item("kapitalrücklage",kapitalrücklage_regex,account_id=self)
            self.gezeichnetes_kapital=account_item("gezeichnetes_kapital",gezeichnetes_kapital_regex,account_id=self)
            self.eingefordertes_kapital=account_item("eingefordertes_kapital",eingefordertes_kapital_regex,children=[self.gezeichnetes_kapital],account_id=self)
            self.verlustvortrag=account_item("verlustvortrag",verlustvortrag_regex,account_id=self)
            self.überschuss=account_item("überschuss",überschuss_regex,account_id=self)
            self.gewinnvortrag=account_item("gewinnvortrag",gewinnvortrag_regex,account_id=self)
            self.bilanzgewinn=account_item("bilanzgewinn",bilanzgewinn_regex,account_id=self)
            #bei activision: kapitalrücklage,gewinnvortrag.jahresüberschuss teil von ek
            self.bilanzverlust=account_item("bilanzverlust",bilanzverlust_regex,account_id=self)
            self.eigenkapital=account_item("eigenkapital",eigenkapital_regex,children=[self.bilanzgewinn,self.gewinnrücklage,self.gewinnvortrag,self.fehlbetrag,self.kapitalrücklage,self.verlustvortrag,self.eingefordertes_kapital,self.bilanzverlust],account_id=self)
            self.rückstellungen=account_item("rückstellungen",rückstellungen_regex,account_id=self)
            #es gibt restlaufzeit unter einem jahr,sonstige verbindlichkeiten
            self.verbindlichkeiten=account_item("verbindlichkeiten",verbindlichkeiten_regex,account_id=self)
            
            self.passiva=account_item("passiva",passiva_regex,children=[self.eigenkapital,self.rückstellungen,self.verbindlichkeiten],account_id=self)
            #self.bilanzsumme_aktiva=account_item("bilanzsumme_aktiva",bilanzsumme_regex)
            self.all_items=[self.vorräte,self.forderungen,self.kassenbestand,self.gewinnvortrag,self.fehlbetrag,self.umlaufvermögen,self.anlagevermögen,self.rechnungsabgrenzungsposten,self.eigenkapital,
                            self.aktiva,self.rückstellungen,self.verbindlichkeiten,self.passiva,self.gezeichnetes_kapital,self.eingefordertes_kapital,self.überschuss,self.gewinnvortrag,self.wertpapiere,self.immaterielle_vermögensgegenstände
                            ,self.kapitalrücklage,self.bilanzverlust,self.gewinnrücklage,self.bilanzgewinn] #reihenfolge in all_items produziert bugs
            

            self.first_layer=[self.aktiva,self.passiva]
            self.second_layer=[self.anlagevermögen,self.umlaufvermögen,self.rechnungsabgrenzungsposten,self.fehlbetrag,self.eigenkapital,self.rückstellungen,self.verbindlichkeiten]
            self.third_layer=[self.kapitalrücklage,self.vorräte,self.forderungen,self.wertpapiere,self.kassenbestand,self.gewinnvortrag,self.fehlbetrag,self.verlustvortrag,self.eingefordertes_kapital,self.finanzanlagen,self.sachanlagen,self.immaterielle_vermögensgegenstände
                              ,self.bilanzverlust,self.gewinnrücklage,self.bilanzgewinn]
            self.fourth_layer=[self.gezeichnetes_kapital,]
            self.dict={}
            self.flag_dict={}
      def create_dict(self):
            for aktivapassiva in self.first_layer:
                  self.dict[aktivapassiva.name]={"recognized_value":aktivapassiva.recognized_value,"theoretical_value":aktivapassiva.theoretical_value,"children":{}}
                  for child in aktivapassiva.children:
                        dict={}
                        dict[child.name]={"recognized_value":child.recognized_value,"theoretical_value":child.theoretical_value,"children":{}}
                        self.dict[aktivapassiva.name]["children"].update(dict)
                        if len(child.children)>=1:
                              for grandchild in child.children:
                                    dict_two={}
                                    dict_two[grandchild.name]={"recognized_value":grandchild.recognized_value,"theoretical_value":grandchild.theoretical_value}

                                    self.dict[aktivapassiva.name]["children"][child.name]["children"].update(dict_two)
                        #hier müssen noch mehr layer kommen
      def search_for_data(self):
            if self.text!="":
                  for item in self.fourth_layer:
                        item.update_recognized_values()
                        item.flag.recognized_values.append(item.values)
                        #item.int_data()
                        item.update_data()
                  for item in self.third_layer:
                        item.update_recognized_values()
                        item.flag.recognized_values.append(item.values)
                        #item.int_data()
                        item.update_data()  
                  for item in self.second_layer:
                        item.update_recognized_values()
                        item.flag.recognized_values.append(item.values)
                        #item.int_data()
                        item.update_data() 
                  for item in self.first_layer:
                        item.update_recognized_values()
                        item.flag.recognized_values.append(item.values)
                        #item.int_data()
                        item.update_data()               
      def check_flags(self):
            for item in self.all_items:
                  item.flag_entry()
                  if item.flag.status==True:
                        self.flag_dict[item.name]={}
                        if item.flag.recognized_value_missing==True:    
                              self.flag_dict[item.name].update({"recognized_value_missing":item.flag.recognized_value_missing})
                        if item.flag.logical_error==True:
                              self.flag_dict[item.name].update({"logical_error":item.flag.logical_error,"theoretical value":item.theoretical_value,"recognized value": item.recognized_value,"recognized_values":item.flag.recognized_values})




backup_item_capture="[\s,\w]*"                         
numbers_string="\s[\d,\.]+"
#für welche items brauchen wir doppelte entries mit oder verknupfung

#aktiva
aktiva_regex=re.compile("Aktiva"+numbers_string,flags=re.I)
anlagevermögen_regex=re.compile("Anlagevermögen"+numbers_string,flags=re.I) #oberkategorie von sachanlagen
sachanlagen_regex=re.compile("Sachanlagen"+numbers_string,flags=re.I)  
umlaufvermögen_regex=re.compile("umlaufvermögen"+numbers_string,flags=re.I)
immaterielle_vermögensgegenstände_regex=re.compile("immaterielle_vermögensgegenstände"+numbers_string,flags=re.I)
#umlaufvermögen children
vorräte_regex=re.compile("vorräte"+numbers_string,flags=re.I)
forderungen_regex_string="forderungen"+numbers_string+"|"+"Forderungen und sonstige Vermögensgegenstände"+numbers_string
forderungen_regex=re.compile(forderungen_regex_string,flags=re.I)
wertpapiere_regex=re.compile("wertpapiere"+numbers_string,flags=re.I)
kassenbestand_regex=re.compile("kassenbestand"+backup_item_capture+numbers_string,flags=re.I)
gewinnrücklage_regex=re.compile("gewinnrücklage"+numbers_string,flags=re.I)
kapitalrücklage_regex=re.compile("kapitalrücklage"+numbers_string,flags=re.I)
rechnungsabgrenzungsposten_regex=re.compile("Rechnungsabgrenzungsposten"+numbers_string,flags=re.I)
fehlbetrag_regex=re.compile("fehlbetrag"+numbers_string,flags=re.I)
#rechnungsabgrenzungspostren+anlagevermögen+umlaufvermögen=Aktiva

#passiva
passiva_regex=re.compile("Passiva"+numbers_string,flags=re.I)
eigenkapital_regex=re.compile("Eigenkapital"+numbers_string,flags=re.I)
#eigenkapital children
bilanzverlust_regex=re.compile("bilanzverlust"+numbers_string,flags=re.I)
eingefordertes_kapital_regex=re.compile("eingefordertes kapital"+numbers_string,flags=re.I)
gezeichnetes_kapital_regex=re.compile("gezeichnetes kapital"+numbers_string,flags=re.I) #teil von eingefordertem kapital
einlagen_regex=re.compile("einlagen"+numbers_string,flags=re.I)#teil von eingefordertem kapital
gewinnvortrag_regex=re.compile("Gewinnvortrag"+numbers_string,flags=re.I)
jahresüberschuss_regex=re.compile("Jahresüberschuss"+numbers_string,flags=re.I)
rückstellungen_regex=re.compile("Rückstellungen"+numbers_string,flags=re.I)
bilanzgewinn_regex=re.compile("bilanzgewinn"+numbers_string,flags=re.I)
immaterielle_vermögensgegestände_regex=re.compile("[I,i]materielle Vermögensgegenstände\s[\s\d,.]+")
finanzanlagen_regex=re.compile("finanzanlagen"+numbers_string,flags=re.I)
vermögensgegenstände_regex=re.compile("sonstige Vermögensgegenstände"+numbers_string,flags=re.I)
kreditinstitute_regex=re.compile("Kreditinstituten"+numbers_string,flags=re.I)
verbindlichkeiten_regex=re.compile("verbindlichkeiten"+numbers_string,flags=re.I)
jahresfehlbetrag_regex=re.compile("jahresfehlbetrag"+numbers_string,flags=re.I)
verlustvortrag_regex=re.compile("verlustvortrag"+numbers_string,flags=re.I)
überschuss_regex=re.compile("überschuss"+numbers_string,flags=re.I)
rechnungsbegrenzungsposten_regex=re.compile("rechnungsbegrenzungsposten"+numbers_string,flags=re.I)


bilanzsumme_regex=re.compile("bilanzsumme"+numbers_string,flags=re.I)

character_pattern=re.compile("[^\d,.\s]\w*")
annual_acount_regex_dict={"imaterielle Vermögensgegenstände":immaterielle_vermögensgegestände_regex,"sachanlagen":sachanlagen_regex,"finanzanlagen":finanzanlagen_regex,"vermögesgegenstände":vermögensgegenstände_regex,"kreditinstitute":kreditinstitute_regex,"aktiva":aktiva_regex,"eigenkapital":eigenkapital_regex,"gezeichnetes_kapital":gezeichnetes_kapital_regex,"gewinnvortrag":gewinnvortrag_regex,"jahresüberschuss":jahresüberschuss_regex,"rückstellungen":rückstellungen_regex,"verbindlichkeiten":verbindlichkeiten_regex,"rechnungsbegrenzungsposten":rechnungsbegrenzungsposten_regex,"passiva":passiva_regex} 
single_number_pattern=re.compile("\d+[,.]\d*[,.]*\d*[,.]*")
