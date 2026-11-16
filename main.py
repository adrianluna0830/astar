import sys

FILAS, COLUMNAS = 7, 9
INICIO, META = (3, 1), (3, 7)
MUROS = {(fila, 4) for fila in range(1, 5)}
MOVIMIENTOS = [(0, 1), (1, 0), (-1, 0), (0, -1)]


def manhattan(nodo):
    return abs(nodo[0] - META[0]) + abs(nodo[1] - META[1])


def buscar(informada=True):
    estimar = manhattan if informada else lambda nodo: 0
    frontera = {INICIO: 0}
    costos, padres, visitados = {INICIO: 0}, {}, []
    while frontera:
        actual = min(frontera, key=lambda nodo: (frontera[nodo] + estimar(nodo), estimar(nodo)))
        frontera.pop(actual)
        visitados.append(actual)
        ruta = []
        if actual == META:
            ruta = [META]
            while ruta[-1] != INICIO:
                ruta.append(padres[ruta[-1]])
            ruta.reverse()
        else:
            for df, dc in MOVIMIENTOS:
                vecino = actual[0] + df, actual[1] + dc
                fila, columna = vecino
                if not (0 <= fila < FILAS and 0 <= columna < COLUMNAS):
                    continue
                if vecino in MUROS or vecino in visitados:
                    continue
                costo = costos[actual] + 1
                if costo < costos.get(vecino, float('inf')):
                    costos[vecino], padres[vecino] = costo, actual
                    frontera.pop(vecino, None)
                    frontera[vecino] = costo
        yield dict(actual=actual, g=costos[actual], h=estimar(actual),
                   visitados=visitados.copy(), frontera=frontera.copy(), ruta=ruta)
        if ruta:
            return


def texto():
    for nombre, informada in [('A*', True), ('BFS', False)]:
        print(nombre)
        for paso in buscar(informada):
            print(paso['actual'], 'g:', paso['g'], 'h:', paso['h'], 'f:', paso['g'] + paso['h'])
        print('Nodos:', len(paso['visitados']), 'Costo:', len(paso['ruta']) - 1)
        print('Ruta:', paso['ruta'])


if __name__ == '__main__':
    texto()
