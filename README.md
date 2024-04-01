# Aplicación de Gestión de Estadísticas de la FBCV con Django

Esta aplicación, desarrollada en Django, te permite explorar y gestionar datos relacionados con el calendario y la clasificación de la FBCV. Además, ofrece la posibilidad de registrarte como jugador de uno de los equipos y añadir tus estadísticas individuales a los partidos. La aplicación utiliza Django Rest Framework para crear una API que facilita el acceso a las estadísticas.

# Pre requisitos para correr las tareas programadas
Instalar redis. 

* Guía para hacerlo en WSL: https://developer.redis.com/create/windows/

* TL; DR:
```
sudo apt-add-repository ppa:redislabs/redis
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install redis-server
```

# ¿Cómo iniciar la aplicación?

Pasos iniciales para la instalación de las librerías necesarias y los ajustes de la aplicación Django. Ejecutar desde la carpeta inicial del repositorio.

1. Instalar dependencias: `pip install -r requirements.txt`
2. Acceder a la carpeta basketball: `cd basketball/`
3. Aplicar migraciones: `python manage.py migrate`
4. Importar tablas ejecutando el script: `python ../importacion_inicial/importar_tablas.py`

Pasos para iniciar Celery y ejecutar las tareas programadas. Ejecutar desde la carpeta basketball.

5. Iniciar Redis server: `redis-server --daemonize yes` (--daemonize ejecutará la instrucción por detrás)
6. Iniciar Celery: `python -m celery -A basketball worker --loglevel=info`
7. Iniciar Celery Beat: `python -m celery -A basketball beat --loglevel=info`

Paso para iniciar la aplicación de Django. Ejecutar desde la carpeta basketball.

8. Iniciar la aplicación de Django: `python manage.py runserver`

Paso para iniciar la aplicación de Bokeh. Ejecutar desde la carpeta inicial del repositorio.

9. Iniciar la aplicación de Bokeh: `bokeh serve --show --allow-websocket-origin='*' bokeh_basket`

Si no es necesario tener actualizaciones de calendario en vivo, omitir los pasos 5, 6 y 7.

# Herramientas Utilizadas
- Django: Framework web de Python.
- Django Rest Framework: Facilita la creación de API REST en Django.
- Celery: Utilizado para la ejecución de las tareas programadas.
- Bokeh: Utilizado para crear gráficas interactivas para introducir puntos manualmente.
- Seaborn: Empleado para representaciones de mapas de calor.
- Tailwind CSS: Utilizado para los estilos de la aplicación web.
