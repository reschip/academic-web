ROJO = 0
NEGRO = 1

class NodoRN:
    def __init__(self, key):
        self.key = key
        self.izq = None
        self.der = None
        self.p = None
        self.color = ROJO  

class ArbolRojoNegro:
    """
    Implementación de Árbol Rojo-Negro basada en el libro de Cormen (CLRS).
    
    Propiedades del Árbol Rojo-Negro:
    1. Cada nodo es rojo o negro.
    2. La raíz es negra.
    3. Cada hoja (NIL) es negra.
    4. Si un nodo es rojo, entonces ambos hijos son negros.
    5. Para cada nodo, todos los caminos desde el nodo hasta las hojas 
       descendientes contienen el mismo número de nodos negros.
    """
    
    def __init__(self):
        # Crear el nodo centinela NIL
        self.NIL = NodoRN(None)
        self.NIL.color = NEGRO
        self.NIL.izq = None
        self.NIL.der = None
        self.NIL.p = None
        self.raiz = self.NIL
    
    
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
    
    
    def insertar(self, key):

        z = NodoRN(key)
        z.izq = self.NIL
        z.der = self.NIL
        
        y = self.NIL
        x = self.raiz
        
        while x != self.NIL:
            y = x
            if z.key < x.key:
                x = x.izq
            else:
                x = x.der
        
        z.p = y
        
        if y == self.NIL:
            self.raiz = z
        elif z.key < y.key:
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
    
    
    def _transplantar(self, u, v):

        if u.p == self.NIL:
            self.raiz = v
        elif u == u.p.izq:
            u.p.izq = v
        else:
            u.p.der = v
        v.p = u.p
    
    
    def borrar(self, z):

        y = z
        y_color_original = y.color
        
        if z.izq == self.NIL:
            x = z.der
            self._transplantar(z, z.der)
        elif z.der == self.NIL:
            x = z.izq
            self._transplantar(z, z.izq)
        else:
            y = self.minimo(z.der)
            y_color_original = y.color
            x = y.der
            
            if y.p == z:
                x.p = y
            else:
                self._transplantar(y, y.der)
                y.der = z.der
                y.der.p = y
            
            self._transplantar(z, y)
            y.izq = z.izq
            y.izq.p = y
            y.color = z.color
        
        if y_color_original == NEGRO:
            self._borrar_fixup(x)
    
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
    
    def borrar_por_llave(self, k):
        nodo = self.buscar_nodo(k)
        if nodo != self.NIL:
            self.borrar(nodo)
            return True
        return False
    
    
    def buscar(self, x, k):
        if x == self.NIL or k == x.key:
            return x
        if k < x.key:
            return self.buscar(x.izq, k)
        else:
            return self.buscar(x.der, k)
    
    def buscar_nodo(self, k):
        return self.buscar(self.raiz, k)
    
    
    def minimo(self, x=None):
        if x is None:
            x = self.raiz
        while x.izq != self.NIL:
            x = x.izq
        return x
    
    def maximo(self, x=None):
        if x is None:
            x = self.raiz
        while x.der != self.NIL:
            x = x.der
        return x
    
    
    def sucesor(self, x):
        if x.der != self.NIL:
            return self.minimo(x.der)
        y = x.p
        while y != self.NIL and x == y.der:
            x = y
            y = y.p
        return y
    
    def predecesor(self, x):
        if x.izq != self.NIL:
            return self.maximo(x.izq)
        y = x.p
        while y != self.NIL and x == y.izq:
            x = y
            y = y.p
        return y
    
    # Recorridos    
    def recorrido_inorder(self, x):
        if x != self.NIL:
            self.recorrido_inorder(x.izq)
            color = "R" if x.color == ROJO else "N"
            print(f"{x.key}({color})", end=' ')
            self.recorrido_inorder(x.der)
    
    def imprimir_inorder(self):
        self.recorrido_inorder(self.raiz)
        print()
    
    def recorrido_preorder(self, x):
        if x != self.NIL:
            color = "R" if x.color == ROJO else "N"
            print(f"{x.key}({color})", end=' ')
            self.recorrido_preorder(x.izq)
            self.recorrido_preorder(x.der)
    
    def imprimir_preorder(self):
        self.recorrido_preorder(self.raiz)
        print()
    
    def recorrido_postorder(self, x):
        if x != self.NIL:
            self.recorrido_postorder(x.izq)
            self.recorrido_postorder(x.der)
            color = "R" if x.color == ROJO else "N"
            print(f"{x.key}({color})", end=' ')
    
    def imprimir_postorder(self):
        self.recorrido_postorder(self.raiz)
        print()
    
    # Funciones de utilidad  para el grafo   
    def crear_desde_lista(self, lista_llaves):
        """Crea un árbol desde una lista de llaves."""
        for llave in lista_llaves:
            self.insertar(llave)
        return self
    
    # Funciones de utilidad  para el grafo   
    def _generar_dot_nodos(self, nodo, lineas, contador):
        if nodo == self.NIL:
            return contador
        
        if nodo.color == ROJO:
            color_fondo = "red"
            color_texto = "white"
        else:
            color_fondo = "black"
            color_texto = "white"        
        lineas.append(f'    n{id(nodo)} [label="{nodo.key}", style=filled, fillcolor={color_fondo}, fontcolor={color_texto}];')
        
        # Procesar hijos
        if nodo.izq != self.NIL:
            contador = self._generar_dot_nodos(nodo.izq, lineas, contador)
            lineas.append(f'    n{id(nodo)} -> n{id(nodo.izq)};')
        else:
            # Nodo NIL izquierdo
            nil_id = f"nil{contador}"
            contador += 1
            lineas.append(f'    {nil_id} [label="NIL", shape=rectangle, style=filled, fillcolor=gray, fontsize=10, width=0.3, height=0.2];')
            lineas.append(f'    n{id(nodo)} -> {nil_id};')
        
        if nodo.der != self.NIL:
            contador = self._generar_dot_nodos(nodo.der, lineas, contador)
            lineas.append(f'    n{id(nodo)} -> n{id(nodo.der)};')
        else:
            # Nodo NIL derecho
            nil_id = f"nil{contador}"
            contador += 1
            lineas.append(f'    {nil_id} [label="NIL", shape=rectangle, style=filled, fillcolor=gray, fontsize=10, width=0.3, height=0.2];')
            lineas.append(f'    n{id(nodo)} -> {nil_id};')
        
        return contador
    
    def generar_dot(self, titulo="Árbol Rojo-Negro"):
        lineas = []
        lineas.append(f'digraph ArbolRojoNegro {{')
        lineas.append(f'    label="{titulo}";')
        lineas.append(f'    labelloc="t";')
        lineas.append(f'    node [shape=circle, fontname="Arial", fontsize=12];')
        lineas.append(f'    edge [arrowsize=0.8];')
        
        if self.raiz != self.NIL:
            self._generar_dot_nodos(self.raiz, lineas, 0)
        else:
            lineas.append('    vacio [label="Árbol vacío", shape=plaintext];')
        
        lineas.append('}')
        return '\n'.join(lineas)
    
    def guardar_dot(self, nombre_archivo, titulo="Árbol Rojo-Negro"):
        dot = self.generar_dot(titulo)
        with open(nombre_archivo, 'w') as f:
            f.write(dot)
        return nombre_archivo
    
    def generar_imagen(self, nombre_archivo, titulo="Árbol Rojo-Negro", formato="png"):
        try:
            import graphviz
            
            g = graphviz.Digraph('ArbolRojoNegro', format=formato)
            g.attr(label=titulo, labelloc='t')
            g.attr('node', shape='circle', fontname='Arial', fontsize='12')
            g.attr('edge', arrowsize='0.8')
            
            if self.raiz != self.NIL:
                self._agregar_nodos_graphviz(self.raiz, g, [0])
            else:
                g.node('vacio', 'Árbol vacío', shape='plaintext')
            
            g.render(nombre_archivo, cleanup=True)
            print(f"Imagen: {nombre_archivo}.{formato}")
            return f"{nombre_archivo}.{formato}"
        except ImportError:
            dot_archivo = nombre_archivo + ".dot"
            self.guardar_dot(dot_archivo, titulo)
            return dot_archivo
        except Exception as e:
            print(f"Error: {e}")
            dot_archivo = nombre_archivo + ".dot"
            self.guardar_dot(dot_archivo, titulo)
            return dot_archivo
    
    def _agregar_nodos_graphviz(self, nodo, g, contador):
        """Agrega nodos al grafo de Graphviz."""
        if nodo == self.NIL:
            return
        
        nodo_id = f"n{id(nodo)}"
        
        if nodo.color == ROJO:
            g.node(nodo_id, str(nodo.key), style='filled', fillcolor='red', fontcolor='white')
        else:
            g.node(nodo_id, str(nodo.key), style='filled', fillcolor='black', fontcolor='white')
        
        if nodo.izq != self.NIL:
            self._agregar_nodos_graphviz(nodo.izq, g, contador)
            g.edge(nodo_id, f"n{id(nodo.izq)}")
        else:
            nil_id = f"nil{contador[0]}"
            contador[0] += 1
            g.node(nil_id, 'NIL', shape='rectangle', style='filled', fillcolor='gray', fontsize='10', width='0.3', height='0.2')
            g.edge(nodo_id, nil_id)
        
        if nodo.der != self.NIL:
            self._agregar_nodos_graphviz(nodo.der, g, contador)
            g.edge(nodo_id, f"n{id(nodo.der)}")
        else:
            nil_id = f"nil{contador[0]}"
            contador[0] += 1
            g.node(nil_id, 'NIL', shape='rectangle', style='filled', fillcolor='gray', fontsize='10', width='0.3', height='0.2')
            g.edge(nodo_id, nil_id)
    
    
def crear_arbol_desde_lista(lista_llaves):
    arbol = ArbolRojoNegro()
    arbol.crear_desde_lista(lista_llaves)
    return arbol


if __name__ == "__main__":
    llaves = [15, 6, 18, 3, 7, 17, 20, 2, 4, 13, 9]
    arbol = crear_arbol_desde_lista(llaves)
    arbol.imprimir_arbol()
