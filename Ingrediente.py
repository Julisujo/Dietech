class Ingrediente:
    def __init__(self, nombre, cantidad, unidad):
        self.nombre = nombre
        self.cantidad = cantidad
        self.unidad = unidad

    def to_dict(self):
        return {
            'nombre': self.nombre,
            'cantidad': self.cantidad,
            'unidad': self.unidad
        }