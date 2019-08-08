#-*- encoding: latin1-*-
"""Views, archivo para el backend del servidor"""
import json
from rest_framework_jwt.settings import api_settings
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, HttpResponseBadRequest
from django.contrib.staticfiles import finders
from django.views.decorators.csrf import csrf_exempt
from .utils import *
from .models import Buildings, Users, Favorites, Salons, Notifications
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist



def obtain_buildings(request):
    """Service that returns the information of all the buildings (including geometry)"""
    dictionary = {}
    info_list = []
    buildings = Buildings.objects.all()
    for building in buildings:
        feature_element = {}
        feature_element["type"] = "Feature"
        feature_element["identificador"] = "Bloque"+str(building.id)
        geometry = {}
        geometry["type"] = "Polygon"
        external_coords = []
        media_coords = []
        geom_long = len(building.geom[0][0])
        for i in range(geom_long):
            coords_tuple = building.geom[0][0][i]
            coordinates = []
            coordinates.append(coords_tuple[1])
            coordinates.append(coords_tuple[0])
            media_coords.append(coordinates)
        external_coords.append(media_coords)
        geometry["coordinates"] = external_coords
        feature_element["geometry"] = geometry
        info_list.append(feature_element)
    dictionary["features"] = info_list
    dictionary["type"] = "FeatureCollection"
    return HttpResponse(json.dumps(dictionary, ensure_ascii=False).encode("utf-8"),
                        content_type="application/json")


def obtain_buildings_info(request):
    """Service that returns the information of all the buildings (excluding geometry)"""
    dictionary = {}
    info_list = []
    buildings = Buildings.objects.all()
    for building in buildings:
        feature_element = {}
        feature_element["type"] = "Feature"
        feature_element["identificador"] = "Bloque"+str(building.id)
        information = {"codigo": building.code_infra,
                       "nombre": building.name_espol, "unidad": building.unity_name}
        information["bloque"] = building.code_infra
        information["tipo"] = building.building_type
        information["descripcio"] = building.description
        feature_element["properties"] = information
        info_list.append(feature_element)
    dictionary["features"] = info_list
    dictionary["type"] = "FeatureCollection"
    return HttpResponse(json.dumps(dictionary, ensure_ascii=False).encode("utf-8")\
        , content_type="application/json")


def alternative_names(request):
    """Service that returns the official and alternative names of all the buildings.
    Used to populate the search bar of the Android app """
    feature_element = {}
    buildings = Buildings.objects.all()
    count = 1
    #Adding buildings
    for building in buildings:
        dictionary = {}
        dictionary["name_espol"] = building.name_espol
        info_list = []
        #code_infra = building.code_infra
        #if (code_infra is not None and code_infra != ""):
            #info_list.append("Bloque "+building.code_infra)
        code_gtsi = building.code_gtsi
        if (code_gtsi is not None and code_gtsi != ""):
            info_list.append(building.code_gtsi)
        alternative_names = building.alternative_names
        if  alternative_names is not None and alternative_names != "":
            names = alternative_names.strip().split(",")
            for name in names:
                info_list.append(name)
        dictionary["code_gtsi"] = code_gtsi
        dictionary["code_infra"] = building.code_infra
        dictionary["alternative_names"] = info_list
        dictionary["type"] = building.building_type
        feature_element[count] = dictionary
        count += 1
    #Adding salons
    salons = Salons.objects.all()
    for salon in salons:
        dictionary = {}
        dictionary["name_espol"] = beautify_name(salon.name_espol)
        info_list = []
        code_gtsi = salon.building.code_gtsi
        code_infra = salon.building.code_infra
        dictionary["code_gtsi"] = code_gtsi
        dictionary["code_infra"] = code_infra
        if (code_gtsi is not None and code_gtsi != ""):
            info_list.append(code_gtsi)
        unity = salon.building.unity_name
        if (unity is not None and unity != ""):
            info_list.append(unity)
        dictionary["alternative_names"] = info_list
        dictionary["type"] = "Aulas"
        feature_element[count] = dictionary
        count += 1
    return HttpResponse(json.dumps(feature_element, ensure_ascii=False).encode("utf-8")\
        , content_type='application/json')


def token_user(request, name_user):
    '''Service that generates tokens of users'''
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    user = Users.objects.get(username=name_user, password=name_user)
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    user.token = str(token)
    user.save()
    datos_retornar = {"access-token": user.token}
    return HttpResponse(json.dumps(datos_retornar, ensure_ascii=False).encode("utf-8")\
        , content_type='application/json')

