import sqlite3
import matplotlib.pyplot as plt
import networkx as nx
from collections import defaultdict
import heapq

def crear_conexion():
    #Crea una conexión a la base de datos SQLite
    try:
        conn = sqlite3.connect('rutas.db')
        return conn
    except sqlite3.Error as e:
        print(f"Error conectando a la base de datos: {e}")
        return None


def cargar_datos():
    #Carga los datos de las tablas y construye el grafo
    conn = crear_conexion()
    if not conn:
        return None, None, None
    
    grafo = defaultdict(dict)
    almacenes = []

    # Cargar almacenes
    cursor = conn.execute("SELECT id_almacen, nombre, ciudad FROM almacenes")
    for id_almacen, nombre, ciudad in cursor:
        almacenes.append((id_almacen, nombre, ciudad))
        grafo[nombre] = {}  # Aseguramos que todos los almacenes existan en el grafo
    
    # Cargar rutas
    cursor = conn.execute("SELECT origen, destino, distancia FROM rutas")
    for origen, destino, distancia in cursor:
        grafo[origen][destino] = distancia
        if destino not in grafo:
            grafo[destino] = {}  # Evita KeyError
    
    # Cargar envíos
    envios = []
    cursor = conn.execute("SELECT id_envio, origen, destino FROM envios")
    for envio in cursor:
        envios.append(envio)

    conn.close()
    return grafo, envios, almacenes


def dijkstra(grafo, origen):
    #Implementación del algoritmo de Dijkstra
    distancias = {nodo: float('infinity') for nodo in grafo}
    distancias[origen] = 0
    pq = [(0, origen)]
    previo = {nodo: None for nodo in grafo}
    
    while pq:
        dist_actual, nodo_actual = heapq.heappop(pq)
        
        if dist_actual > distancias[nodo_actual]:
            continue
            
        for vecino, peso in grafo[nodo_actual].items():
            distancia = dist_actual + peso
            
            if distancia < distancias[vecino]:
                distancias[vecino] = distancia
                previo[vecino] = nodo_actual
                heapq.heappush(pq, (distancia, vecino))
    
    return distancias, previo


def obtener_ruta(previo, origen, destino):
    #Reconstruye la ruta desde el origen hasta el destino
    ruta = []
    actual = destino
    
    while actual is not None:
        ruta.append(actual)
        actual = previo[actual]
        
    if not ruta or ruta[-1] != origen:
        return None
    return list(reversed(ruta))


def visualizar_grafo(grafo, rutas_cortas=None):
    #Visualiza el grafo usando matplotlib y networkx
    G = nx.DiGraph()
    
    for origen in grafo:
        for destino, peso in grafo[origen].items():
            G.add_edge(origen, destino, weight=peso)
    
    pos = nx.spring_layout(G)
    
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=600)
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edges(G, pos)
    
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels)
    
    if rutas_cortas:
        edge_colors = ['red' if (u,v) in rutas_cortas else 'black' for u,v in G.edges()]
        nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=2)
    
    plt.title("Grafo de Rutas y Almacenes")
    plt.axis('off')
    plt.show()


def main():
    grafo, envios, almacenes = cargar_datos()
    if not grafo or not envios:
        print("Error al cargar los datos")
        return

    print("Lista de Almacenes:")
    for id_a, nombre, ciudad in almacenes:
        print(f" - {nombre} (ID: {id_a}, Ciudad: {ciudad})")
    
    print("\nProcesando envíos...\n")

    rutas_cortas = set()

    for id_envio, origen, destino in envios:
        distancias, previo = dijkstra(grafo, origen)
        ruta = obtener_ruta(previo, origen, destino)
        
        print(f"Envío {id_envio}:")
        print(f"Origen = {origen}")
        print(f"Destino = {destino}")
        
        if ruta and distancias[destino] != float('infinity'):
            print(f"Distancia mínima = {distancias[destino]}")
            print(f"Ruta = {' -> '.join(map(str, ruta))}")
            for i in range(len(ruta)-1):
                rutas_cortas.add((ruta[i], ruta[i+1]))
        else:
            print("Ruta no encontrada")
        print()
    
    visualizar_grafo(grafo, rutas_cortas)


if __name__ == "__main__":
    main()
