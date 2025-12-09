---
title: "Tarea 10: Árbol de Intervalos"
description: "Pseudocódigo e implementación en Python de un árbol de intervalos basado en árboles rojo-negro con operaciones de inserción, borrado y búsqueda de solapamientos."
pubDate: 2025-12-09
heroImage: "/~andres.cruz/images/posts/Tarea10.png"
tags: ["árbol de intervalos", "interval tree", "estructuras de datos", "algoritmos", "árbol rojo-negro"]
course: "Análisis y Diseño de Algoritmos"
readTime: "18 min read"
imageType: 1
---

## Información de la Tarea

**Estudiante:** Andrés Cruz Chipol  
**Curso:** Análisis y Diseño de Algoritmos  
**Fecha de entrega:** Martes 9 de diciembre, 2025

## Descripción de la Tarea

Realizar el árbol de intervalos usando un árbol rojo y negro. Llenar el árbol con 10 intervalos. Quitar y poner 5 intervalos. Repetir tres veces el punto anterior y visualizar los árboles resultantes. También checar en cada árbol la búsqueda de algún intervalo y reportarlo.

---

# Árbol de Intervalos

## Introducción

Un **árbol de intervalos** es una estructura de datos que mantiene un conjunto dinámico de intervalos cerrados, permitiendo operaciones eficientes de inserción, borrado y búsqueda de intervalos que se solapan con un intervalo dado.

El árbol de intervalos es una extensión de los árboles de búsqueda binaria balanceados (específicamente árboles rojo-negro) donde cada nodo almacena un intervalo `[low, high]` y un valor adicional `max` que representa el máximo extremo derecho de todos los intervalos en su subárbol.

## Propiedades del Árbol de Intervalos

Un árbol de intervalos tiene las siguientes características:

1. **Basado en BST:** Los nodos se ordenan por el extremo inferior (`low`) del intervalo.
2. **Atributo max:** Cada nodo mantiene el máximo de todos los extremos superiores (`high`) en su subárbol.
3. **Balance:** Utiliza las propiedades de un árbol rojo-negro para mantener el balance.
4. **Solapamiento:** Dos intervalos `[a, b]` y `[c, d]` se solapan si `a ≤ d` y `c ≤ b`.

El atributo `max` es crucial para la eficiencia de la búsqueda, ya que permite podar ramas del árbol que no pueden contener intervalos solapados.

## Operaciones del Árbol de Intervalos

Las operaciones principales son:

- **interval_insert**: Inserta un nuevo intervalo manteniendo las propiedades del árbol rojo-negro y actualizando los valores `max`.
- **interval_delete**: Elimina un intervalo y rebalancea el árbol.
- **interval_search**: Busca un intervalo que se solape con el intervalo dado.
- **interval_search_all**: Encuentra todos los intervalos que se solapan con el intervalo dado.

Todas las operaciones se realizan en tiempo **O(log n)**, excepto `interval_search_all` que es O(k log n) donde k es el número de solapamientos.

---

## Pseudocódigo

### Estructura del Nodo de Intervalo

```
INTERVAL-NODE
    int      : intervalo [low, high]
    max      : máximo extremo derecho en el subárbol
    left     : hijo izquierdo
    right    : hijo derecho
    p        : padre
    color    : ROJO o NEGRO
```

### Verificación de Solapamiento

```
OVERLAP(i1, i2)
1   return i1.low ≤ i2.high and i2.low ≤ i1.high
```

### Actualizar Max

```
UPDATE-MAX(x)
1   if x ≠ T.nil
2       m = x.int.high
3       if x.left ≠ T.nil
4           m = max(m, x.left.max)
5       if x.right ≠ T.nil
6           m = max(m, x.right.max)
7       x.max = m
```

### Rotación Izquierda (con actualización de max)

```
LEFT-ROTATE(T, x)
1   y = x.right
2   x.right = y.left
3   if y.left ≠ T.nil
4       y.left.p = x
5   y.p = x.p
6   if x.p == T.nil
7       T.root = y
8   elseif x == x.p.left
9       x.p.left = y
10  else x.p.right = y
11  y.left = x
12  x.p = y
13  UPDATE-MAX(x)          // Actualizar max después de rotación
14  UPDATE-MAX(y)
```

### Rotación Derecha (con actualización de max)

```
RIGHT-ROTATE(T, x)
1   y = x.left
2   x.left = y.right
3   if y.right ≠ T.nil
4       y.right.p = x
5   y.p = x.p
6   if x.p == T.nil
7       T.root = y
8   elseif x == x.p.right
9       x.p.right = y
10  else x.p.left = y
11  y.right = x
12  x.p = y
13  UPDATE-MAX(x)          // Actualizar max después de rotación
14  UPDATE-MAX(y)
```

