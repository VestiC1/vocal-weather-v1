from geopy.geocoders import Nominatim


class GEOService:
    """ GEO coding service"""
# Création d'un objet géocodeur Nominatim
    def __init__(self):
        
        self.geolocator = Nominatim(user_agent="my_geocoder")
    
    def get_coordinates(self, loc):

        location = self.geolocator.geocode(loc.title())

        return {'lat' : location.latitude, 'lon' : location.longitude}

if __name__ == '__main__':
    geo = GEOService()
    print(geo.get_coordinates('Tours'))