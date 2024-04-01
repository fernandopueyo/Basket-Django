import sqlite3
import requests
import json
import csv
from datetime import datetime


def crear_calendario(ruta_db):
    # Descargar calendario de la federacion
    url_calendar_format = 'https://www.fbcv.es/wp-json/calendario/v1/id_grupo/{grupo}'
    id_grupo = 83398
    calendar = requests.get(url_calendar_format.format(grupo=id_grupo)).json()
    calendar = json.loads(calendar)

    # Connecting Python to SQLite
    conn = sqlite3.connect(ruta_db)
    cur = conn.cursor()

    for jornadas in calendar:
        partidos = jornadas["Partidos"]
        num_jornada = jornadas["NumJornada"]
        for partido in partidos:
            partido = dict(partido)
            id_game = int(partido.get("IdPartido"))
            id_equipo_local = int(partido.get("IdEquipoLocal"))
            id_equipo_visitante = int(partido.get("IdEquipoVisitante"))
            equipo_local = partido.get("eqlocal")
            equipo_visitante = partido.get("eqvisitante")
            fecha_partido = partido.get("FechaPartido")
            fecha_partido = datetime.strptime(fecha_partido, "%d/%m/%Y %H:%M").date()
            resultado_local = int(partido.get("ResultadoLoc"))
            resultado_visitante = int(partido.get("ResultadoVis"))
            cur.execute("""INSERT INTO calendar(
                        num_jornada, id_game, id_equipo_local, id_equipo_visitante, equipo_local, equipo_visitante, fecha_partido, resultado_local, resultado_visitante) VALUES (
                        ?, ?, ?, ?, ?, ?, ?, ?, ?);""",
                        (num_jornada, id_game, id_equipo_local, id_equipo_visitante, equipo_local, equipo_visitante, fecha_partido, resultado_local, resultado_visitante))

    # Make the changes to the database persistent
    conn.commit()

    # Close cursor and communication with the database
    cur.close()
    conn.close()


def crear_clasificacion(ruta_db):
    # Descargar clasificacion de la federacion
    url_clasificacion_format = "https://www.fbcv.es/wp-json/clasificaciones/v1/id_grupo/{grupo}"
    id_grupo = 83398
    clasificacion = requests.get(url_clasificacion_format.format(grupo=id_grupo)).json()
    clasificacion = json.loads(clasificacion)["clasificacion"]

    # Connecting Python to SQLite
    conn = sqlite3.connect(ruta_db)
    cur = conn.cursor()

    for clasificado in clasificacion:
        clasificado = dict(clasificado)
        id_equipo = int(clasificado.get("IdEquipo"))
        posicion = int(clasificado.get("Posicion"))
        jugados = int(clasificado.get("Jugados"))
        puntos = int(clasificado.get("Puntos"))
        ganados = int(clasificado.get("Ganados"))
        perdidos = int(clasificado.get("Perdidos"))
        puntos_favor = int(clasificado.get("PuntosFavor"))
        puntos_contra = int(clasificado.get("PuntosContra"))
        racha = clasificado.get("Racha")
        cur.execute("""INSERT INTO clasificacion(
                    id_team, posicion, jugados, puntos, ganados, perdidos, puntos_favor, puntos_contra, racha) VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?);""",
                    (id_equipo, posicion, jugados, puntos, ganados, perdidos, puntos_favor, puntos_contra, racha))

    # Make the changes to the database persistent
    conn.commit()

    # Close cursor and communication with the database
    cur.close()
    conn.close()


def crear_equipos(ruta_db):
    # Conectar a la base de datos SQLite
    conn = sqlite3.connect(ruta_db)
    cur = conn.cursor()

    # Abrir el archivo CSV y leer los datos
    with open('teams.csv', newline='') as archivo_csv:
        lector_csv = csv.reader(archivo_csv)
        for fila in lector_csv:
            id = fila[0]
            name = fila[1]
            id_team = fila[2]
            # Insertar los datos en la tabla Teams
            cur.execute("""INSERT INTO teams(
                        id, name, id_team) VALUES (
                        ?, ?, ?);""", 
                        (id, name, id_team))
            # Insertar los datos en la tabla Team_statistics
            cur.execute("""INSERT INTO team_statistics(
                        id_team, team) VALUES (
                        ?, ?);""",
                        (id_team, name))
    
    # Guardar los cambios en la base de datos
    conn.commit()
    
    # Cerrar la conexión con la base de datos
    conn.close()

def buscar_por_clave_valor_unico(lista_diccionarios, clave, valor):
    for diccionario in lista_diccionarios:
        if clave in diccionario and diccionario[clave] == valor:
            return diccionario
    return None

