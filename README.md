# 📁 Entity Resolution

## 🎯 Obiectiv principal
Obiectivul principal a fost identificarea si gruparea companiilor duplicate, folosind un algoritm bazat pe similaritatea textuala si reguli euristice aplicate pe coloane esentiale precum nume, domeniu, email, telefon si adresa.

## 🧠 Gandirea din spatele solutiei

### 1. Explorare initiala
Primul pas a fost sa inteleg structura datelor, asa ca am creat scriptul `file_reader.py` pentru a vedea mai usor coloane si informatii despre acestea, iar apoi am creat scriptul `data_completeness.py`, care afiseaza gradul de completitudine al fiecarei coloane. Acest pas m-a ajutat sa decid ce coloane sunt utile pentru procesul de deduplicare.

### 2. Experimentare pe subset
Am creat apoi un fisier mic — `mini_example.py` — pentru a testa o logica simplificata pe un subset de date. A fost ideal pentru a intelege comportamentul functiei de similaritate si cum sa structurez logica de grupare.

### 3. Prelucrarea si deduplicarea

Fisierul principal, `matcher.py`, contine implementarea finala:

- Am selectat doar coloanele cu o valoare informativa si un grad decent de completitudine.
- Am aplicat preprocesare (normalizare text, eliminare caractere inutile etc.).
- Am definit o functie de `similarity_score` care combina scoruri fuzzy (folosind `rapidfuzz`) cu egalitati exacte.
- Gruparea entitatilor se face pe baza domeniului web si a scorului total, intr-o maniera eficienta.

## 📊 Rezultate

- Datele au fost grupate in functie de `website_domain` si apoi comparate pereche cu pereche folosind un scor euristic.
- S-a obtinut un fisier CSV cu ID-ul grupului si datele companiei pentru entitatile considerate duplicate.
- Codul este usor de extins pentru scoruri personalizate sau alte metode de comparare.

## 🧪 Cum rulez?

Asigura-te ca ai instalat dependintele intr-un mediu virtual:
pip install pandas pyarrow rapidfuzz

Apoi ruleaza scriptul principal:
python src/matcher.py

