from api import ergast_api
from aws_classes import loader
import loggers
import logging

logger = logging.getLogger(__name__)

logger.info("starting test run log")

# extract = ergast_api.ErgastAPI()
# extract.get_all_data("/mnt/d/Documents/Data Projects/formula_1_racing/data")

# load = loader.Loader()
# load.load_csv_objects(dir_path="./data/", files=["circuits.csv"], bucket="kc-test-f1-bucket")


# kc-f1-racing-landing
list_csv_objs = []
import os
for file in os.listdir("/mnt/d/Documents/Data Projects/formula_1_racing/data"):
    if file.endswith('.csv'):
        list_csv_objs.append(file)
print(list_csv_objs)