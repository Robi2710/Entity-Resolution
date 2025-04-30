from rapidfuzz import fuzz
import pandas as pd
import re

# Funcția de preprocesare
def preprocess_text(text):
    if pd.isna(text):
        return ""
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)  # elimină spații multiple
    text = re.sub(r'[^a-z0-9@.\-/ ]', '', text)  # păstrează doar caractere utile
    return text.strip()

def preprocess_dataframe(df):
    # Coloane relevante pentru deduplicare
    relevant_cols = [
        'company_name',
        'company_commercial_names',
        'website_domain',
        'primary_email',
        'primary_phone',
        'main_address_raw_text'
    ]
    df = df[relevant_cols].fillna('')

    # Aplicăm preprocesarea
    df['company_name'] = df['company_name'].apply(preprocess_text)
    df['company_commercial_names'] = df['company_commercial_names'].apply(
        lambda x: [preprocess_text(name) for name in x] if isinstance(x, list) else [])
    df['website_domain'] = df['website_domain'].apply(preprocess_text)
    df['primary_email'] = df['primary_email'].apply(preprocess_text)
    df['primary_phone'] = df['primary_phone'].apply(preprocess_text)
    df['main_address_raw_text'] = df['main_address_raw_text'].apply(preprocess_text)

    return df

# Citim datele
df = pd.read_parquet('../veridion_entity_resolution_challenge.snappy.parquet', engine='pyarrow')

# Aplicăm preprocesarea
df = preprocess_dataframe(df)

visited = set()
groups = []
threshold = 60  # prag de similaritate

# Funcția de scor între două rânduri
def similarity_score(row1, row2):
    score = 0

    # Comparare website_domain
    if row1['website_domain'] and row2['website_domain'] == row1['website_domain']:
        score += 50

    # Comparare nume companie
    name_score = fuzz.token_set_ratio(row1['company_name'], row2['company_name'])
    if name_score > 90:
        score += 30
    elif name_score > 80:
        score += 15

    # Comparare email
    if row1['primary_email'] and row2['primary_email'] == row1['primary_email']:
        score += 10

    # Comparare telefon
    if row1['primary_phone'] and row2['primary_phone'] == row1['primary_phone']:
        score += 5

    # Comparare adresă
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
