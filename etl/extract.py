from api import ergast_api

def extract_data():
    extract = ergast_api.ErgastAPI()
    extract.get_all_data("/mnt/d/Documents/Data Projects/formula_1_racing/data")