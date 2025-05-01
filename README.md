# 📁 Entity Resolution
## 🎯 Obiectiv principal
Obiectivul principal a fost identificarea și gruparea companiilor duplicate, folosind un algoritm bazat pe similaritatea textuală și reguli euristice aplicate pe coloane esențiale precum nume, domeniu, email, telefon și adresă.

## 🧠 Gândirea din spatele soluției
### 1. Explorare initiala
Primul pas a fost să înțeleg structura datelor, așa că am creat scriptul file_reader.py pentru a vedea mai usor coloane si informatii desprea acestea, iar apoi am creat scriptul data_completeness.py, care afișează gradul de completitudine al fiecărei coloane. Acest pas m-a ajutat să decid ce coloane sunt utile pentru procesul de deduplicare.
### 2. Experimentare pe subset
Am creat apoi un fișier mic — mini_example.py — pentru a testa o logică simplificată pe un subset de date. A fost ideal pentru a înțelege comportamentul funcției de similaritate și cum să structurez logica de grupare.
### 3. Prelucrarea și deduplicarea

Fișierul principal, matcher.py, conține implementarea finală:

- Am selectat doar coloanele cu o valoare informativă și un grad decent de completitudine.

- Am aplicat preprocesare (normalizare text, eliminare caractere inutile etc.).

- Am definit o funcție de similarity_score care combină scoruri fuzzy (folosind rapidfuzz) cu egalități exacte.

- Gruparea entităților se face pe baza domeniului web și a scorului total, într-o manieră eficientă.

## 📊 Rezultate

- Datele au fost grupate în funcție de website_domain și apoi comparate pereche cu pereche folosind un scor euristic.

- S-a obținut un fișier CSV cu ID-ul grupului și datele companiei pentru entitățile considerate duplicate.

- Codul este ușor de extins pentru scoruri personalizate sau alte metode de comparare.

## 🧪 Cum rulez?

Asigură-te că ai instalat dependințele într-un mediu virtual:

__pip install pandas pyarrow rapidfuzz__

Apoi rulează scriptul principal:

__python src/matcher.py__