### Insertar Intervalo

```
INTERVAL-INSERT(T, i)
1   z = new INTERVAL-NODE with interval i
2   z.max = i.high
3   z.left = T.nil
4   z.right = T.nil
5   y = T.nil
6   x = T.root
7   while x ≠ T.nil
8       y = x
9       x.max = max(x.max, i.high)     // Actualizar max en el camino
10      if i.low < x.int.low
11          x = x.left
12      else x = x.right
13  z.p = y
14  if y == T.nil
15      T.root = z
16  elseif z.int.low < y.int.low
17      y.left = z
18  else y.right = z
19  z.color = RED
20  RB-INSERT-FIXUP(T, z)
```

### Buscar Intervalo con Solapamiento

```
INTERVAL-SEARCH(T, i)
1   x = T.root
2   while x ≠ T.nil and not OVERLAP(x.int, i)
3       if x.left ≠ T.nil and x.left.max ≥ i.low
4           x = x.left
5       else x = x.right
6   return x
```

### Buscar Todos los Solapamientos

```
INTERVAL-SEARCH-ALL(T, i)
1   resultados = []
2   INTERVAL-SEARCH-ALL-HELPER(T.root, i, resultados)
3   return resultados

INTERVAL-SEARCH-ALL-HELPER(nodo, i, resultados)
1   if nodo == T.nil
2       return
3   if OVERLAP(nodo.int, i)
4       resultados.append(nodo)
5   if nodo.left ≠ T.nil and nodo.left.max ≥ i.low
6       INTERVAL-SEARCH-ALL-HELPER(nodo.left, i, resultados)
7   if nodo.right ≠ T.nil and nodo.int.low ≤ i.high
8       INTERVAL-SEARCH-ALL-HELPER(nodo.right, i, resultados)
```

### Eliminar Intervalo

```
INTERVAL-DELETE(T, i)
1   z = BUSCAR-EXACTO(T, i)
2   if z == T.nil
3       return FALSE
4   y = z
5   y-original-color = y.color
6   if z.left == T.nil
7       x = z.right
8       x-padre = z.p
9       RB-TRANSPLANT(T, z, z.right)
10  elseif z.right == T.nil
11      x = z.left
12      x-padre = z.p
13      RB-TRANSPLANT(T, z, z.left)
14  else y = TREE-MINIMUM(z.right)
15      y-original-color = y.color
16      x = y.right
17      if y.p == z
18          x.p = y
19          x-padre = y
20      else x-padre = y.p
21          RB-TRANSPLANT(T, y, y.right)
22          y.right = z.right
23          y.right.p = y
24      RB-TRANSPLANT(T, z, y)
25      y.left = z.left
26      y.left.p = y
27      y.color = z.color
28      UPDATE-MAX(y)
29  PROPAGAR-MAX-ARRIBA(x-padre)     // Propagar max hacia arriba
30  if y-original-color == BLACK
31      RB-DELETE-FIXUP(T, x)
32  return TRUE
```

### Propagar Max hacia Arriba

```
PROPAGAR-MAX-ARRIBA(nodo)
1   while nodo ≠ nil and nodo ≠ T.nil
2       UPDATE-MAX(nodo)
3       nodo = nodo.p
```

---

## Implementación en Python

```python
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
```

---

## Demostración con Múltiples Iteraciones

Se creó un árbol de intervalos con 10 intervalos aleatorios iniciales, y se realizaron 3 iteraciones donde en cada una se eliminan 5 intervalos y se insertan 5 nuevos, demostrando que la estructura mantiene sus propiedades después de cada operación.

```python
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
```

---

## Resultados

### Árbol Inicial

**Insertando 10 intervalos:**

```
Arbol de Intervalos

Insertando 10 intervalos:

  INSERT [8, 13]
  INSERT [7, 12]
  INSERT [8, 28]
  INSERT [40, 47]
  INSERT [38, 50]
  INSERT [9, 23]
  INSERT [41, 53]
  INSERT [39, 50]
  INSERT [25, 36]
  INSERT [24, 43]

Arbol inicial:
R----[9, 23] (max=53) [NEGRO]
     L----[8, 13] (max=28) [ROJO]
     |    L----[7, 12] (max=12) [NEGRO]
     |    R----[8, 28] (max=28) [NEGRO]
     R----[38, 50] (max=53) [ROJO]
          L----[25, 36] (max=43) [NEGRO]
          |    L----[24, 43] (max=43) [ROJO]
          R----[40, 47] (max=53) [NEGRO]
               L----[39, 50] (max=50) [ROJO]
               R----[41, 53] (max=53) [ROJO]

Busqueda: [19, 49]
  Encontrado: [9, 23]
```

**Visualización del árbol inicial:**

