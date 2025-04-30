from rapidfuzz import fuzz
import pandas as pd

# Citim datele
df = pd.read_parquet('../veridion_entity_resolution_challenge.snappy.parquet', engine='pyarrow')

# Coloane utile și cu completitudine rezonabilă
cols = [
    'company_name',
    'company_commercial_names',
    'website_domain',
    'primary_email',
    'primary_phone',
    'main_address_raw_text'
]

df = df[cols].fillna('')
df = df.astype(str).apply(lambda x: x.str.lower())

visited = set()
groups = []
threshold = 60  # prag de similaritate

def similarity_score(row1, row2):
    score = 0

    if row1['website_domain'] and row2['website_domain'] == row1['website_domain']:
        score += 50

    name_score = fuzz.token_set_ratio(row1['company_name'], row2['company_name'])
    if name_score > 90:
        score += 30
    elif name_score > 80:
        score += 15

    if row1['primary_email'] and row2['primary_email'] == row1['primary_email']:
        score += 10

    if row1['primary_phone'] and row2['primary_phone'] == row1['primary_phone']:
        score += 5

    addr_score = fuzz.token_set_ratio(row1['main_address_raw_text'], row2['main_address_raw_text'])
    if addr_score > 85:
        score += 5
    elif addr_score > 70:
        score += 2

    return score

# Grupăm după website_domain
for _, group_df in df.groupby('website_domain'):
    indices = group_df.index.tolist()
    for i in range(len(indices)):
        idx_i = indices[i]
        if idx_i in visited:
            continue
        group = [idx_i]
        for j in range(i + 1, len(indices)):
            idx_j = indices[j]
            if idx_j in visited:
                continue
            score = similarity_score(df.loc[idx_i], df.loc[idx_j])
            if score >= threshold:
                group.append(idx_j)
                visited.add(idx_j)
        groups.append(group)

# Construim rezultatul
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