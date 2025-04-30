import pandas as pd
import re

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
        'company_legal_names',
        'company_commercial_names',
        'website_domain',
        'all_domains',
        'primary_email',
        'emails',
        'primary_phone',
        'phone_numbers',
        'main_address_raw_text'
    ]
    df = df[relevant_cols].copy()

    # Aplicăm preprocesarea
    df['company_name'] = df['company_name'].apply(preprocess_text)
    df['company_legal_names'] = df['company_legal_names'].apply(
        lambda x: [preprocess_text(name) for name in x] if isinstance(x, list) else [])
    df['company_commercial_names'] = df['company_commercial_names'].apply(
        lambda x: [preprocess_text(name) for name in x] if isinstance(x, list) else [])

    df['website_domain'] = df['website_domain'].apply(preprocess_text)
    df['all_domains'] = df['all_domains'].apply(
        lambda x: [preprocess_text(domain) for domain in x] if isinstance(x, list) else [])

    df['primary_email'] = df['primary_email'].apply(preprocess_text)
    df['emails'] = df['emails'].apply(
        lambda x: [preprocess_text(email) for email in x] if isinstance(x, list) else [])

    df['primary_phone'] = df['primary_phone'].apply(preprocess_text)
    df['phone_numbers'] = df['phone_numbers'].apply(
        lambda x: [preprocess_text(phone) for phone in x] if isinstance(x, list) else [])

    df['main_address_raw_text'] = df['main_address_raw_text'].apply(preprocess_text)

    # Combinații utile
    df['all_names'] = df.apply(
        lambda row:
            ([row['company_name']] if row['company_name'] else []) +
            row['company_legal_names'] +
            row['company_commercial_names'],
        axis=1
    )
    df['all_domains_combined'] = df.apply(
        lambda row:
            ([row['website_domain']] if row['website_domain'] else []) +
            row['all_domains'],
        axis=1
    )

    # Eliminăm golurile
    df['all_names'] = df['all_names'].apply(lambda x: [item for item in x if item])
    df['all_domains_combined'] = df['all_domains_combined'].apply(lambda x: [item for item in x if item])

    return df

