import pandas as pd

ingredients_df = pd.read_csv('active_ingredients.csv')
valid_ingredients = ingredients_df['id'].unique()


interaction_files = ['cleaned_med_data.csv']
df_interactions = pd.concat([pd.read_csv(f) for f in interaction_files], ignore_index=True)


df_interactions = df_interactions[df_interactions['severity'].str.strip().str.lower() != 'unknown']


mask = df_interactions['medA'].isin(valid_ingredients) & df_interactions['medB'].isin(valid_ingredients)
df_filtered = df_interactions[mask].copy()

df_final = df_filtered.drop_duplicates(subset=['medA', 'medB', 'severity'])


df_final.to_csv('final_validated_interactions.csv', index=False)

print(f"Validation complete.")
print(f"Rows remaining after ingredient check and de-duplication: {len(df_final)}")