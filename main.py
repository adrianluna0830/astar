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


def ventana():
    import tkinter as tk

    raiz = tk.Tk()
    raiz.title('A* - Tarea 2,3')
    metodo = tk.StringVar(value='A*')
    estado = tk.StringVar()
    tabla = tk.StringVar()
    automatico, pasos = False, None

    def dibujar(paso):
        tablero.delete('all')
        orden = {nodo: i + 1 for i, nodo in enumerate(paso['visitados'])}
        for fila in range(FILAS):
            for columna in range(COLUMNAS):
                nodo = fila, columna
                color, marca = '#ffffff', ''
                if nodo in MUROS:
                    color, marca = '#f3b3a9', 'X'
                elif nodo in orden:
                    color, marca = '#e8e5dc', str(orden[nodo])
                elif nodo in paso['frontera']:
                    color, marca = '#ddefef', 'F'
                if nodo in paso['ruta']:
                    color = '#bcd5ff'
                if nodo == INICIO:
                    marca = 'S ' + marca
                elif nodo == META:
                    marca = 'M ' + marca
                x, y = 35 + columna * 56, 30 + fila * 56
                borde = '#f3a447' if nodo == paso['actual'] else '#b7b7b7'
                tablero.create_rectangle(x, y, x + 56, y + 56, fill=color, outline=borde,
                                         width=4 if nodo == paso['actual'] else 1)
                tablero.create_text(x + 28, y + 28, text=marca, font=('Arial', 13))
        for fila in range(FILAS):
            tablero.create_text(15, 58 + fila * 56, text=fila)
        for columna in range(COLUMNAS):
            tablero.create_text(63 + columna * 56, 15, text=columna)
        estimar = manhattan if metodo.get() == 'A*' else lambda nodo: 0
        nodos = sorted(paso['frontera'], key=lambda n: (paso['frontera'][n] + estimar(n), estimar(n)))
        lineas = ['Pendientes | g h f']
        for nodo in nodos:
            g, h = paso['frontera'][nodo], estimar(nodo)
            lineas.append(f'{nodo} | {g} | {h} | {g + h}')
        tabla.set('\n'.join(lineas))

    def avanzar():
        nonlocal automatico, pasos
        if pasos is None:
            return
        paso = next(pasos, None)
        if paso is None:
            estado.set('Sin camino')
            automatico, pasos = False, None
            return
        dibujar(paso)
        g, h = paso['g'], paso['h']
        estado.set(f"Paso {len(paso['visitados'])} | Actual: {paso['actual']} | g={g} h={h} f={g + h}")
        if paso['ruta']:
            estado.set(estado.get() + f' | Costo final: {len(paso["ruta"]) - 1}')
            automatico, pasos = False, None

    def reiniciar():
        nonlocal pasos, automatico
        pasos = buscar(metodo.get() == 'A*')
        automatico = False
        estado.set('Listo')
        dibujar(dict(actual=None, visitados=[], frontera={INICIO: 0}, ruta=[]))

    def correr():
        if automatico:
            avanzar()
        raiz.after(500, correr)

    def alternar():
        nonlocal automatico
        automatico = not automatico and pasos is not None
        if automatico:
            avanzar()

    controles = tk.Frame(raiz)
    controles.pack(pady=10)
    for nombre in ['A*', 'BFS']:
        tk.Radiobutton(controles, text=nombre, variable=metodo, value=nombre, command=reiniciar).pack(side='left')
    for nombre, accion in [('Paso', avanzar), ('Auto / Pausa', alternar), ('Reiniciar', reiniciar)]:
        tk.Button(controles, text=nombre, command=accion).pack(side='left', padx=5)
    tk.Label(raiz, textvariable=estado, font=('Arial', 12)).pack(padx=15)
    contenido = tk.Frame(raiz)
    contenido.pack()
    tablero = tk.Canvas(contenido, width=550, height=435)
    tablero.pack(side='left')
    tk.Label(contenido, textvariable=tabla, justify='left', anchor='nw',
             width=30, font=('Monospace', 11)).pack(side='left', fill='y', padx=15)
    tk.Label(raiz, text='F: pendiente · X: muro · Azul: ruta').pack(pady=5)
    reiniciar()
    correr()
    raiz.mainloop()


if __name__ == '__main__':
    texto() if '--texto' in sys.argv else ventana()
