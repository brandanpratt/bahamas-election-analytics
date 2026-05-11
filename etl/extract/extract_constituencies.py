import pandas as pd

def extract_constituencies():

    df = pd.read_csv("data/constituencies_extracted.csv")

    return df