class wrds_table():
    def __init__(self) -> None:
        self.database_prefix=None
        self.name=None
        self.size_long=None
        self.path=None
        self.size_dict={"small":"s","medium":"m","large":"l","verylarge":"v"}
        self.size_short=None
    def set_size_and_name(self,size_long,name):
        self.size_long=size_long
        self.size_short=self.size_dict[size_long]
        self.name=name
    def build_path(self):
        self.path=f"{self.database_prefix}_{self.size_long}.{self.name}_{self.size_short}"
        return self.path

class amadeus_table(wrds_table):
    def __init__(self) -> None:
        super().__init__()
        self.database_prefix="bvd_ama"

class orbis_table(wrds_table):
    def __init__(self) -> None:
        super().__init__()
        self.database_prefix="bvd_orbis"

class table_builder():
    def __init__(self) -> None:
        self.name=None
        self.size=None
    def build_amadeus(self):
        return amadeus_table()
    def build_orbis(self):
        return orbis_table()

