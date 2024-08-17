
class project():
    def __init__(self) -> None:
        self.id=None
        self.name=None
        self.release_date=None
        self.released=None
        self.subsidy=None
        self.subsidy_start=None
        self.subsidy_end=None
    def __str__(self) -> str:
        return f"ID: {self.id},Name: {self.name}, Release_date: {self.release_date}"


class project_builder():
    def __init__(self) -> None:
        self.project=project()
    def build_id(self,id):
        self.project.id=id
        return self #ist das hier richtig oder ist der return self.project?
    def build_name(self):
        pass
        return self
    def build_release_date(self):
        pass
        return self
    def build_subsidy(self,subsidy):
        pass
        return self
    def build_subsidized(self):
        pass
        return self
    def get_project(self):
        return self.project
    
class subsidized_project_builder(project_builder):
    def __init__(self) -> None:
        super().__init__()
        self.project=project()
    def build_subsidy(self,subsidy):
        self.project.subsidy=subsidy
        self.project.subsidized=True
        return self
    def build_duration(self,subsidy_start,subsidy_end):
        self.project.subsidy_start=subsidy_start
        self.project.subsidy_end=subsidy_end
        return self  
    
    
class not_subsidized_project_builder(project_builder):
    def __init__(self) -> None:
        super().__init__()
        self.project=project()
    def build_subsidy(self):
        self.project.subsidized=False
        return self

#sub_builder=subsidized_builder

#project_1=sub_builder.build_duration()




    


