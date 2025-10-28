import sqlite3

def crear_base_datos():
    conexion = sqlite3.connect('rutas.db')
    cursor = conexion.cursor()

    cursor.executescript("""
    DROP TABLE IF EXISTS rutas;
    DROP TABLE IF EXISTS envios;
    DROP TABLE IF EXISTS almacenes;

    -- Tabla de almacenes con id, nombre y ciudad
    CREATE TABLE almacenes (
        id_almacen INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE,
        ciudad TEXT NOT NULL
    );

    -- Tabla de rutas (aristas del grafo)
    CREATE TABLE rutas (
        id_ruta INTEGER PRIMARY KEY AUTOINCREMENT,
        origen TEXT NOT NULL,
        destino TEXT NOT NULL,
        distancia REAL NOT NULL,
        FOREIGN KEY (origen) REFERENCES almacenes(nombre),
        FOREIGN KEY (destino) REFERENCES almacenes(nombre)
    );

    -- Tabla de envíos
    CREATE TABLE envios (
        id_envio INTEGER PRIMARY KEY AUTOINCREMENT,
        origen TEXT NOT NULL,
        destino TEXT NOT NULL,
        FOREIGN KEY (origen) REFERENCES almacenes(nombre),
        FOREIGN KEY (destino) REFERENCES almacenes(nombre)
    );

    -- Insertar almacenes
    INSERT INTO almacenes (nombre, ciudad) VALUES
    ('Almacén Norte', 'Ciudad A'),
    ('Almacén Sur', 'Ciudad B'),
    ('Almacén Este', 'Ciudad C'),
    ('Almacén Oeste', 'Ciudad D'),
    ('Almacén Central', 'Ciudad E'),
    ('Almacén Frontera', 'Ciudad F'),
    ('Almacén Marítimo', 'Ciudad G');

    -- Insertar rutas entre almacenes
    INSERT INTO rutas (origen, destino, distancia) VALUES
    ('Almacén Norte', 'Almacén Sur', 5.0),
    ('Almacén Norte', 'Almacén Este', 10.0),
    ('Almacén Sur', 'Almacén Oeste', 3.0),
    ('Almacén Sur', 'Almacén Central', 8.0),
    ('Almacén Este', 'Almacén Central', 2.0),
    ('Almacén Oeste', 'Almacén Frontera', 4.0),
    ('Almacén Central', 'Almacén Frontera', 1.0),
    ('Almacén Frontera', 'Almacén Marítimo', 6.0),
    ('Almacén Este', 'Almacén Marítimo', 12.0);

    -- Insertar envíos
    INSERT INTO envios (origen, destino) VALUES
    ('Almacén Norte', 'Almacén Frontera'),
    ('Almacén Sur', 'Almacén Marítimo'),
    ('Almacén Este', 'Almacén Oeste'),
    ('Almacén Norte', 'Almacén Marítimo');
    """)

    conexion.commit()
    conexion.close()
    print("Base de datos 'rutas.db' creada correctamente con almacenes (id, nombre, ciudad), rutas y envíos.")

if __name__ == "__main__":
    crear_base_datos()
