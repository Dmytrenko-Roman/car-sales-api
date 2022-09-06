import pandas as pd


def parse_data(file: object):
    df = pd.read_excel(file)
    df.fillna("", inplace=True)
    return df.to_dict(orient="records")
