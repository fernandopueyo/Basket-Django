from data.data import obtener_informacion_bd, actualizar_informacion_bd

from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from bokeh.models import ColumnDataSource, PointDrawTool, Button
from bokeh.models.widgets import DataTable, TableColumn, SelectEditor, IntEditor
from bokeh.layouts import column, row
from bokeh.models import CustomJS
from bokeh.transform import factor_cmap, factor_mark
from bokeh.io import curdoc

# Ejecutar el servidor
# bokeh serve --show --allow-websocket-origin='*' bokeh_basket 

# Obtener los argumentos de la URL
args = curdoc().session_context.request.arguments

# Obtener las variables de los argumentos
id_game = args.get('id_game')[0].decode('utf-8')
id_player = args.get('id_player')[0].decode('utf-8')

# Construye la ruta a la imagen
# background_image_path = "bokeh_basket/static/images/halfcourt.png"
background_image_path = "/static/statistics_basketball/halfcourt.png" # Ruta para la aplicación en Django

# Obtener puntos de la base de datos
shots = obtener_informacion_bd(id_game=id_game, id_player=id_player)

# Crear un diccionario de ColumnDataSource
source = ColumnDataSource(data=shots)

# Crear la figura
xmin, ymin = 0, 0
xmax, ymax = 500, 500
p = figure(title=None, name="court", toolbar_location=None,
            x_range=(xmin, xmax), y_range=(ymin, ymax))

# Ocultar ejes de la figura
p.axis.visible = False

# Añadir la imagen de la pista de baloncesto
p.image_url(url=[background_image_path], x=xmin, y=ymax,  w=xmax - xmin, h=ymax - ymin, alpha=0.8)

# Añadir los puntos
shot_made = ["Anotado", "Fallado"]
color_made = ["green", "red"]
markers_made = ["circle", "x"]
renderer = p.scatter(x='x', y='y', size=12, fill_alpha=0.4, color=factor_cmap('made', color_made, shot_made), marker=factor_mark('made', markers_made, shot_made), legend_group='made', source=source)
draw_tool = PointDrawTool(renderers=[renderer])
p.add_tools(draw_tool)
p.toolbar.active_tap = draw_tool

# Crear la tabla
columns = [
    TableColumn(field="x", title="Coord. X", editor=IntEditor()),
    TableColumn(field="y", title="Coord. Y", editor=IntEditor()),
    TableColumn(field="made", title="Anotado", editor=SelectEditor(options=shot_made))
]
data_table = DataTable(source=source, columns=columns, editable=True, width=400, height=280, name="shot_table")

# Crear el botón
button = Button(label="Guardar tiros", button_type="success")

# Crear el callback
def save_button_callback():
    datos = {"x": [], "y": [], "made": []}
    # Obtener los puntos
    for i in range(len(source.data['x'])):
        datos["x"].append(int(round(source.data['x'][i])))
        datos["y"].append(int(round(source.data['y'][i])))
        datos["made"].append(True if source.data['made'][i] == "Anotado" else False)

    # Guardar las estadísticas del tiro en la base de datos
    actualizar_informacion_bd(id_game=id_game, id_player=id_player, datos=datos)

# Añadir el callback al botón
button.on_click(save_button_callback)

# Crear una fila con la tabla de datos y el botón
fila_inferior = row(data_table, button)

# Añadir los componentes a la página
layout = column(p, fila_inferior)
layout.name = "my_layout"

curdoc().add_root(layout)

