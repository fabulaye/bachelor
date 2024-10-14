import contextlib

class balance_sheet():
    def __init__(self,observation):
        
        self.closdate_year=observation["closdate_year"]
        self.actuals=actual_items(observation)
        self.theoreticals=theoretical_items(observation)
        self.debt_to_equity_ratio=None
        self.current_ratio=None
            #what do I do with other shareholder funds? return on shfd
            #total liabilities var?
   
    #    self.equity_increase_diff=#value from year -1 - self.equity_increase_theoretical
    def compare_actual_and_theoretical(self):
        absolute_difference_list=[]
        actual_values_list=[]
        theoretical_values_list=[]
        relative_difference_list=[]
        index_list=[]
        for key,value in self.actuals.items():
            try:
                actual_value=self.actuals[key]
                actual_values_list.append(actual_value)
                theoretical_value=self.theoreticals[key]
                theoretical_values_list.append(theoretical_value)
                absolute_difference=actual_value-theoretical_value
                absolute_difference_list.append(absolute_difference)
                if self.actuals[key]==0:
                    relative_difference=0
                else:
                    relative_difference=absolute_difference/self.actuals[key]
                relative_difference_list.append(relative_difference)
                index_list.append(key)  
            except KeyError:
                print(f"{key} not in keys")    
        df_data={"actual_value":actual_values_list,"theoretical_value":theoretical_values_list,"absolute_difference":absolute_difference_list,"relative_difference":relative_difference_list,"variable":index_list}
        df=pd.DataFrame(df_data)
        #df.set_index(index_list,inplace=True)
        return df
    
class items():
    def __init__(self):
        pass
    def create_dict(self):
        dictionary={}
        dictionary = {attr: value for attr, value in vars(self).items() if not callable(value)}
        #for attribute in dir(self):
        #    if not attribute.startswith("__"):
        #        dictionary[attribute]=getattr(self, attribute)
                
        self.dictionary=dictionary
        return dictionary
    def items(self):
        return self.dictionary.items()
    def __getitem__(self, key):
        return self.dictionary[key]

class actual_items(items):
    def __init__(self,observation):
        super().__init__()
        #with my_context_manager():
        self.toas=observation["toas"]
        self.toas_2=observation["toas"]
        self.cuas=observation["cuas"]
        self.fias=observation["fias"]
        self.culi=observation["culi"]
        self.ncli=observation["ncli"]
        #self.debt=observation["debt"]
        #self.liab=observation[""] #total liabilities
        #self.shfd=observation["shfd"]
        #self.tshf=observation["tshf"] #shareholder funds + liabilties
        #self.tshfd=observation["tshf"]
        self.fias=observation["fias"]
        self.balance_sheet_equation=0
        #self.residual_equity=self.toas-self.tshf #equity ist nicht nur tshfd
        #self.cf=observation["cf"]
        #self.ooas=observation["ooas"]
        #self.ooli=observation["ooli"]
        #self.ltdb=observation["ltdb"] #longterm debt --> theoretical liabilities with long and shortterm liab, maybe use as proxy in case var is not available. Maybe create a proxy function with hierachies: If ncas na use ltdb etc. 
        #self.equity_increase=observation["equity_increase"]
        self.create_dict()
   
class theoretical_items(items):
     def __init__(self,observation):
        super().__init__()
        #with my_context_manager():
        self.toas=observation["cuas"]+observation["ncas"]
        self.cuas=observation["cash"]+observation["ocas"]#+observation["onci"]#+observation["oitl"]
        self.fias=observation["ifas"]+observation["tfas"]+observation["ofas"]
        self.toas_2=self.cuas+self.fias #besser machen
        self.liabilities=observation["culi"]+observation["ncli"]#+observation["oolb"]
        #self.culi=observation["oapb"]+observation["ocli"]+observation["loans"]+observation["cred"] #könnte problem geben wenn orbis loans filled und nicht 
        self.ncli=observation["ltdb"]+observation["oncl"]
        self.culi=observation["loans"]#+was fehlt hier?
        self.liabilities_2=self.culi+self.ncli
        self.ooas=observation["ocas"] + observation["ofas"] #name
        self.oolb=observation["ocli"] + observation["oncl"]
        self.equity_increase=observation["cf"]
        self.debt=observation["loans"]+observation["ltdb"]
        self.balance_sheet_equation=observation["toas"]-observation["tshf"]
        self.create_dict()




import pandas as pd
def balance_sheet_debug():
    data=pd.read_excel(r"C:\Users\lukas\Desktop\bachelor\data\financials_merge_treatment_and_control_categorials.xlsx")
    for index,row in data.iterrows():
        balance_sheet_bachelor=balance_sheet(row)
        diffs=balance_sheet_bachelor.compare_actual_and_theoretical()
        print(diffs)

balance_sheet_debug()