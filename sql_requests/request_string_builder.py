class request_string():
    def __init__(self) -> None:
        self.how=None
        self.country=None
        self.request_string=None
    def build_request_string(self,database,name,search_params:dict):
        self.how=search_params["how"]
        if "country" in search_params.keys():
            self.country=search_params["country"]
        if self.how=="exact":
            self.request_string=f""" SELECT * FROM {database} WHERE Upper({self.name_identifier}) = '{name}' """
        elif self.how=="like":
            self.request_string=f""" SELECT * FROM {database} WHERE Upper({self.name_identifier}) LIKE '%%{name}%%' """
        if self.country!=None:
            self.request_string=self.request_string+f"""AND cntrycde='{self.country}'"""
        return self
    
class amadeus_request_string(request_string):
    def __init__(self) -> None:
        super().__init__()
        self.name_identifier="name_nat"
        self.country_identifier="cntrycde"

class orbis_request_string(request_string):
    def __init__(self) -> None:
        super().__init__()
        self.name_identifier="name_native"
        self.country_identifier="ctryiso"    
    
    

