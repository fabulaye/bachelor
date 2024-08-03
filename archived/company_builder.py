from bachelor.archived.project_builder import project_builder

class company():
    def __init__(self) -> None:
        self.name=None  
        self.rechtsform=None
        self.projects=[]
        self.country=None
    def __str__(self) -> str:
        return f"Name: {self.name}, Rechtsform: {self.rechtsform}, Projects: {print(self.projects)}"
    
class company_builder():
    def __init__(self) -> None:
        self.company=company()
    def build_name():
        pass
    def build_rechtsform():
        pass
    def build_projects():
        pass
    def get_company(self):
        return self.company 

from bachelor.archived.project_builder import subsidized_project_builder

class subsidized_company_builder(company_builder):
    def __init__(self) -> None:
        super().__init__()
        self.company=company()
    def build_name(self,name):
        self.company.name=None
    def build_projects(self,project_data):
        for index,project in enumerate(project_data):
            project_object=subsidized_project_builder()
            project_object.build_id(project_data["id"]).build_subsidy(project_data["subsidy_euro"]).build_duration(project_data["subsidy_start"],project_data["subsidy_end"]).get_project()
            self.company.projects.append(project_object)
            return self
        
test_data={"id":23,"subsidy_euro":124123,"subsidy_start":"24.03.2019","subsidy_end":"25.06.2024"}


subsidized_company_1=subsidized_company_builder().build_projects(test_data).get_company()
print(subsidized_company_1)

        

