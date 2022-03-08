import pandas as pd
import os

# load data from csv file
def get_list_of_domains():
    csv = os.getenv("CSV")
    data = pd.read_csv(csv)
    return data['Root Domain'].to_numpy()
