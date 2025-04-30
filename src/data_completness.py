import pandas as pd

df = pd.read_parquet('../veridion_entity_resolution_challenge.snappy.parquet', engine='pyarrow')

# calculeaza completitudinea fiecărei coloane
completeness = (df.notnull().sum() / len(df) * 100).sort_values(ascending=False)

completitudine = df.notna().mean() * 100
with open("../completness.txt", "w") as f:
    f.write("Completitudinea coloanelor (%):\n")
    f.write(completitudine.sort_values(ascending=False).to_string())
