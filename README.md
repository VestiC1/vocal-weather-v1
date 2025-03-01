# vocal-weather-v1
Projet Vocal Weather - Prédiction météo via demande vocale

# creation environnement
```python
python -m venv venv
```

# activation desactivation venv
```bash
venv\Scripts\activate.bat 
venv\Scripts\deactivate.bat
```

# installation azure-cognitiveservices-speech (stt)
```python
pip install azure-cognitiveservices-speech
```

# lancer l'application speech_recognition
```python
python stt.py
```

# installation transformers - camemBERT (ner with dates)
```python
pip install transformers
```

# lancer l'application camemBERT
```python
python ner.py
```

# installation geopy
```python
pip install geopy
```

# lancer l'application geopy
```python
python geo.py
```

# installation open meteo
```python
pip install openmeteo-requests
pip install requests-cache retry-requests numpy pandas
```

# Reponse open meteo
code python via le site : https://open-meteo.com/en/docs

# installation fastapi
```python
pip install fastapi[all]
```

# lancer l'application geopy
```python
fastapi dev app.py
```
