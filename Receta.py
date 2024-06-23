class Receta:
    def __init__(self, nombre, ingredientes):
        self.nombre = nombre
        self.ingredientes = ingredientes

    def to_dict(self):
        return {
            'nombre': self.nombre,
            'ingredientes': [ingrediente.to_dict() for ingrediente in self.ingredientes]
        }