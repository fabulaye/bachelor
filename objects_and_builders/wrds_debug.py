
from datahandling.change_directory import chdir_id
import importlib.util
import sys
import os
import pandas as pd
def import_module_from_path(module_name, file_path):
    # Ensure the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    # Create a module spec from the file location
    spec = importlib.util.spec_from_file_location(module_name, file_path)

    if spec is None:
        raise ImportError(f"Cannot create a module spec for {module_name} from {file_path}")

    # Create a module object from the spec
    module = importlib.util.module_from_spec(spec)

    # Add the module to sys.modules
    sys.modules[module_name] = module

    # Execute the module
    spec.loader.exec_module(module)

    return module

#import pandas as pd
#wrds_connection=import_module_from_path("wrds_connection",r"C:\Users\lukas\Documents\GitHub\bachelor\sql_requests\wrds_connection.py")
#
#
#conenction=wrds_connection.start_connection()
#
#request=conenction.raw_sql(f"SELECT bvdid FROM bvd_orbis_medium.ob_cflow_non_us_ind_eur_m")
#request_df=pd.DataFrame(request)
#chdir_id()
#request_df.to_csv("bvdid_medium.csv")

from processing.my_list import list_intersection

chdir_id()

bvd_medium_ids=pd.read_csv("bvdid_medium.csv")["bvdid"]
all_ids=pd.read_csv("all_treatment_ids.csv")["bvdid"]

intersection=list_intersection([bvd_medium_ids.to_list(),all_ids.to_list()])
print(intersection)

def find_de():
    german=[]
    for id in bvd_medium_ids:
        if id.startswith("DE"):
            german.append(id)
    return german

german=find_de()
print(german)