@csrf_exempt
def login(request):
    """Service that creates a user that logged in for the first time"""
    datos = json.loads(str(request.body)[2:-1])
    usuario = Users.objects.filter(username=datos.get("data").get("username"))
    if len(usuario) > 0:
        user = Users.objects.get(username=datos.get("data").get("username"),\
         password=datos.get("data").get("username"))
        datos_retornar = {"access-token": user.token}
        return HttpResponse(json.dumps(datos_retornar, ensure_ascii=False).encode("utf-8")\
        , content_type='application/json')
    usuario = Users()
    usuario.username = datos.get("data").get("username")
    usuario.password = datos.get("data").get("username")
    usuario.token = "None"
    usuario.save()
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    user = Users.objects.get(username=datos.get("data").get("username"),\
     password=datos.get("data").get("username"))
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    user.token = str(token)
    user.save()
    datos_retornar = {"access-token": user.token}
    return HttpResponse(json.dumps(datos_retornar, ensure_ascii=False).encode("utf-8")\
        , content_type='application/json')



def show_photo(request, codigo):
    """Service that returns the photo of a building, given its gtsi code """
    if request.method == 'GET':
        building = Buildings.objects.filter(code_infra=codigo)
        if len(building) != 1:
            url = "http://www.espol-guide.espol.edu.ec/static/img/espol/espol.png"
            return HttpResponseRedirect(url)
        else:
            full_path = finders.find("img/"+codigo+"/"+codigo+".JPG")
            if full_path == None:
                url = "http://www.espol-guide.espol.edu.ec/static/img/espol/espol.png"
            else:
                url = "http://www.espol-guide.espol.edu.ec/static/img/"+codigo+"/"+codigo+".JPG"
            return HttpResponseRedirect(url)
    else:
        return HttpResponseNotFound('<h1>Invalid request</h1>')


@csrf_exempt
def favorites(request):
    """Service that returns the favorite POIs of a user"""
    if request.method == 'POST':
        token = request.META["HTTP_ACCESS_TOKEN"]
        user = Users.objects.filter(token=token)
        datos = str(request.body)
        datos = json.loads(datos[2:-1])
        code = datos.get("code_gtsi")
        code_in = datos["code_infra"]
        if len(user) > 0:
            if not verify_favorite(code.strip(), user[0].username, code_in):
                if five_favorites(code.strip(), user[0].username):
                    building = Buildings.objects.filter(code_gtsi=code.strip(),\
                     code_infra=code_in.strip())
                    favorites = Favorites()
                    favorites.id_buildings = building[0]
                    favorites.id_users = user[0]
                    favorites.save()
                else:
                    remove_oldest_fav(user[0].username)
                    building = Buildings.objects.filter(code_gtsi=code.strip(), \
                        code_infra=code_in.strip())
                    favorites = Favorites()
                    favorites.id_buildings = building[0]
                    favorites.id_users = user[0]
                    favorites.save()

    if request.method == 'GET':
        token = request.META["HTTP_ACCESS_TOKEN"]
        user = Users.objects.filter(token=token)
    code_pois_favorites_gtsi = []
    code_pois_favorites_infra = []
    if len(user) > 0:
        favorites = Favorites.objects.filter(id_users=user[0].id)
        for fav in favorites:
            building = Buildings.objects.filter(id=fav.id_buildings.id)
            if building[0].code_gtsi == "":
                code_pois_favorites_gtsi.append(" ")
            else:
                code_pois_favorites_gtsi.append(building[0].code_gtsi)
            if building[0].code_infra == "":
                code_pois_favorites_infra.append(" ")
            else:
                code_pois_favorites_infra.append(building[0].code_infra)
    feature = {"codes_gtsi": code_pois_favorites_gtsi, "codes_infra": code_pois_favorites_infra}
    return HttpResponse(json.dumps(feature, ensure_ascii=False).encode("utf-8")\
    , content_type='application/json')

@csrf_exempt
def get_building_centroid(request):
    """Service that returns the centroid of a building"""
    if request.method == 'POST':
        datos = str(request.body)
        datos = json.loads(datos[2:-1])
        code_gtsi = datos.get("code_gtsi")
        code_in = datos.get("code_infra")
        dictionary = {}
        building = Buildings.objects.filter(code_gtsi=code_gtsi.strip(), code_infra=code_in.strip())
        if len(building) == 0:
            building = Buildings.objects.filter(code_gtsi=code_gtsi.strip())

        #If there are no buildings or more than one with that code
        #Return empty dictionary
        if len(building) != 1:
            return HttpResponse(json.dumps(dictionary, ensure_ascii=False).encode("utf-8")\
            , content_type="application/json")
        building = building[0]
        points = []
        geom_long = len(building.geom[0][0])
        for i in range(geom_long):
            coords_tuple = building.geom[0][0][i]
            coordinates = (coords_tuple[1], coords_tuple[0])
            points.append(coordinates)
        centroid = get_centroid(points)
        dictionary["lat"] = centroid[0]
        dictionary["long"] = centroid[1]
        return HttpResponse(json.dumps(dictionary, ensure_ascii=False).encode("utf-8")\
            , content_type="application/json")

