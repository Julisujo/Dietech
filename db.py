import sqlite3

def crear_tablas():
    conn = sqlite3.connect('dietech.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ingredientes (
        id INTEGER PRIMARY KEY,
        nombre TEXT NOT NULL,
        cantidad REAL NOT NULL,
        unidad TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS recetas (
        id INTEGER PRIMARY KEY,
        nombre TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ingredientes_receta (
        receta_id INTEGER,
        ingrediente_id INTEGER,
        cantidad REAL NOT NULL,
        FOREIGN KEY (receta_id) REFERENCES recetas(id),
        FOREIGN KEY (ingrediente_id) REFERENCES ingredientes(id)
    )
    ''')

    conn.commit()
    conn.close()

def agregar_receta(nombre, ingredientes):
    conn = sqlite3.connect('dietech.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO recetas (nombre) VALUES (?)', (nombre,))
    receta_id = cursor.lastrowid
    for ing in ingredientes:
        cursor.execute('INSERT INTO ingredientes_receta (receta_id, ingrediente_id, cantidad) VALUES (?, ?, ?)', (receta_id, ing['id'], ing['cantidad']))
    conn.commit()
    conn.close()

def editar_receta(receta_id, nombre=None, ingredientes=None):
    conn = sqlite3.connect('dietech.db')
    cursor = conn.cursor()
    if nombre:
        cursor.execute('UPDATE recetas SET nombre = ? WHERE id = ?', (nombre, receta_id))
    if ingredientes:
        cursor.execute('DELETE FROM ingredientes_receta WHERE receta_id = ?', (receta_id,))
        for ing in ingredientes:
            cursor.execute('INSERT INTO ingredientes_receta (receta_id, ingrediente_id, cantidad) VALUES (?, ?, ?)', (receta_id, ing['id'], ing['cantidad']))
    conn.commit()
    conn.close()

def mostrar_recetas():
    conn = sqlite3.connect('dietech.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM recetas')
    recetas = cursor.fetchall()
    conn.close()
    return recetas

def filtrar_recetas_por_ingredientes(cantidad_ingredientes):
    conn = sqlite3.connect('dietech.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT r.id, r.nombre, COUNT(ir.ingrediente_id) as num_ingredientes
    FROM recetas r
    JOIN ingredientes_receta ir ON r.id = ir.receta_id
    GROUP BY r.id
    HAVING num_ingredientes <= ?
    ''', (cantidad_ingredientes,))
    recetas = cursor.fetchall()
    conn.close()
    return recetas

def filtrar_recetas_por_kcal(max_kcal):
    # Suponiendo que tienes una columna 'kcal' en la tabla recetas
    conn = sqlite3.connect('dietech.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM recetas WHERE kcal <= ?', (max_kcal,))
    recetas = cursor.fetchall()
    conn.close()
    return recetas

def agregar_ingrediente(nombre, cantidad, unidad):
    conn = sqlite3.connect('dietech.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO ingredientes (nombre, cantidad, unidad) VALUES (?, ?, ?)', (nombre, cantidad, unidad))
    conn.commit()
    conn.close()

def eliminar_ingrediente(ingrediente_id):
    conn = sqlite3.connect('dietech.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM ingredientes WHERE id = ?', (ingrediente_id,))
    conn.commit()
    conn.close()

def consultar_receta(receta_id):
    conn = sqlite3.connect('dietech.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT i.nombre, ir.cantidad, i.cantidad, i.unidad
    FROM ingredientes_receta ir
    JOIN ingredientes i ON ir.ingrediente_id = i.id
    WHERE ir.receta_id = ?
    ''', (receta_id,))
    ingredientes_necesarios = cursor.fetchall()
    conn.close()

    for nombre, cantidad_necesaria, cantidad_disponible, unidad in ingredientes_necesarios:
        if cantidad_disponible < cantidad_necesaria:
            return f"No hay suficiente {nombre}. Necesitas {cantidad_necesaria} {unidad}, pero solo tienes {cantidad_disponible} {unidad}."
    
    return "Todos los ingredientes están disponibles para esta receta."

crear_tablas()