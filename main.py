import argparse
import folium
from geopy.geocoders import Nominatim
from haversine import haversine

parser = argparse.ArgumentParser()
parser.add_argument("year", type=str, help="year of films")
parser.add_argument("latitude", type=str, help="latitude")
parser.add_argument('longitude', help="longitude")
args = parser.parse_args()


def coordinates_calculator(coord_1_0, coord_1_1, coord_2_0, coord_2_1):
    """
    returns distance between two coordinates
    >>> coordinates_calculator(45.7597, 4.8422, 48.8567, 2.3508)
    392.2172595594006
    """
    first_place = (coord_1_0, coord_1_1)
    second_place = (coord_2_0, coord_2_1)
    distance = haversine(first_place, second_place)
    return distance


def map_write(latitude_0, longitude_0, all_info):
    """
    :param latitude_0: latitude coordinate of start position on map
    :param longitude_0: longitude coordinate of start position on map
    :param all_info: tuple with all info:
    (latitude, longitude, info about film, distance to start coordinates)
    """
    cur_map = folium.Map(location=(latitude_0, longitude_0), zoom_start=5)
    fg = folium.FeatureGroup(name='Closest 10')
    fg0 = folium.FeatureGroup(name='Your coordinates')
    fg1 = folium.FeatureGroup(name='Closest 10-20')
    fg2 = folium.FeatureGroup(name='Closest 20-30')
    fg3 = folium.FeatureGroup(name='Closest 30 - ...')

    fg0.add_child(folium.Marker(location=(latitude_0, longitude_0), popup='Your location',
                                icon=folium.Icon(color='orange', icon='anchor')))
    if len(all_info) > 10:
        for i in range(10):
            fg.add_child(folium.Marker(location=(all_info[i][0], all_info[i][1]), popup=all_info[i][2],
                                       icon=folium.Icon(color='red', icon='off')))
    if len(all_info) > 20:
        for i in range(10, 20):
            fg1.add_child(folium.Marker(location=(all_info[i][0], all_info[i][1]), popup=all_info[i][2],
                                        icon=folium.Icon(color='purple', icon='off')))
    if len(all_info) > 30:
        for i in range(20, 30):
            fg2.add_child(folium.Marker(location=(all_info[i][0], all_info[i][1]), popup=all_info[i][2],
                                        icon=folium.Icon(color='darkpurple', icon='off')))
    for i in range(30, len(all_info)):
        fg3.add_child(folium.Marker(location=(all_info[i][0], all_info[i][1]), popup=all_info[i][2],
                                    icon=folium.Icon(color='pink', icon='none')))

    cur_map.add_child(fg)  # adds some layers
    cur_map.add_child(fg0)
    cur_map.add_child(fg1)
    cur_map.add_child(fg2)
    cur_map.add_child(fg3)
    folium.TileLayer('Stamen Terrain').add_to(cur_map)  # adds some map styles
    folium.TileLayer('Stamen Toner').add_to(cur_map)
    folium.TileLayer('Stamen Water Color').add_to(cur_map)
    folium.TileLayer('cartodbpositron').add_to(cur_map)
    folium.TileLayer('cartodbdark_matter').add_to(cur_map)
    cur_map.add_child(folium.LayerControl())  # adds the ability to control layers
    cur_map.save('./html.Map1.html')


def read_database(file_path, year):
    """
    :param year: year of film, have to be searched
    :param file_path: full path to the file
    :return: raw list of films this year, consists of .split('\t') lines
    this list is not parsed
    """
    all_info = []
    year_str = '(' + year + ')'
    with open(file_path, mode='r', encoding='ISO-8859-1') as file1:
        counter = 0
        for line in file1:
            counter += 1
            line = line.split('\t')
            if year_str in line[0]:
                all_info.append(line)
            # if database is loo big, limites it to 30,000 lines
            if counter == 30000:
                break
    return all_info


def parse_list(all_info, latitude, longitude):
    """
    :param all_info:
    :param latitude: latitude_0 -> start input latitude
    :param longitude: longitude_0 -> start input longitude
    :return: raw list of films this year, consists of coordinates,
    description of the film, and distance to coordinates_0
    """
    for i in range(len(all_info)):
        while True:
            if '' in all_info[i]:
                all_info[i].remove('')
            else:
                break
        address = all_info[i][1].split(',')
        while len(address) > 3:
            address.pop(0)
        address = ', '.join(address)
        all_info[i][1] = address
    new_all_info = []
    for i in range(len(all_info)):
        geolocator = Nominatim(user_agent="Artem's app")
        try:
            location = geolocator.geocode(all_info[i][1])
            distance = coordinates_calculator(float(latitude), float(longitude),
                                              float(location.latitude), float(location.longitude))
            new_all_info.append((location.latitude, location.longitude, all_info[i][0], distance))
        except:
            pass
            # this try - except parses lines, where geopy haven't found coordinates
    #print('LEN OF ALL LIST IS', len(all_info))
    #print('LEN OF ALL NEW LIST WITH COORDINATES IS ', len(new_all_info))
    return new_all_info


if __name__ == '__main__':
    all_info = read_database(_your file name_, args.year)
    new_all_info = parse_list(all_info, args.latitude, args.longitude)
    new_all_info = sorted(new_all_info, key=lambda x: x[3])
    map_write(args.latitude, args.longitude, new_all_info)
