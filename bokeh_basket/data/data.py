import sqlite3
from math import sqrt

def obtener_informacion_bd(id_game, id_player):
    # Establecer la conexión con la base de datos
    conn = sqlite3.connect("basketball/db.sqlite3")

    # Crear un cursor para ejecutar consultas SQL
    cur = conn.cursor()

    # Ejecutar una consulta SQL para obtener la información deseada
    consulta = "SELECT x, y, made FROM shot_statistics WHERE id_game = ? AND id_player = ?;"
    parametros = (id_game, id_player)
    cur.execute(consulta, parametros)

    # Obtener los resultados de la consulta
    resultados = cur.fetchall()

    # Cerrar el cursor y la conexión
    cur.close()
    conn.close()

    # Cambiar la distribución de los resultados en un diccionario
    diccionario_distribuido = {
        "x": [],
        "y": [],
        "made": []
    }
    for fila in resultados:
        diccionario_distribuido["x"].append(fila[0])
        diccionario_distribuido["y"].append(fila[1])
        diccionario_distribuido["made"].append("Anotado" if fila[2] else "Fallado")

    # Devolver el diccionario de resultados
    return diccionario_distribuido

# prueba = obtener_informacion_bd(2354542, 5)
# print(prueba)

def actualizar_informacion_bd(id_game, id_player, datos):
    # Establecer la conexión con la base de datos
    conn = sqlite3.connect("basketball/db.sqlite3")

    # Crear un cursor para ejecutar consultas SQL
    cur = conn.cursor()

    # Crear una consulta SQL SELECT para consultar el id_team del jugador
    seleccionar_consulta = "SELECT id_team FROM players WHERE id = ?"
    seleccionar_parametros = (id_player)

    # Ejecutar la consulta
    cur.execute(seleccionar_consulta, seleccionar_parametros)

    # Obtener los resultados
    resultados = cur.fetchall()

    # Guardar el id_team
    id_team = resultados[0][0]

    # Eliminar los valores existentes para el id_game y id_player dados
    eliminar_consulta = "DELETE FROM shot_statistics WHERE id_game = ? AND id_player = ?"
    eliminar_parametros = (id_game, id_player)
    cur.execute(eliminar_consulta, eliminar_parametros)

    # Insertar los nuevos valores en la base de datos
    insertar_consulta = "INSERT INTO shot_statistics (id_game, id_player, id_team, x, y, made, threep) VALUES (?, ?, ?, ?, ?, ?, ?)"
    for i in range(len(datos["x"])):
        x = datos["x"][i]
        y = datos["y"][i]
        made = datos["made"][i]
        threep = dentro_del_area(x, y)
        insertar_parametros = (id_game, id_player, id_team, x, y, made, threep)
        cur.execute(insertar_consulta, insertar_parametros)

    # Crear una consulta SQL SELECT para calcular los tiros intentados, anotados y porcentaje
    seleccionar_consulta = "SELECT made, threep FROM shot_statistics WHERE id_game = ? AND id_player = ?"
    seleccionar_parametros = (id_game, id_player)

    # Ejecutar la consulta
    cur.execute(seleccionar_consulta, seleccionar_parametros)

    # Obtener los resultados
    resultados = cur.fetchall()

    # Obtener estadísticas generales
    fga = 0
    fgm = 0
    threepa = 0
    threepm = 0

    for resultado in resultados:
        fga += 1 if not resultado[1] else 0
        fgm += 1 if (resultado[0] and not resultado[1]) else 0
        threepa += 1 if resultado[1] else 0
        threepm += 1 if (resultado[0] and resultado[1]) else 0
    
    if fga > 0:
        fgperc = fgm / fga
    else:
        fgperc = 0
    
    if threepa > 0:
        threepperc = threepm / threepa
    else:
        threepperc = 0

    # Crear una consulta SQL INSERT ... ON DUPLICATE KEY UPDATE
    insertar_o_actualizar_consulta = """
        INSERT INTO statistics (id_game, id_player, id_team, fgm, fga, fgperc, threepm, threepa, threepperc) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT (id_game, id_player, id_team) DO UPDATE SET
        fgm = EXCLUDED.fgm,
        fga = EXCLUDED.fga,
        fgperc = EXCLUDED.fgperc,
        threepm = EXCLUDED.threepm,
        threepa = EXCLUDED.threepa,
        threepperc = EXCLUDED.threepperc
    """
    insertar_o_actualizar_parametros = (id_game, id_player, id_team, fgm, fga, fgperc, threepm, threepa, threepperc)

    # Ejecutar la consulta
    cur.execute(insertar_o_actualizar_consulta, insertar_o_actualizar_parametros)

    # Confirmar los cambios en la base de datos
    conn.commit()

    # Cerrar el cursor y la conexión
    cur.close()
    conn.close()

def dentro_del_area(x, y):
    # Definir las coordenadas del centro y el radio del semicírculo
    centro_x, centro_y = 249, 421
    radio = 180

    # Ecuación del semicírculo
    radio_calculado = sqrt((x - centro_x) ** 2 + (y - centro_y) ** 2)

    # Lineas borde
    x_1 = 69
    x_2 = 429
    y_1 = 476

    # Comprobar si está fuera o dentro
    if x < x_1 or x > x_2:
        return True
    elif x >= x_1 and x <= x_2 and radio_calculado > radio:
        return True
    else:
        return False