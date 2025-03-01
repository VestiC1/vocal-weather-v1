## vocal-weather-v1
Projet Vocal Weather - Prédiction météo par commande vocale
L'application permet d'obtenir des prévisions météo en effectuant une demande vocale. L'utilisateur doit préciser au minimum le nom de la ville et le nombre de jours souhaité pour la prédiction.


## Installation

# creation environnement
```python
python -m venv venv
```

# activation desactivation venv
```bash
venv\Scripts\activate.bat 
venv\Scripts\deactivate.bat
```

# Installation librairies
```python
pip install -r requirements.txt
```


## Test des différent Services :

# Azure STT
```python
python services/stt.py
```

# camemBert-NER
```python
python services/ner.py
```

# Geocoding
```python
python services/geo.py
```

# Open Meteo
```python
python services/meteo.py
```


## Lancement de l'application
```python
fastapi dev app.py
```