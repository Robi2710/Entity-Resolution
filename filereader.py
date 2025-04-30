import pandas as pd

# Calea către fișierul descărcat (schimbă cu unde l-ai salvat tu)
file_path = 'veridion_entity_resolution_challenge.snappy.parquet'

# Citește fișierul Parquet
df = pd.read_parquet(file_path)

# Sau vezi toate coloanele disponibile
print(df.columns)