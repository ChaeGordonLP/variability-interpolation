# Simulation of loss on half-an-hour data

import pandas as pd

file_name = "Export Vestas 2015-2019 1700051751614_2015-01-01_2019-11-13_V2019-11-13_AE.xlsx"
sheet_names = [
    "2019 Halfhourly",
    "2018 Halfhourly",
    "2017 Halfhourly",
    "2016 Halfhourly",
    "2015 Halfhourly",
]

def get_dfs(file_name=file_name, sheet_names=sheet_names):
    return pd.read_excel(file_name, sheet_name=sheet_names)
