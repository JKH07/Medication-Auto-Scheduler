import pandas as pd
import glob

all_files = glob.glob("merged_final.csv")
temp_list = []

for f in all_files:
    df = pd.read_csv(f)
   
    temp_list.append(df[['id', 'name']])

# Merge and remove duplicates
medications_df = pd.concat(temp_list).drop_duplicates(subset=['id'])
medications_df.to_csv("merged2.csv", index=False)