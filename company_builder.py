from project_builder import project_builder
import pandas as pd

orbis_exact_search_incomplete=pd.read_csv(r"C:\Users\lukas\Desktop\bachelor\data\complete_search\orbis_exact_search_incomplete.csv")

class company():
    def __init__(self) -> None:
        self.name=None
        self.ids=None
        self.financials=None

class company_builder():
    def __init__(self) -> None:
        self.company=company()
    def build_ids(self,ids):
        self.ids=ids
        return self
    def build_name(self,name):
        self.name=name
        return self
    def build_financials(self,financial_df):
        self.financials=financial_df
        return self
    
class treated_company_builder(company_builder):
    def __init__(self,*args) -> None:
        super().__init__()
        self.projects=None
    def build_projects(self,projects):
        for project_name,project_data in projects.items():
            self.company.projects[project_name]=project_builder(project_data)
        return self
    def build_treatment(self):
        self.treatment_dummy=1
        return self
    
class company_database():
    def __init__(self) -> None:
        self._companies={}
    def list_companies(self):
        return [company.name for company in self._companies.values()]
    def search_by_atribute():
        None
    def to_csv(self):
        df=pd.DataFrame(self._companies)
    def __str__(self) -> str:
        return str(self.list_companies())
    def __getitem__(self,key):
        return self._companies[key]
    def __setitem__(self, key, value):
        self._companies[key] = value
    def __iter__(self):
        return iter(self._companies.items())


#own object to store companies?
def build_companies(orbis_exact_search_incomplete):
    company_db=company_database()
    for index,row in orbis_exact_search_incomplete.iterrows():
        company_object=treated_company_builder().build_ids(row["bvdid"]).build_name(row["name_native"]).build_treatment() #name_native only for this one
        company_db[company_object.name]=company_object
    return company_db

companies_db=build_companies(orbis_exact_search_incomplete)
print(companies_db)

#search by name and search by id
#