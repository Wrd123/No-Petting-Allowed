import pandas as pd

df_main = pd.read_csv('../data/UNSW-NB15_1.csv', low_memory=False)
df_gt = pd.read_csv('../data/NUSW-NB15_GT.csv', low_memory=False)

print("Main dataset columns:", df_main.columns.tolist())
print("Ground truth columns:", df_gt.columns.tolist())
