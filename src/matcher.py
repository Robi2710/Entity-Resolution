import pandas as pd
from fuzzywuzzy import fuzz
from collections import defaultdict
from preprocess import preprocess_dataframe  # <- Funcția ta de preprocess

# Încarcă și preprocesează datele
df = pd.read_parquet('../veridion_entity_resolution_challenge.snappy.parquet', engine='pyarrow')
df = preprocess_dataframe(df)

visited = set()
groups = []
threshold = 60  # prag de similaritate

# Funcție de scor între două rânduri
def similarity_score(row1, row2):
    score = 0

    # Domenii comune
    if set(row1['all_domains_combined']) & set(row2['all_domains_combined']):
        score += 50

    # Similaritate pe nume
    max_name_score = max(
        (fuzz.token_set_ratio(n1, n2) for n1 in row1['all_names'] for n2 in row2['all_names']),
        default=0
    )
    if max_name_score > 90:
        score += 30
    elif max_name_score > 80:
        score += 15

    # Email exact
    if row1['primary_email'] and row1['primary_email'] == row2['primary_email']:
        score += 10

    # Telefon exact
    if row1['primary_phone'] and row1['primary_phone'] == row2['primary_phone']:
        score += 5

    # Adresă similară
    addr_score = fuzz.token_set_ratio(row1['main_address_raw_text'], row2['main_address_raw_text'])
    if addr_score > 85:
        score += 5
    elif addr_score > 70:
        score += 2

    return score

# Blocking simplu pe prima literă din website_domain
buckets = defaultdict(list)
for idx, row in df.iterrows():
    key = row['website_domain'][:1] if row['website_domain'] else ''
    buckets[key].append(idx)

# Grupare
for bucket in buckets.values():
    for i in range(len(bucket)):
        idx_i = bucket[i]
        if idx_i in visited:
            continue
        group = [idx_i]
        for j in range(i + 1, len(bucket)):
            idx_j = bucket[j]
            if idx_j in visited:
                continue
            score = similarity_score(df.loc[idx_i], df.loc[idx_j])
            if score >= threshold:
                group.append(idx_j)
                visited.add(idx_j)
        groups.append(group)

# Output final
results = []
for group_id, group in enumerate(groups):
    for idx in group:
        results.append({
            'group_id': group_id,
            'company_name': df.loc[idx, 'company_name'],
            'website_domain': df.loc[idx, 'website_domain'],
            'email': df.loc[idx, 'primary_email']
        })

output_df = pd.DataFrame(results)
output_df.to_csv('deduplicated_groups.csv', index=False)
print("✅ Salvat în deduplicated_groups.csv")