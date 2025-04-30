# exemplu doar pentru primele 10 randuri
# pentru o intelegere mai usoara a algoritmului

import pandas as pd # pentru manipularea datelor in tabele
from fuzzywuzzy import fuzz # compara texte si spune cat de asemanatoare sunt

df = pd.read_parquet('veridion_entity_resolution_challenge.snappy.parquet', engine='pyarrow') #dataframe

sample_df = df[['company_name', 'website_domain']].head(10).reset_index(drop=True) # extrag doar colonaele company_name
                                                                                   # si website_domain, se pastreaza primele 10 randuri

duplicate_groups = []
visited = set()

for i in range(len(sample_df)):
    if i in visited:
        continue
    group = [i]
    name_i = str(sample_df.loc[i, 'company_name']).lower()
    domain_i = str(sample_df.loc[i, 'website_domain']).lower()

    for j in range(i+1, len(sample_df)):
        name_j = str(sample_df.loc[j, 'company_name']).lower()
        domain_j = str(sample_df.loc[j, 'website_domain']).lower()

        if pd.isna(sample_df.loc[i, 'company_name']) or pd.isna(sample_df.loc[j, 'company_name']): # evita situatiile sa dea ca au acelasi nume la null
            continue


        if pd.isna(sample_df.loc[i, 'website_domain']) or pd.isna(sample_df.loc[j, 'website_domain']):
            continue

        name_similarity = fuzz.token_set_ratio(name_i, name_j) #compara 2 texte si intoarce
                                                               # un scor de asemanare intre 0 si 100
        domain_similarity = fuzz.token_set_ratio(domain_i, domain_j)
        if name_similarity >= 90 or domain_similarity >= 90:
            group.append(j)
            visited.add(j)

    duplicate_groups.append(group)

for group in duplicate_groups:
    print(sample_df.loc[group, :])
    print('-' * 50)




