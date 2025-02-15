import pandas as pd

from node import Nodo
from fifo import ColaFIFO
from lifo import ColaLIFO
from prio import ColaPRIORITY

def leer_costos(archivo):
    df = pd.read_csv(archivo)
    costos = {}
    for _, fila in df.iterrows():
        origen, destino, costo = fila['Origen'], fila['Destino'], fila['Cost']
        if origen not in costos:
            costos[origen] = {}
        costos[origen][destino] = costo
    return costos

def leer_heuristica(archivo):
    df = pd.read_csv(archivo)
    return {fila['Activity']: fila['Recovery time after burning 300cal (minutes)'] for _, fila in df.iterrows()}

def obt_ruta_final(nodo):
    ruta = []
    while nodo:
        ruta.append(nodo.estado)
        nodo = nodo.parent
    return ruta[::-1]

def ejecutar_algoritmo(tipo_busqueda, nodo_inicial, nodo_objetivo, costos, heuristicas):
    if tipo_busqueda == "BFS":
        cola = ColaFIFO()
    elif tipo_busqueda == "DFS":
        cola = ColaLIFO()
    elif tipo_busqueda in ["UCS", "A*"]:
        cola = ColaPRIORITY()
    elif tipo_busqueda == "Greedy":
        cola = ColaPRIORITY()
    else:
        raise ValueError("Tipo de búsqueda no válido")

    visitados = set()
    cola.add(nodo_inicial)

    while not cola.empty():
        print("\nCola actual:", [nodo.estado for nodo in cola.cola])
        print("Visitados:", list(visitados))
        
        nodo_actual = cola.pop()
        
        if nodo_actual.estado in visitados:
            continue
        visitados.add(nodo_actual.estado)
        
        if nodo_actual.estado == nodo_objetivo:
            print("\nNodo objetivo encontrado:", nodo_actual.estado)
            print("Ruta Directa:", obt_ruta_final(nodo_actual))
            print("Costo:", nodo_actual.costo_acumulado)
            return nodo_actual

        for hijo, costo in costos.get(nodo_actual.estado, {}).items():
            if hijo not in visitados:
                costo_acumulado = nodo_actual.costo_acumulado + costo
                heuristica = heuristicas.get(hijo, 0) if tipo_busqueda in ["Greedy", "A*"] else 0
                nuevo_nodo = Nodo(hijo, action=f"to {hijo}", parent=nodo_actual, costo_acumulado=costo_acumulado, heuristica=heuristica)
                cola.add(nuevo_nodo)

    print("\nNo se encontró un camino al nodo objetivo.")

# ------------------------------------------------------ MAIN ------------------------------------------------------
archivo_funcion_costo = "funcion_de_costo.csv"
archivo_heuristica = "heuristica.csv"

costos = leer_costos(archivo_funcion_costo)
heuristicas = leer_heuristica(archivo_heuristica)

nodo_inicial = Nodo("Warm-up activities", action="", costo_acumulado=0, heuristica=heuristicas["Warm-up activities"])
nodo_objetivo = "Stretching"
algoritmos = {1: "BFS", 2: "DFS", 3: "UCS", 4: "Greedy", 5: "A*"}

stay = True
while (stay):
    print("\n---------------------------------")
    print("              MENU")
    print("---------------------------------")
    print("Seleccione el tipo de búsqueda:")
    print("1. Breadth-first search (BFS)")
    print("2. Depth-first search (DFS)")
    print("3. Uniform-cost search (UCS)")
    print("4. Greedy Best-first search")
    print("5. A*")
    print("6. Salir")

    opcion = int(input("Ingrese el número de su opción: "))

    if opcion in algoritmos:
        ejecutar_algoritmo(algoritmos[opcion], nodo_inicial, nodo_objetivo, costos, heuristicas)
    elif opcion == 6:
        stay = False
    else:
        print("Opción no válida.")

print("Hasta la proxima! ^°^/")
# ------------------------------------------------------ MAIN ------------------------------------------------------