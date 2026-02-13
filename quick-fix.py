import pandas as pd

pd.read_csv("data.csv").T.to_csv("data_transposed.csv")