import pandas as pd

# load data from csv file
def get_list_of_domains():
    data = pd.read_csv("top500Domains.csv")
    return data['Root Domain'].to_numpy()