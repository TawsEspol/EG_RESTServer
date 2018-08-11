"""Function for views"""
from .models import Buildings, Users, Favorites



def get_centroid(vertexes):
    """Function for get centroid for shapes"""
    _x_list = [vertex[0] for vertex in vertexes]
    _y_list = [vertex[1] for vertex in vertexes]
    _len = len(vertexes)
    _x = sum(_x_list) / _len
    _y = sum(_y_list) / _len
    return(_x, _y)

def verify_favorite(code, user):
    """Function for verify if new POI or not"""
    users = Users.objects.filter(username=user)
    building = Buildings.objects.filter(code_gtsi=code)
    favorites = Favorites.objects.filter(id_buildings=building[0])
    for obj in favorites:
        if obj.id_users.id == users[0].id:
            return True
    return False

def five_favorites(code, user):
    """Function for verify for user only 5 favorites"""
    code_gtsi = code
    users = Users.objects.filter(username=user)
    favorites = Favorites.objects.filter(id_users=users[0])
    return len(favorites) < 5

def remove_oldest_fav(user):
    """Function for remove oldes POIS add in favorite"""
    users = Users.objects.filter(username=user)
    favorites = Favorites.objects.filter(id_users=users[0]).order_by('time_of_create')
    favorites[0].delete()

def beautify_name(name):
    if not any(char.isdigit() for char in name):
        name = name.capitalize()
    return name