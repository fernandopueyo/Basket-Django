from .models import Clasificacion

# Vista clasificacion
def obtener_clasificacion():
    clasificacion = Clasificacion.objects.all().select_related("id_team").order_by("posicion")
    
    return clasificacion

def clasificacion_view():
    clasificacion = obtener_clasificacion()
    context = {
        'clasificacion': clasificacion
    }
    return context