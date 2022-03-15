import pandas as pd

"""
    function to load domain names from a csv file
    return: the list of domain names
"""
def get_list_of_domains():
    data = pd.read_csv("top500Domains.csv")
    return data['Root Domain'].to_numpy()