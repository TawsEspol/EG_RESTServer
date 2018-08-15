# EG_RESTServer
Servidor de la aplicacion movil EspolGuide.

[![Python Version][python-image]][python-downloads]
[![DJango Version][django-image]][django-downloads]
[![Postgis Version][postgis-image]][postgis-downloads]

EspolGuide es un aplicacion que ayudara a todos los estudiantes de ESPOL a ubicarse dentro del Campus Gustavo Galindo, ubicando un punto dentro del mapa, donde se podra ademas ver informacion del lugar y conocer la ruta de como llegar al punto escogido.

![](header.png)

## Prerequisitos

Antes de iniciar el servidor se debe constar con la instalación de cierto módulos indispensables para correr el servidor. Debemos seguir los siguientes pasos:

```sh
git clone https://github.com/TawsEspol/EG_RESTServer.git
```
Cambiar al directorio EGRESTServer y ejecutar el script para instalar las dependencias apt necesarios:

```sh
./dependencias_apt
```

Luego instalar las dependencias de python:

```sh
pip install -r requirements.txt
```

## Crear Base

Colocar en user el usuario que desee asi como su contraseña

```sh
sudo -u postgres psql
CREATE DATBASE espolguide_db;
CREATE USER user WITH PASSWORD 'password';
ALTER ROLE user SET client_encoding TO 'utf8';
ALTER ROLE user SET default_transaction_isolation TO 'read committed';
ALTER ROLE user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE espolguide_db TO user;
```

Ahora se debe crear un archivo .env en donde colocaremos lo siguiente:

```sh
SECRET_KEY='' 
DATABASE_HOST=''
DATABASE_USER=''
DATABASE_PASSWORD=''
DATABASE_NAME='espolguide_db'
```
NOTA: 
- La SECRET_KEY es la que da django cuando se crea un proyecto de django
- DATABASE_HOST en donde se encuentra alojada la base de datos ("localhost")
- DATABASE_USER es el usuario que se creo en postgres
- DATABASE_PASSWORD es la contraseña que se le dio al usuario creado



## Poblar Base

Para poblar la base, si se cuentan con los shapefiles primero se debe agregar al .env la siguiente linea con la direccion en donde se encuentran el archivo shp a caragr:

```sh
SHAPES_PATH=''
```

Luego se debe hacer lo siguiente:

```sh
python manage.py shell
```

```sh
>>> from espolguide_app import load
>>> load.run()
```


Si no cuenta con los shapefile se pueden cargar los dumps ya creados con los siguientes comandos

```sh
python manage.py loaddata dumps/buildings.json
python manage.py loaddata dumps/salons.json
```

## Correr las migraciones

```sh
python manage.py makemigrations
python manage.py migrate
```



## Correr el Servidor

OS X y Linux:


```sh
python manage.py runserver tu_ip_publica:8000
```







[python-image]: https://img.shields.io/pypi/pyversions/Django.svg
[django-image]: https://img.shields.io/pypi/dm/Django.svg
[python-downloads]: https://www.python.org/downloads/
[django-downloads]: https://www.djangoproject.com/download/
[postgis-image]: https://img.shields.io/pypi/dm/Django.svg
[postgis-downloads]: http://www.gis-blog.com/how-to-install-postgis-2-3-on-ubuntu-16-04-lts/
