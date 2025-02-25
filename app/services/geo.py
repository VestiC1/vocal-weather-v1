from geopy.geocoders import Nominatim
 
# Création d'un objet géocodeur Nominatim
geolocator = Nominatim(user_agent="my_geocoder")
 
# Géocodage d'une adresse
location = geolocator.geocode("Tours")
 
# Affichage des informations de localisation
print("Adresse:", location.address,"Latitude:", location.latitude, "Longitude:", location.longitude)

# Pour plusieurs resultat utiliser la boucle suivante avec : (locations = geolocator.geocode("Tours", exactly_one=False))
#for location in locations:
#   print("Adresse:", location.address,"Latitude:", location.latitude, "Longitude:", location.longitude)