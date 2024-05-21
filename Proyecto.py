
    
from flask import Flask, jsonify, request # type: ignore
from Ingrediente import Ingrediente
from Receta import Receta

app = Flask(__name__)

ingredientes = [
    Ingrediente('pollo', 250, 'proteina', '3 unidades'),
    Ingrediente('papa', 100, 'carbohidrato', '500 gramos'),
    Ingrediente('zanahoria', 50, 'vegetal', '300 gramos'),
    Ingrediente('cebolla', 30, 'vegetal', '1 unidad'),
    Ingrediente('aceite de oliva', 120, 'grasa', '50 mililitros'),
]

recetas = [
    Receta('Pollo al horno', ['pollo', 'papa', 'zanahoria'], 'media', 400, 60),
    Receta('Ensalada de pollo', ['pollo', 'zanahoria', 'cebolla'], 'fácil', 200, 0),
    Receta('Papas fritas', ['papa', 'aceite de oliva'], 'fácil', 300, 30),
]

@app.route('/ingredientes', methods=['GET'])
def obtener_ingredientes():
    return jsonify({'ingredientes': [ingrediente.a_dic() for ingrediente in ingredientes]})

@app.route('/ingredientes', methods=['POST'])
def agregar_ingrediente():
    data = request.json
    nuevo_ingrediente = Ingrediente(data['nombre'], data['calorias'], data['tipo'], data['cantidad'])
    ingredientes.append(nuevo_ingrediente)
    return jsonify({'mensaje': 'Ingrediente agregado correctamente'})

@app.route('/ingredientes/<nombre>', methods=['DELETE'])
def eliminar_ingrediente(nombre):
    global ingredientes
    ingredientes = [ingrediente for ingrediente in ingredientes if ingrediente.nombre != nombre]
    return jsonify({'mensaje': 'Ingrediente eliminado correctamente'})

@app.route('/recetas', methods=['GET'])
def obtener_recetas():
    return jsonify({'recetas': [receta.a_dic() for receta in recetas]})

@app.route('/recetas', methods=['POST'])
def agregar_receta():
    data = request.json
    nueva_receta = Receta(data['nombre'], data['ingredientes'], data['dificultad'], data['calorias'], data['tiempo_coccion'])
    recetas.append(nueva_receta)
    return jsonify({'mensaje': 'Receta agregada correctamente'})

@app.route('/recetas/<nombre>', methods=['DELETE'])
def eliminar_receta(nombre):
    global recetas
    recetas = [receta for receta in recetas if receta.nombre != nombre]
    return jsonify({'mensaje': 'Receta eliminada correctamente'})

@app.route('/recetas/<nombre>/ingredientes_faltantes', methods=['GET'])
def obtener_ingredientes_faltantes(nombre):
    for receta in recetas:
        if receta.nombre == nombre:
            ingredientes_receta = receta.ingredientes
            ingredientes_disponibles = [ingrediente.nombre for ingrediente in ingredientes]
            faltantes = [ingrediente for ingrediente in ingredientes_receta if ingrediente not in ingredientes_disponibles]
            return jsonify({'ingredientes_faltantes': faltantes})
    return jsonify({'mensaje': 'Receta no encontrada'})

if __name__ == '__main__':
    app.run(debug=True)

