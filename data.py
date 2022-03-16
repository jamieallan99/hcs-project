import pandas as pd
import os

"""
    function to load domain names from a csv file
    return: the list of domain names
"""
def get_list_of_domains():
    csv = os.getenv("CSV")
    data = pd.read_csv(csv)
    return data['Root Domain'].to_numpy()