def buscar_por_clave_valor_lista(lista_diccionarios, clave, valor):
    resultado = []
    for diccionario in lista_diccionarios:
        if clave in diccionario and diccionario[clave] == valor:
            resultado.append(diccionario)
    return resultado

def crear_estadisticas_equipo(ruta_db):
    # Conexión a la base de datos SQLite
    conn = sqlite3.connect(ruta_db)
    cur = conn.cursor()

    # Cargar datos de la base de datos
    filas_calendario = cur.execute("SELECT * FROM calendar").fetchall()
    columnas_calendario = [descripcion[0] for descripcion in cur.description]
    calendario = [{columnas_calendario[i]: fila[i] for i in range(len(columnas_calendario))} for fila in filas_calendario]

    filas_clasificacion = cur.execute("SELECT * FROM clasificacion").fetchall()
    columnas_clasificacion = [descripcion[0] for descripcion in cur.description]
    clasificacion = [{columnas_clasificacion[i]: fila[i] for i in range(len(columnas_clasificacion))} for fila in filas_clasificacion]
    
    filas_estadisticas_equipo = cur.execute("SELECT * FROM team_statistics").fetchall()
    columnas_estadisticas_equipo = [descripcion[0] for descripcion in cur.description]
    estadisticas_equipo = [{columnas_estadisticas_equipo[i]: fila[i] for i in range(len(columnas_estadisticas_equipo))} for fila in filas_estadisticas_equipo]

    # Actualizar estadisticas de equipo
    for fila in estadisticas_equipo:
        # Clasificacion equipo fila
        clasificacion_fila = buscar_por_clave_valor_unico(clasificacion, "id_team", fila["id_team"])

        # Columnas iguales de la clasificacion
        fila["posicion"] = clasificacion_fila["posicion"]
        fila["jugados"] = clasificacion_fila["jugados"]
        fila["ganados"] = clasificacion_fila["ganados"]
        fila["perdidos"] = clasificacion_fila["perdidos"]

        # Valores de puntos generales
        if fila["jugados"] != 0:
            fila["puntos_favor"] = round(clasificacion_fila["puntos_favor"] / fila["jugados"], 1)
            fila["puntos_contra"] = round(clasificacion_fila["puntos_contra"] / fila["jugados"], 1)
            fila["dif_puntos"] = fila["puntos_favor"] - fila["puntos_contra"]
        else:
            fila["puntos_favor"] = 0
            fila["puntos_contra"] = 0
            fila["dif_puntos"] = 0

        # Partidos del equipo
        partidos_equipo = [partido for partido in calendario if any([
        partido['id_equipo_local'] == fila['id_team'] and partido['resultado_local'] > 0,
        partido['id_equipo_visitante'] == fila['id_team'] and partido['resultado_visitante'] > 0
        ])]

        # Partidos en casa
        partidos_casa = buscar_por_clave_valor_lista(partidos_equipo, "id_equipo_local", fila["id_team"])
        partidos_ganados_casa = [partido for partido in partidos_casa if partido["resultado_local"] > partido["resultado_visitante"]]
        partidos_perdidos_casa = [partido for partido in partidos_casa if partido["resultado_local"] < partido["resultado_visitante"]]
        fila["c_jugados"] = len(partidos_casa)
        fila["c_ganados"] = len(partidos_ganados_casa)
        fila["c_perdidos"] = len(partidos_perdidos_casa)

        # Puntos generales en casa
        if fila["c_jugados"] != 0:
            fila["c_puntos_favor"] = round(sum([partido["resultado_local"] for partido in partidos_casa]) / fila["c_jugados"], 1)
            fila["c_puntos_contra"] = round(sum([partido["resultado_visitante"] for partido in partidos_casa]) / fila["c_jugados"], 1)
            fila["c_dif_puntos"] = fila["c_puntos_favor"] - fila["c_puntos_contra"]
        else:
            fila["c_puntos_favor"] = 0
            fila["c_puntos_contra"] = 0
            fila["c_dif_puntos"] = 0

        # Punos ganados y perdidos en casa
        if fila["c_ganados"] != 0:
            fila["c_g_puntos_favor"] = round(sum([partido["resultado_local"] for partido in partidos_ganados_casa]) / fila["c_ganados"], 1)
            fila["c_g_puntos_contra"] = round(sum([partido["resultado_visitante"] for partido in partidos_ganados_casa]) / fila["c_ganados"], 1)
            fila["c_g_dif_puntos"] = fila["c_g_puntos_favor"] - fila["c_g_puntos_contra"]
        else:
            fila["c_g_puntos_favor"] = 0
            fila["c_g_puntos_contra"] = 0
            fila["c_g_dif_puntos"] = 0
        
        if fila["c_perdidos"] != 0:
            fila["c_p_puntos_favor"] = round(sum([partido["resultado_local"] for partido in partidos_perdidos_casa]) / fila["c_perdidos"], 1)
            fila["c_p_puntos_contra"] = round(sum([partido["resultado_visitante"] for partido in partidos_perdidos_casa]) / fila["c_perdidos"], 1)
            fila["c_p_dif_puntos"] = fila["c_p_puntos_favor"] - fila["c_p_puntos_contra"]
        else:
            fila["c_p_puntos_favor"] = 0
            fila["c_p_puntos_contra"] = 0
            fila["c_p_dif_puntos"] = 0

        # Partidos fuera de casa
        partidos_fuera = buscar_por_clave_valor_lista(partidos_equipo, "id_equipo_visitante", fila["id_team"])
        partidos_ganados_fuera = [partido for partido in partidos_fuera if partido["resultado_local"] < partido["resultado_visitante"]]
        partidos_perdidos_fuera = [partido for partido in partidos_fuera if partido["resultado_local"] > partido["resultado_visitante"]]
        fila["f_jugados"] = len(partidos_fuera)
        fila["f_ganados"] = len(partidos_ganados_fuera)
        fila["f_perdidos"] = len(partidos_perdidos_fuera)

        # Puntos generales fuera de casa
        if fila["f_jugados"] != 0:
            fila["f_puntos_favor"] = round(sum([partido["resultado_visitante"] for partido in partidos_fuera]) / fila["f_jugados"], 1)
            fila["f_puntos_contra"] = round(sum([partido["resultado_local"] for partido in partidos_fuera]) / fila["f_jugados"], 1)
            fila["f_dif_puntos"] = fila["f_puntos_favor"] - fila["f_puntos_contra"]
        else:
            fila["f_puntos_favor"] = 0
            fila["f_puntos_contra"] = 0
            fila["f_dif_puntos"] = 0
        
        # Puntos ganados y perdidos fuera de casa
        if fila["f_ganados"] != 0:
            fila["f_g_puntos_favor"] = round(sum([partido["resultado_visitante"] for partido in partidos_ganados_fuera]) / fila["f_ganados"], 1)
            fila["f_g_puntos_contra"] = round(sum([partido["resultado_local"] for partido in partidos_ganados_fuera]) / fila["f_ganados"], 1)
            fila["f_g_dif_puntos"] = fila["f_g_puntos_favor"] - fila["f_g_puntos_contra"]
        else:
            fila["f_g_puntos_favor"] = 0
            fila["f_g_puntos_contra"] = 0
            fila["f_g_dif_puntos"] = 0

        if fila["f_perdidos"] != 0:
            fila["f_p_puntos_favor"] = round(sum([partido["resultado_visitante"] for partido in partidos_perdidos_fuera]) / fila["f_perdidos"], 1)
            fila["f_p_puntos_contra"] = round(sum([partido["resultado_local"] for partido in partidos_perdidos_fuera]) / fila["f_perdidos"], 1)
            fila["f_p_dif_puntos"] = fila["f_p_puntos_favor"] - fila["f_p_puntos_contra"]
        else:
            fila["f_p_puntos_favor"] = 0
            fila["f_p_puntos_contra"] = 0
            fila["f_p_dif_puntos"] = 0

        # Puntos ganados y perdidos total
        if fila["ganados"] != 0:
            fila["g_puntos_favor"] = round((fila["c_g_puntos_favor"] + fila["f_g_puntos_favor"]) / fila["ganados"], 1)
            fila["g_puntos_contra"] = round((fila["c_g_puntos_contra"] + fila["f_g_puntos_contra"]) / fila["ganados"], 1)
            fila["g_dif_puntos"] = fila["g_puntos_favor"] - fila["g_puntos_contra"]
        else:
            fila["g_puntos_favor"] = 0
            fila["g_puntos_contra"] = 0
            fila["g_dif_puntos"] = 0
        
        if fila["perdidos"] != 0:
            fila["p_puntos_favor"] = round((fila["c_p_puntos_favor"] + fila["f_p_puntos_favor"]) / fila["perdidos"], 1)
            fila["p_puntos_contra"] = round((fila["c_p_puntos_contra"] + fila["f_p_puntos_contra"]) / fila["perdidos"], 1)
            fila["p_dif_puntos"] = fila["p_puntos_favor"] - fila["p_puntos_contra"]
        else:
            fila["p_puntos_favor"] = 0
            fila["p_puntos_contra"] = 0
            fila["p_dif_puntos"] = 0

        # Actualizar la base de datos        
        cur.execute("""UPDATE team_statistics SET
                    posicion = ?, jugados = ?, ganados = ?, perdidos = ?, puntos_favor = ?, puntos_contra = ?, dif_puntos = ?,
                    c_jugados = ?, c_ganados = ?, c_perdidos = ?, c_puntos_favor = ?, c_puntos_contra = ?, c_dif_puntos = ?,
                    c_g_puntos_favor = ?, c_g_puntos_contra = ?, c_g_dif_puntos = ?, c_p_puntos_favor = ?, c_p_puntos_contra = ?, c_p_dif_puntos = ?,
                    f_jugados = ?, f_ganados = ?, f_perdidos = ?, f_puntos_favor = ?, f_puntos_contra = ?, f_dif_puntos = ?,
                    f_g_puntos_favor = ?, f_g_puntos_contra = ?, f_g_dif_puntos = ?, f_p_puntos_favor = ?, f_p_puntos_contra = ?, f_p_dif_puntos = ?,
                    g_puntos_favor = ?, g_puntos_contra = ?, g_dif_puntos = ?, p_puntos_favor = ?, p_puntos_contra = ?, p_dif_puntos = ?
                    WHERE id_team = ?;""",
                    (fila["posicion"], fila["jugados"], fila["ganados"], fila["perdidos"], fila["puntos_favor"], fila["puntos_contra"], fila["dif_puntos"],
                    fila["c_jugados"], fila["c_ganados"], fila["c_perdidos"], fila["c_puntos_favor"], fila["c_puntos_contra"], fila["c_dif_puntos"],
                    fila["c_g_puntos_favor"], fila["c_g_puntos_contra"], fila["c_g_dif_puntos"], fila["c_p_puntos_favor"], fila["c_p_puntos_contra"], fila["c_p_dif_puntos"],
                    fila["f_jugados"], fila["f_ganados"], fila["f_perdidos"], fila["f_puntos_favor"], fila["f_puntos_contra"], fila["f_dif_puntos"],
                    fila["f_g_puntos_favor"], fila["f_g_puntos_contra"], fila["f_g_dif_puntos"], fila["f_p_puntos_favor"], fila["f_p_puntos_contra"], fila["f_p_dif_puntos"],
                    fila["g_puntos_favor"], fila["g_puntos_contra"], fila["g_dif_puntos"], fila["p_puntos_favor"], fila["p_puntos_contra"], fila["p_dif_puntos"],
                    fila["id_team"]))
    
    # Guardar cambios en la base de datos
    conn.commit()

    # Calcular posicion en casa y fuera de casa
    filas_estadisticas_equipo = cur.execute("SELECT * FROM team_statistics").fetchall()
    columnas_estadisticas_equipo = [descripcion[0] for descripcion in cur.description]
    estadisticas_equipo = [{columnas_estadisticas_equipo[i]: fila[i] for i in range(len(columnas_estadisticas_equipo))} for fila in filas_estadisticas_equipo]

    equipos_casa = sorted([team for team in estadisticas_equipo if team['c_jugados'] > 0],
    key=lambda team: (-team['c_ganados'], -team['c_dif_puntos'], -team['c_puntos_favor']))

    equipos_fuera = sorted([team for team in estadisticas_equipo if team['f_jugados'] > 0],
    key=lambda team: (-team['f_ganados'], -team['f_dif_puntos'], -team['f_puntos_favor']))

    posicion_casa = 1
    for row in equipos_casa:
        cur.execute(
            "UPDATE team_statistics SET c_posicion = ? WHERE id_team = ?",
            (posicion_casa, row['id_team'])
        )
        posicion_casa += 1

    posicion_fuera = 1
    for row in equipos_fuera:
        cur.execute(
            "UPDATE team_statistics SET f_posicion = ? WHERE id_team = ?",
            (posicion_fuera, row['id_team'])
        )
        posicion_fuera += 1

    # Guardar cambios en la base de datos
    conn.commit()

    # Cerrar la conexión con la base de datos
    conn.close()

    return 

# Crear las tablas en la base de datos
crear_calendario("../basketball/db.sqlite3")
crear_clasificacion("../basketball/db.sqlite3")
crear_equipos("../basketball/db.sqlite3")
crear_estadisticas_equipo("../basketball/db.sqlite3")