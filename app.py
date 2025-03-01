import os
from dotenv import load_dotenv
from fastapi import FastAPI, Form, Request # Importation des modules nécessaires de FastAPI
from fastapi.responses import HTMLResponse, JSONResponse # Importation de HTMLResponse pour indiquer que la réponse sera du HTML
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates # Importation de Jinja2Templates pour gérer les templates
from services.meteo import OpenMeteoService
from services.ner import NERService
from services.geo import GEOService
import re
load_dotenv()

SPEECH_KEY = os.getenv("SPEECH_KEY")
SPEECH_REGION = os.getenv("SPEECH_REGION")


opem_meteo = OpenMeteoService()
ner = NERService()
geo = GEOService()

app = FastAPI() # Création de l'instance FastAPI de l'application, `app` est le nom de l'instance FastAPI

app.mount("/static", StaticFiles(directory="./webapp/static"), name="static")

templates = Jinja2Templates(directory="./webapp/templates") # Initialisation de Jinja2Templates en spécifiant le dossier des templates

@app.get("/", response_class=HTMLResponse) # Définition de la route pour la page d'accueil (/), la réponse sera du HTML
async def read_root(request: Request): # Fonction asynchrone associée à la route /
    return templates.TemplateResponse("index.html", {"request": request, "speech_key": SPEECH_KEY, "speech_region": SPEECH_REGION})
# On charge le template index.html et on passe les variables (request et nom_app)


@app.post("/weather", response_class=JSONResponse)
async def get_weather(request: Request, voice_command: str = Form()):
    print(voice_command)
    entities = ner.extract_entities(voice_command)
    
    try :
      city = extract_city(entities)
      coord = get_coordinates(city = city)
    except ValueError as e:
        return JSONResponse(content={'error'  : str(e)})
    except AttributeError as e:
        return JSONResponse(content={'error'  : f'{city} : Ville inconnue.'})
    horizon = extract_horizon(entities)
  
    

    weather = get_openweather( lat=coord['lat'], lon=coord['lon'], horizon=horizon)
    weather['city'] = city
    return  JSONResponse(content=weather)


def extract_city(entities):
    for ent in entities:
        if ent[0] == 'LOC':
            return ent[1]
    raise ValueError("Veuillez préciser une localisation dans votre demande.")

def extract_horizon(entities):
    horizon = 1
    found_date = 0
    for ent in entities:
        if ent[0] == 'DATE':
            found_date = int(re.sub("[^0-9]", "", ent[1]))
            break  
    if  found_date > horizon :
        horizon = found_date
    return min(horizon, 16)

                


def get_coordinates(city):
    coord = geo.get_coordinates(city)
    return{"city":city, "lat":coord['lat'], "lon": coord["lon"]}

def get_openweather(lat, lon, horizon):
    return opem_meteo.get_forecast(lat=lat, lon=lon, horizon=horizon)
    