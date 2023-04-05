from geopy.distance import geodesic
import pandas as pd

def get_radial_distance(user1_cordinates: tuple, user2_coordinates:tuple) -> str:
    '''Calculate the distance between two coordinates'''
    distance = geodesic(user1_cordinates, user2_coordinates).km
    return distance


def closest_places_ids(data: pd.DataFrame, user_lat, user_long, threshold: int=2) -> tuple:
    distances_nearby = {}
    for row in data.itertuples():
        distance = get_radial_distance(
                                         (user_lat, user_long), 
                                        (getattr(row,'latitude'), getattr(row, 'longitude')
                                        )
                                       )
        distances_nearby[getattr(row, 'id')] = int(distance)
    sorted_dict = dict(sorted(distances_nearby.items(), key=lambda x:x[1])[:threshold])
    return list(sorted_dict.keys())


lat_long = {'id': {0: 1, 1: 3}, 
            'street': {0: 'Sector-25', 1: 'Jain Market'},
              'city': {0: 'Faridabad', 1: 'Meerut'}, 
              'state': {0: 'Haryana', 1: 'Uttarpradesh'}, 
              'country': {0: 'India', 1: 'India'}, 
              'zip': {0: '121004', 1: '112233'}, 
              'latitude': {0: 28.3352279, 1: 28.984644},
                'longitude': {0: 77.3079144, 1: 77.705956}}
user_lat = 28.335228
user_long  = 77.307914
df = pd.DataFrame(lat_long)
print(closest_places_ids(df, user_lat, user_long))