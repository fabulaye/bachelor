

class query():
    def __init__(self) -> None:
        self.how=None
        self.country=None
        self.query_string=None
        self.name_identifier=None
        self.country_identifier=None
        self.id_name=None
    def build_general_query_string(self,path,name,search_params:dict):
        self.how=search_params["how"]
        if "country" in search_params.keys():
            self.country=search_params["country"].upper()
        if self.how=="exact":
            self.query_string=f""" f"SELECT * FROM {path} WHERE Upper({self.name_identifier}) = '{name}' """
        elif self.how=="like":
            self.query_string=f""" f"SELECT * FROM {path} WHERE Upper({self.name_identifier}) LIKE '%%{name}%%' """
        if self.country!=None:
            self.query_string=self.query_string+f"""AND {self.country_identifier} = '{self.country}'"""
        return self.query_string
    def build_id_query_string(self,path,ids):
        self.query_string=f"SELECT * FROM {path} WHERE {self.id_name} IN {ids}"
        #self.query_string=f"SELECT * FROM {path} WHERE id IN ({','.join('?' * len(ids))}"
        #self.query_string=f"SELECT * FROM {path} WHERE {self.id_name} = ANY(%s)"
        print(self.query_string)
        #self.query_string=f"SELECT * FROM {path} LIMIT 100"
        return self.query_string

#vielleicht eine build_query_string function oder sowas

class query_builder():
    def __init__(self) -> None:
        self.query=query()
    def build_amadeus(self):    
        self.query.name_identifier="name_nat"
        self.query.country_identifier="cntrycde"
        self.query.id_name="idnr"
        return self.query
    def build_orbis(self):
        self.query.name_identifier="name_native"
        self.query.country_identifier="ctryiso"   
        self.query.id_name="bvdid"
        return self.query






