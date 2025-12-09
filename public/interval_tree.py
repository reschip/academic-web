import graphviz
import random

ROJO = 0
NEGRO = 1

class Intervalo:
    def __init__(self, low, high):
        self.low = low
        self.high = high
    
    def __str__(self):
        return f"[{self.low}, {self.high}]"
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        if other is None:
            return False
        return self.low == other.low and self.high == other.high


class NodoIntervalo:
    def __init__(self, intervalo):
        self.intervalo = intervalo
        self.max = intervalo.high if intervalo else 0
        self.izq = None
        self.der = None
        self.p = None
        self.color = ROJO


class ArbolIntervalos:

    def __init__(self):
        self.NIL = NodoIntervalo(Intervalo(0, 0))
        self.NIL.color = NEGRO
        self.NIL.max = float('-inf')
        self.NIL.izq = None
        self.NIL.der = None
        self.NIL.p = None
        self.raiz = self.NIL

    def _actualizar_max(self, x):
        if x != self.NIL:
            m = x.intervalo.high
            if x.izq != self.NIL:
                m = max(m, x.izq.max)
            if x.der != self.NIL:
                m = max(m, x.der.max)
            x.max = m

    def _propagar_max_arriba(self, nodo):
        while nodo is not None and nodo != self.NIL:
            self._actualizar_max(nodo)
            nodo = nodo.p

    # Rotación izquierda
    def rotar_izquierda(self, x):
        y = x.der
        x.der = y.izq

        if y.izq != self.NIL:
            y.izq.p = x

        y.p = x.p

        if x.p == self.NIL:
            self.raiz = y
        elif x == x.p.izq:
            x.p.izq = y
        else:
            x.p.der = y

        y.izq = x
        x.p = y

        self._actualizar_max(x)
        self._actualizar_max(y)

    # Rotación derecha
    def rotar_derecha(self, x):
        y = x.izq
        x.izq = y.der

        if y.der != self.NIL:
            y.der.p = x

        y.p = x.p

        if x.p == self.NIL:
            self.raiz = y
        elif x == x.p.der:
            x.p.der = y
        else:
            x.p.izq = y

        y.der = x
        x.p = y

        self._actualizar_max(x)
        self._actualizar_max(y)

    # INTERVAL-INSERT
    def interval_insert(self, intervalo):
        z = NodoIntervalo(intervalo)
        z.izq = self.NIL
        z.der = self.NIL

        y = self.NIL
        x = self.raiz

        while x != self.NIL:
            y = x
            x.max = max(x.max, intervalo.high)
            
            if z.intervalo.low < x.intervalo.low:
                x = x.izq
            else:
                x = x.der

        z.p = y

        if y == self.NIL:
            self.raiz = z
        elif z.intervalo.low < y.intervalo.low:
            y.izq = z
        else:
            y.der = z

        z.color = ROJO
        self._insertar_fixup(z)

    def _insertar_fixup(self, z):
        while z.p.color == ROJO:
            if z.p == z.p.p.izq:
                y = z.p.p.der

                if y.color == ROJO:
                    z.p.color = NEGRO
                    y.color = NEGRO
                    z.p.p.color = ROJO
                    z = z.p.p
                else:
                    if z == z.p.der:
                        z = z.p
                        self.rotar_izquierda(z)
                    z.p.color = NEGRO
                    z.p.p.color = ROJO
                    self.rotar_derecha(z.p.p)
            else:
                y = z.p.p.izq

                if y.color == ROJO:
                    z.p.color = NEGRO
                    y.color = NEGRO
                    z.p.p.color = ROJO
                    z = z.p.p
                else:
                    if z == z.p.izq:
                        z = z.p
                        self.rotar_derecha(z)
                    z.p.color = NEGRO
                    z.p.p.color = ROJO
                    self.rotar_izquierda(z.p.p)

        self.raiz.color = NEGRO

    # Verifica si dos intervalos se solapan
    def _overlap(self, i1, i2):
        return i1.low <= i2.high and i2.low <= i1.high

    # INTERVAL-SEARCH
    def interval_search(self, i):
        x = self.raiz
        
        while x != self.NIL and not self._overlap(x.intervalo, i):
            if x.izq != self.NIL and x.izq.max >= i.low:
                x = x.izq
            else:
                x = x.der
        
        return x if x != self.NIL else None

    # Busca todos los solapamientos
    def interval_search_all(self, i):
        resultados = []
        self._interval_search_all_helper(self.raiz, i, resultados)
        return resultados

    def _interval_search_all_helper(self, nodo, i, resultados):
        if nodo == self.NIL:
            return
        
        if self._overlap(nodo.intervalo, i):
            resultados.append(nodo)
        
        if nodo.izq != self.NIL and nodo.izq.max >= i.low:
            self._interval_search_all_helper(nodo.izq, i, resultados)
        
        if nodo.der != self.NIL and nodo.intervalo.low <= i.high:
            self._interval_search_all_helper(nodo.der, i, resultados)

    # Búsqueda exacta
    def buscar_exacto(self, intervalo):
        return self._buscar_exacto_helper(self.raiz, intervalo)

    def _buscar_exacto_helper(self, nodo, intervalo):
        if nodo == self.NIL:
            return nodo
        
        if intervalo.low == nodo.intervalo.low and intervalo.high == nodo.intervalo.high:
            return nodo
        
        if intervalo.low < nodo.intervalo.low:
            return self._buscar_exacto_helper(nodo.izq, intervalo)
        else:
            resultado = self._buscar_exacto_helper(nodo.der, intervalo)
            if resultado == self.NIL and intervalo.low == nodo.intervalo.low:
                resultado = self._buscar_exacto_helper(nodo.izq, intervalo)
            return resultado

    def _transplantar(self, u, v):
        if u.p == self.NIL:
            self.raiz = v
        elif u == u.p.izq:
            u.p.izq = v
        else:
            u.p.der = v
        v.p = u.p

    def minimo(self, x=None):
        if x is None:
            x = self.raiz
        while x.izq != self.NIL:
            x = x.izq
        return x

    # INTERVAL-DELETE
    def interval_delete(self, intervalo):
        z = self.buscar_exacto(intervalo)
        
        if z == self.NIL:
            print(f"  {intervalo} no encontrado")
            return False

        y = z
        y_color_original = y.color
        x_padre = None

        if z.izq == self.NIL:
            x = z.der
            x_padre = z.p
            self._transplantar(z, z.der)
        elif z.der == self.NIL:
            x = z.izq
            x_padre = z.p
            self._transplantar(z, z.izq)
        else:
            y = self.minimo(z.der)
            y_color_original = y.color
            x = y.der

            if y.p == z:
                x.p = y
                x_padre = y
            else:
                x_padre = y.p
                self._transplantar(y, y.der)
                y.der = z.der
                y.der.p = y

            self._transplantar(z, y)
            y.izq = z.izq
            y.izq.p = y
            y.color = z.color
            self._actualizar_max(y)

        if x_padre and x_padre != self.NIL:
            self._propagar_max_arriba(x_padre)

        if y_color_original == NEGRO:
            self._borrar_fixup(x)

        return True

    def _borrar_fixup(self, x):
        while x != self.raiz and x.color == NEGRO:
            if x == x.p.izq:
                w = x.p.der

                if w.color == ROJO:
                    w.color = NEGRO
                    x.p.color = ROJO
                    self.rotar_izquierda(x.p)
                    w = x.p.der

                if w.izq.color == NEGRO and w.der.color == NEGRO:
                    w.color = ROJO
                    x = x.p
                else:
                    if w.der.color == NEGRO:
                        w.izq.color = NEGRO
                        w.color = ROJO
                        self.rotar_derecha(w)
                        w = x.p.der
                    w.color = x.p.color
                    x.p.color = NEGRO
                    w.der.color = NEGRO
                    self.rotar_izquierda(x.p)
                    x = self.raiz
            else:
                w = x.p.izq

                if w.color == ROJO:
                    w.color = NEGRO
                    x.p.color = ROJO
                    self.rotar_derecha(x.p)
                    w = x.p.izq

                if w.der.color == NEGRO and w.izq.color == NEGRO:
                    w.color = ROJO
                    x = x.p
                else:
                    if w.izq.color == NEGRO:
                        w.der.color = NEGRO
                        w.color = ROJO
                        self.rotar_izquierda(w)
                        w = x.p.izq
                    w.color = x.p.color
                    x.p.color = NEGRO
                    w.izq.color = NEGRO
                    self.rotar_derecha(x.p)
                    x = self.raiz

        x.color = NEGRO

    def recorrido_inorder(self, x):
        if x != self.NIL:
            self.recorrido_inorder(x.izq)
            color = "R" if x.color == ROJO else "N"
            print(f"{x.intervalo}(max={x.max})({color})", end=' ')
            self.recorrido_inorder(x.der)

    def imprimir_inorder(self):
        self.recorrido_inorder(self.raiz)
        print()

    def imprimir_arbol(self):
        self._imprimir_arbol_helper(self.raiz, "", True)

    def _imprimir_arbol_helper(self, nodo, indent, ultimo):
        if nodo != self.NIL:
            print(indent, end='')
            if ultimo:
                print("R----", end='')
                indent += "     "
            else:
                print("L----", end='')
                indent += "|    "
            
            color_str = "ROJO" if nodo.color == ROJO else "NEGRO"
            print(f"{nodo.intervalo} (max={nodo.max}) [{color_str}]")
            self._imprimir_arbol_helper(nodo.izq, indent, False)
            self._imprimir_arbol_helper(nodo.der, indent, True)

    def generar_diagrama(self, nombre_archivo="arbol_intervalos", formato='png'):
        try:
            dot = graphviz.Digraph(comment='Arbol de Intervalos')
            dot.attr(rankdir='TB')
            dot.node_attr['shape'] = 'record'
            dot.node_attr['style'] = 'filled'
            dot.node_attr['fontname'] = 'Arial'
            dot.node_attr['fontcolor'] = 'white'
            
            if self.raiz == self.NIL:
                dot.node('vacio', 'Arbol Vacio', fillcolor='gray', fontcolor='black')
            else:
                self._agregar_nodos_graphviz(self.raiz, dot)
            
            dot.render(nombre_archivo, format=formato, cleanup=True, view=False)
            print(f"  Diagrama: {nombre_archivo}.{formato}")
            return True
            
        except Exception as e:
            print(f"  Error en diagrama: {e}")
            return False

    def _agregar_nodos_graphviz(self, nodo, dot):
        if nodo != self.NIL:
            color_fill = 'firebrick' if nodo.color == ROJO else 'black'
            etiqueta = f"{nodo.intervalo}\\nmax: {nodo.max}"
            nodo_id = str(id(nodo))
            
            dot.node(nodo_id, etiqueta, fillcolor=color_fill)
            
            if nodo.izq != self.NIL:
                dot.edge(nodo_id, str(id(nodo.izq)))
                self._agregar_nodos_graphviz(nodo.izq, dot)
            else:
                nil_id = f"nil_izq_{nodo_id}"
                dot.node(nil_id, "NIL", shape="point", width="0.1", fillcolor="black")
                dot.edge(nodo_id, nil_id)
            
            if nodo.der != self.NIL:
                dot.edge(nodo_id, str(id(nodo.der)))
                self._agregar_nodos_graphviz(nodo.der, dot)
            else:
                nil_id = f"nil_der_{nodo_id}"
                dot.node(nil_id, "NIL", shape="point", width="0.1", fillcolor="black")
                dot.edge(nodo_id, nil_id)

    def crear_desde_lista(self, lista_intervalos):
        for intervalo in lista_intervalos:
            self.interval_insert(intervalo)
        return self

    def obtener_todos_intervalos(self):
        intervalos = []
        self._obtener_todos_helper(self.raiz, intervalos)
        return intervalos

    def _obtener_todos_helper(self, nodo, lista):
        if nodo != self.NIL:
            self._obtener_todos_helper(nodo.izq, lista)
            lista.append(nodo.intervalo)
            self._obtener_todos_helper(nodo.der, lista)