![Árbol Inicial](/~andres.cruz/arbol_0_inicial.png)

---

### Iteración 1

**Eliminando 5 intervalos e insertando 5 nuevos:**

```
--- Iteracion 1 ---

Eliminando 5 intervalos:
  DELETE [8, 13]
  DELETE [7, 12]
  DELETE [8, 28]
  DELETE [40, 47]
  DELETE [38, 50]

Insertando 5 intervalos:
  INSERT [55, 76]
  INSERT [28, 47]
  INSERT [18, 23]
  INSERT [8, 23]
  INSERT [29, 35]

Arbol resultante:
R----[39, 50] (max=76) [NEGRO]
     L----[24, 43] (max=47) [ROJO]
     |    L----[9, 23] (max=23) [NEGRO]
     |    |    L----[8, 23] (max=23) [ROJO]
     |    |    R----[18, 23] (max=23) [ROJO]
     |    R----[28, 47] (max=47) [NEGRO]
     |         L----[25, 36] (max=36) [ROJO]
     |         R----[29, 35] (max=35) [ROJO]
     R----[41, 53] (max=76) [NEGRO]
          R----[55, 76] (max=76) [ROJO]

Busqueda: [27, 41]
  Encontrado: [39, 50]
  Total solapamientos: 6
    - [39, 50]
    - [24, 43]
    - [28, 47]
    - [25, 36]
    - [29, 35]
    - [41, 53]
```

**Visualización del árbol después de la iteración 1:**

![Árbol Iteración 1](/~andres.cruz/arbol_1_iteracion.png)

---

### Iteración 2

**Eliminando 5 intervalos e insertando 5 nuevos:**

```
--- Iteracion 2 ---

Eliminando 5 intervalos:
  DELETE [9, 23]
  DELETE [41, 53]
  DELETE [39, 50]
  DELETE [25, 36]
  DELETE [24, 43]

Insertando 5 intervalos:
  INSERT [21, 31]
  INSERT [37, 46]
  INSERT [9, 21]
  INSERT [12, 24]
  INSERT [21, 40]

Arbol resultante:
R----[28, 47] (max=76) [NEGRO]
     L----[18, 23] (max=40) [ROJO]
     |    L----[9, 21] (max=24) [NEGRO]
     |    |    L----[8, 23] (max=23) [ROJO]
     |    |    R----[12, 24] (max=24) [ROJO]
     |    R----[21, 31] (max=40) [NEGRO]
     |         R----[21, 40] (max=40) [ROJO]
     R----[37, 46] (max=76) [NEGRO]
          L----[29, 35] (max=35) [ROJO]
          R----[55, 76] (max=76) [ROJO]

Busqueda: [15, 53]
  Encontrado: [28, 47]
  Total solapamientos: 9
    - [28, 47]
    - [18, 23]
    - [9, 21]
    - [8, 23]
    - [12, 24]
    - [21, 31]
    - [21, 40]
    - [37, 46]
    - [29, 35]
```

**Visualización del árbol después de la iteración 2:**

![Árbol Iteración 2](/~andres.cruz/arbol_2_iteracion.png)

---

### Iteración 3

**Eliminando 5 intervalos e insertando 5 nuevos:**

```
--- Iteracion 3 ---

Eliminando 5 intervalos:
  DELETE [55, 76]
  DELETE [28, 47]
  DELETE [18, 23]
  DELETE [8, 23]
  DELETE [29, 35]

Insertando 5 intervalos:
  INSERT [9, 24]
  INSERT [12, 20]
  INSERT [37, 60]
  INSERT [54, 72]
  INSERT [31, 53]

Arbol resultante:
R----[21, 31] (max=72) [NEGRO]
     L----[9, 24] (max=24) [ROJO]
     |    L----[9, 21] (max=21) [NEGRO]
     |    R----[12, 24] (max=24) [NEGRO]
     |         R----[12, 20] (max=20) [ROJO]
     R----[37, 46] (max=72) [ROJO]
          L----[21, 40] (max=53) [NEGRO]
          |    R----[31, 53] (max=53) [ROJO]
          R----[37, 60] (max=72) [NEGRO]
               R----[54, 72] (max=72) [ROJO]

Busqueda: [23, 40]
  Encontrado: [21, 31]
  Total solapamientos: 7
    - [21, 31]
    - [9, 24]
    - [12, 24]
    - [37, 46]
    - [21, 40]
    - [31, 53]
    - [37, 60]
```

**Visualización del árbol después de la iteración 3:**

![Árbol Iteración 3](/~andres.cruz/arbol_3_iteracion.png)

---

## Referencias

Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). Introduction to algorithms (3ra ed.). MIT Press. Capítulo 14: Augmenting Data Structures.

