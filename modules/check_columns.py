import pandas as pd

df_main = pd.read_csv('../data/UNSW_NB15_training-set.csv', low_memory=False)
df_gt = pd.read_csv('../data/UNSW_NB15_testing-set.csv', low_memory=False)

print("Training Set:", df_main.columns.tolist())
print("Testing Set:", df_gt.columns.tolist())