def crear_arbol_desde_lista(lista_intervalos):
    arbol = ArbolIntervalos()
    arbol.crear_desde_lista(lista_intervalos)
    return arbol


if __name__ == "__main__":
    
    print("\nArbol de Intervalos\n")
    
    arbol = ArbolIntervalos()
    lista_intervalos = []
    
    print("\nInsertando 10 intervalos:\n")
    for _ in range(10):
        low = random.randint(1, 50)
        length = random.randint(5, 20)
        intervalo = Intervalo(low, low + length)
        lista_intervalos.append(intervalo)
        arbol.interval_insert(intervalo)
        print(f"  INSERT {intervalo}")
    
    print("\nArbol inicial:")
    arbol.imprimir_arbol()
    arbol.generar_diagrama("arbol_0_inicial")
    
    # Busqueda inicial
    busqueda = Intervalo(random.randint(10, 30), random.randint(35, 50))
    print(f"\nBusqueda: {busqueda}")
    resultado = arbol.interval_search(busqueda)
    if resultado:
        print(f"  Encontrado: {resultado.intervalo}")
    else:
        print("  No encontrado")
    
    for iteracion in range(1, 4):
        print(f"\n--- Iteracion {iteracion} ---")
        
        print("\nEliminando 5 intervalos:")
        if len(lista_intervalos) >= 5:
            a_borrar = lista_intervalos[:5]
            lista_intervalos = lista_intervalos[5:]
            
            for intervalo in a_borrar:
                print(f"  DELETE {intervalo}")
                arbol.interval_delete(intervalo)
        
        print("\nInsertando 5 intervalos:")
        for _ in range(5):
            low = random.randint(1, 60)
            length = random.randint(5, 25)
            nuevo = Intervalo(low, low + length)
            print(f"  INSERT {nuevo}")
            lista_intervalos.append(nuevo)
            arbol.interval_insert(nuevo)
        
        print(f"\nArbol resultante:")
        arbol.imprimir_arbol()
        arbol.generar_diagrama(f"arbol_{iteracion}_iteracion")
        
        busqueda = Intervalo(random.randint(15, 35), random.randint(40, 55))
        print(f"\nBusqueda: {busqueda}")
        resultado = arbol.interval_search(busqueda)
        
        if resultado:
            print(f"  Encontrado: {resultado.intervalo}")
            todos = arbol.interval_search_all(busqueda)
            if len(todos) > 1:
                print(f"  Total solapamientos: {len(todos)}")
                for nodo in todos:
                    print(f"    - {nodo.intervalo}")
        else:
            print("  No encontrado")
    
