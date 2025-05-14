import yaml
import pandas as pd
import json

def read_yml(path):
    with open(path, "r") as config:
        data = yaml.load(config, Loader=yaml.FullLoader)
    return data

def read_csv_dicts(path):
    for record in pd.read_csv(path).to_dict(orient="records"):
        yield record