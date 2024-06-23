from ingrediente import Ingrediente
from receta import Receta
import db
import api
import analisis

# Crear las tablas en la base de datos
db.crear_tablas()

# Ejemplo de uso de la base de datos
ingredientes_receta = [
    {'id': 1, 'cantidad': 200},
    {'id': 2, 'cantidad': 100}
]
db.agregar_receta("Ensalada César", ingredientes_receta)

# Consultar disponibilidad de ingredientes para una receta
print(db.consultar_receta(1))

# Ejemplo de uso de la API
recetas = api.obtener_recetas_desde_api('pasta')
print(recetas)

# Ejemplo de análisis de CSV
analisis.analizar_csv('ruta/a/tu/archivo.csv')