@csrf_exempt
def delete_favorite(request):
    """Delete a favorite POIs from your list"""
    code_pois_favorites = []
    if request.method == 'POST':
        datos = json.loads(str(request.body)[2:-1])
        code_gtsi = datos.get("code_gtsi")
        token = request.META["HTTP_ACCESS_TOKEN"]
        user = Users.objects.filter(token=token)
        if len(user) > 0:
            favorites = Favorites.objects.filter(id_users=user[0].id)
            for fav in favorites:
                building = Buildings.objects.filter(id=fav.id_buildings.id)
                if building[0].code_gtsi == code_gtsi:
                    fav.delete()
                    break
        code_pois_favorites_infra = []
        if len(user) > 0:
            favorites = Favorites.objects.filter(id_users=user[0].id)
            for fav in favorites:
                building = Buildings.objects.filter(id=fav.id_buildings.id)
                if building[0].code_gtsi == "":
                    code_pois_favorites.append(" ")
                else:
                    code_pois_favorites.append(building[0].code_gtsi)
                if building[0].code_infra == "":
                    code_pois_favorites_infra.append(" ")
                else:
                    code_pois_favorites_infra.append(building[0].code_infra)
        feature = {"codes_gtsi": code_pois_favorites, "codes_infra":code_pois_favorites_infra}
        return HttpResponse(json.dumps(feature, ensure_ascii=False).encode("utf-8")\
        , content_type='application/json')
    else:
        return HttpResponseNotFound('<h1>Invalid request</h1>')


@csrf_exempt
def notifications_per_user(request):
    """Service that returns the information of all the notification of a user, given by user_id"""
    if request.method == 'POST':
        datos = str(request.body)
        datos = json.loads(datos[2:-1])
        info_list = []
        #get the user object
        user = Users.objects.filter(token=datos["token"])
        if (len(user) == 1):
            #filter notifications by user_id
            notifications = Notifications.objects.filter(id_user = user[0].id)
            notifs_list = []

            for notification in notifications:
                #add each notification to a dictionary
                dictionary = {"notification_id":notification.id, "time_unit" : notification.time_unit,"value" : notification.value,
                "event_ts" : notification.event_ts, "event_title":notification.event_title, "notification_ts": notification.notification_ts}
                notifs_list.append(dictionary)

            response = {"notifications":notifs_list}
            return HttpResponse(json.dumps(response, ensure_ascii=False, default=date_converter).encode("utf-8"),
                                content_type="application/json")
        else:
            return HttpResponseNotFound('<h1>Not Found</h1>') 
    else:
        return HttpResponseBadRequest('<h1>Invalid request</h1>')      

@csrf_exempt
def update_create_notification(request):
    """Service that creates a notification or updates the data of a notification. 
    Specifically, time_unit and value."""
    if request.method == 'POST':
        response = {}
        datos = str(request.body)
        datos = json.loads(datos[2:-1])
        value = datos["value"]
        time_unit = datos["time_unit"]

        if("notification_id" in datos):
            #means there is a notification, and it should be updated
            notification_id = datos["notification_id"]
            
            try:
                notification = Notifications.objects.get(id=notification_id)
                event_ts = notification.event_ts
                new_ts = get_event_datetime(value,time_unit,event_ts)
                notification.notification_ts = new_ts
                notification.save()
                response["result"] = "success"
                response["notification_id"] = notification.id
                response["notification_ts"] = notification.notification_ts
                return HttpResponse(json.dumps(response, default=date_converter).encode("utf-8"), 
                    content_type="application/json")
            except ObjectDoesNotExist:
                print("Could not update notification")
                response["result"] = "error"
                return HttpResponse(json.dumps(response).encode("utf-8"), 
                    content_type="application/json")
        else:
            #means the notification is going to be created
            user = Users.objects.filter(token=datos["token"])
            if (len(user) != 1):
                return HttpResponseBadRequest('<h1>Invalid request</h1>')
            else:
                response = {}
                notification = Notifications()
                notification.value = datos["value"]
                notification.time_unit = datos["time_unit"]
                event_ts = str_to_datetime(datos["event_ts"])
                notification.event_ts = event_ts
                notification.event_title = datos["event_title"]
                notification.event_id = datos["event_id"]
                notification.notification_ts = get_event_datetime(datos["value"],datos["time_unit"],event_ts)
                notification.id_user = user[0]
                notification.save()
                response["result"] = "success"
                response["notification_id"] = notification.id
                response["notification_ts"] = notification.notification_ts
                return HttpResponse(json.dumps(response, default=date_converter).encode("utf-8"), 
                    content_type="application/json")

    else:
        return HttpResponseBadRequest('<h1>Invalid request</h1>')      

def delete_notification(request):
    """View for deleting a notification object, given its id."""
    if request.method == 'POST':
        response = {}
        datos = str(request.body)
        datos = json.loads(datos[2:-1])
        notification_id = datos["notification_id"]
        try:
            instance = Notifications.objects.get(id=notification_id)
            instance.delete()
            response["result"] = "success"
        except ObjectDoesNotExist:
            print("Notification does not exists. Could not delete it.")
            response["result"] = "failure"
        
        return HttpResponse(json.dumps(response).encode("utf-8"), 
                    content_type="application/json")
    else:
        return HttpResponseBadRequest('<h1>Invalid request</h1>')
