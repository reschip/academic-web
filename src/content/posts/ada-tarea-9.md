---
title: "Tarea 9: Árboles Rojo y Negro"
description: "Pseudocódigo e implementación en Python de un árbol de búsqueda binario rojo y negro con operaciones de inserción, borrado y visualización."
pubDate: 2025-11-25
heroImage: "/~andres.cruz/images/posts/Tarea9.png"
tags: ["árbol rojo-negro", "BST", "estructuras de datos", "algoritmos", "balanceo"]
course: "Análisis y Diseño de Algoritmos"
readTime: "15 min read"
imageType: 1
---

## Información de la Tarea

**Estudiante:** Andrés Cruz Chipol  
**Curso:** Análisis y Diseño de Algoritmos  
**Fecha de entrega:** Martes 25 de noviembre, 2025

## Descripción de la Tarea

Hacer el pseudocódigo y el código en Python para crear un árbol de búsqueda binario rojo y negro. Con tres entradas aleatorias crear el árbol rojo y negro insertando nodos y visualizar los tres árboles resultantes. Borrar nodos de forma aleatoria y visualizar el resultado para mostrar que se sigue manteniendo el árbol rojo y negro.

---

# Árbol Rojo-Negro

## Introducción

Un **árbol rojo-negro** es un árbol de búsqueda binario auto-balanceado donde cada nodo tiene un bit extra de almacenamiento: su **color**, que puede ser ROJO o NEGRO. Al restringir la forma en que los nodos se colorean en cualquier camino desde la raíz hasta una hoja, los árboles rojo-negro garantizan que ningún camino sea más del doble de largo que cualquier otro, de modo que el árbol está aproximadamente balanceado.

## Propiedades del Árbol Rojo-Negro

Un árbol de búsqueda binario es un árbol rojo-negro si satisface las siguientes **propiedades rojo-negro**:

1. **Cada nodo es rojo o negro.**
2. **La raíz es negra.**
3. **Cada hoja (NIL) es negra.**
4. **Si un nodo es rojo, entonces ambos hijos son negros.** (No puede haber dos nodos rojos consecutivos)
5. **Para cada nodo, todos los caminos simples desde el nodo hasta las hojas descendientes contienen el mismo número de nodos negros.** (Altura negra)

Estas propiedades garantizan que la altura del árbol sea O(log n), donde n es el número de nodos.

## Operaciones del Árbol Rojo-Negro

Las operaciones básicas como **buscar**, **mínimo**, **máximo**, **sucesor** y **predecesor** son las mismas que en un Árbol de Búsqueda Binaria (BST).

Las operaciones adicionales necesarias para crear y mantener un árbol rojo-negro son:

- **rotar_izquierda**: Rotación hacia la izquierda para rebalancear
- **rotar_derecha**: Rotación hacia la derecha para rebalancear
- **insertar**: Inserta un nuevo nodo y rebalancea el árbol
- **insertar_fixup**: Corrige las violaciones de propiedades después de insertar
- **borrar**: Elimina un nodo y rebalancea el árbol
- **borrar_fixup**: Corrige las violaciones de propiedades después de borrar

Todas las operaciones se realizan en un tiempo **O(log n)**.

---

## Pseudocódigo

**NOTA:** Las operaciones básicas como BUSCAR, MÍNIMO, MÁXIMO, SUCESOR y PREDECESOR son las mismas que en un Árbol de Búsqueda Binaria (BST). Las siguientes son las operaciones adicionales necesarias para crear y mantener un Árbol Rojo-Negro.

### Rotación Izquierda

```
LEFT-ROTATE(T, x)
1   y = x.right                     // y es el hijo derecho de x
2   x.right = y.left                // el subárbol izq de y pasa a ser subárbol der de x
3   if y.left ≠ T.nil
4       y.left.p = x
5   y.p = x.p                       // el padre de x ahora es padre de y
6   if x.p == T.nil
7       T.root = y
8   elseif x == x.p.left
9       x.p.left = y
10  else x.p.right = y
11  y.left = x                      // x pasa a ser hijo izquierdo de y
12  x.p = y
```

### Rotación Derecha

```
RIGHT-ROTATE(T, x)
1   y = x.left                      // y es el hijo izquierdo de x
2   x.left = y.right                // el subárbol der de y pasa a ser subárbol izq de x
3   if y.right ≠ T.nil
4       y.right.p = x
5   y.p = x.p                       // el padre de x ahora es padre de y
6   if x.p == T.nil
7       T.root = y
8   elseif x == x.p.right
9       x.p.right = y
10  else x.p.left = y
11  y.right = x                     // x pasa a ser hijo derecho de y
12  x.p = y
```

### Insertar

```
RB-INSERT(T, z)
1   y = T.nil
2   x = T.root
3   while x ≠ T.nil
4       y = x
5       if z.key < x.key
6           x = x.left
7       else x = x.right
8   z.p = y
9   if y == T.nil
10      T.root = z
11  elseif z.key < y.key
12      y.left = z
13  else y.right = z
14  z.left = T.nil
15  z.right = T.nil
16  z.color = RED
17  RB-INSERT-FIXUP(T, z)
```

### Insertar Fixup

```
RB-INSERT-FIXUP(T, z)
1   while z.p.color == RED
2       if z.p == z.p.p.left
3           y = z.p.p.right         // y es el tío de z
4           if y.color == RED                       // Caso 1
5               z.p.color = BLACK
6               y.color = BLACK
7               z.p.p.color = RED
8               z = z.p.p
9           else if z == z.p.right                  // Caso 2
10              z = z.p
11              LEFT-ROTATE(T, z)
12              z.p.color = BLACK                   // Caso 3
13              z.p.p.color = RED
14              RIGHT-ROTATE(T, z.p.p)
15      else (igual que arriba con "right" y "left" intercambiados)
16  T.root.color = BLACK
```

### Transplantar

```
RB-TRANSPLANT(T, u, v)
1   if u.p == T.nil
2       T.root = v
3   elseif u == u.p.left
4       u.p.left = v
5   else u.p.right = v
6   v.p = u.p
```

### Borrar

```
RB-DELETE(T, z)
1   y = z
2   y-original-color = y.color
3   if z.left == T.nil
4       x = z.right
5       RB-TRANSPLANT(T, z, z.right)
6   elseif z.right == T.nil
7       x = z.left
8       RB-TRANSPLANT(T, z, z.left)
9   else y = TREE-MINIMUM(z.right)
10      y-original-color = y.color
11      x = y.right
12      if y.p == z
13          x.p = y
14      else RB-TRANSPLANT(T, y, y.right)
15          y.right = z.right
16          y.right.p = y
17      RB-TRANSPLANT(T, z, y)
18      y.left = z.left
19      y.left.p = y
20      y.color = z.color
21  if y-original-color == BLACK
22      RB-DELETE-FIXUP(T, x)
```

### Borrar Fixup

```
RB-DELETE-FIXUP(T, x)
1   while x ≠ T.root and x.color == BLACK
2       if x == x.p.left
3           w = x.p.right                           // w es hermano de x
4           if w.color == RED                       // Caso 1
5               w.color = BLACK
6               x.p.color = RED
7               LEFT-ROTATE(T, x.p)
8               w = x.p.right
9           if w.left.color == BLACK and w.right.color == BLACK  // Caso 2
10              w.color = RED
11              x = x.p
12          else if w.right.color == BLACK          // Caso 3
13              w.left.color = BLACK
14              w.color = RED
15              RIGHT-ROTATE(T, w)
16              w = x.p.right
17          w.color = x.p.color                     // Caso 4
18          x.p.color = BLACK
19          w.right.color = BLACK
20          LEFT-ROTATE(T, x.p)
21          x = T.root
22      else (igual que arriba con "right" y "left" intercambiados)
23  x.color = BLACK
```

---

## Implementación en Python

```python
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
                y = z.p.p.der  # tío
                
                if y.color == ROJO:
                    # Caso 1: el tío es rojo
                    z.p.color = NEGRO
                    y.color = NEGRO
                    z.p.p.color = ROJO
                    z = z.p.p
                else:
                    if z == z.p.der:
                        # Caso 2: z es hijo derecho
                        z = z.p
                        self.rotar_izquierda(z)
                    # Caso 3: z es hijo izquierdo
                    z.p.color = NEGRO
                    z.p.p.color = ROJO
                    self.rotar_derecha(z.p.p)
            else:
                y = z.p.p.izq  # tío
                
                if y.color == ROJO:
                    # Caso 1: el tío es rojo
                    z.p.color = NEGRO
                    y.color = NEGRO
                    z.p.p.color = ROJO
                    z = z.p.p
                else:
                    if z == z.p.izq:
                        # Caso 2: z es hijo izquierdo
                        z = z.p
                        self.rotar_derecha(z)
                    # Caso 3: z es hijo derecho
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
                w = x.p.der  # hermano
                
                if w.color == ROJO:
                    # Caso 1
                    w.color = NEGRO
                    x.p.color = ROJO
                    self.rotar_izquierda(x.p)
                    w = x.p.der
                
                if w.izq.color == NEGRO and w.der.color == NEGRO:
                    # Caso 2
                    w.color = ROJO
                    x = x.p
                else:
                    if w.der.color == NEGRO:
                        # Caso 3
                        w.izq.color = NEGRO
                        w.color = ROJO
                        self.rotar_derecha(w)
                        w = x.p.der
                    # Caso 4
                    w.color = x.p.color
                    x.p.color = NEGRO
                    w.der.color = NEGRO
                    self.rotar_izquierda(x.p)
                    x = self.raiz
            else:
                w = x.p.izq  # hermano
                
                if w.color == ROJO:
                    # Caso 1
                    w.color = NEGRO
                    x.p.color = ROJO
                    self.rotar_derecha(x.p)
                    w = x.p.izq
                
                if w.der.color == NEGRO and w.izq.color == NEGRO:
                    # Caso 2
                    w.color = ROJO
                    x = x.p
                else:
                    if w.izq.color == NEGRO:
                        # Caso 3
                        w.der.color = NEGRO
                        w.color = ROJO
                        self.rotar_izquierda(w)
                        w = x.p.izq
                    # Caso 4
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
    
    def recorrido_inorder(self, x):
        if x != self.NIL:
            self.recorrido_inorder(x.izq)
            color = "R" if x.color == ROJO else "N"
            print(f"{x.key}({color})", end=' ')
            self.recorrido_inorder(x.der)
    
    def imprimir_inorder(self):
        self.recorrido_inorder(self.raiz)
        print()
    
    def crear_desde_lista(self, lista_llaves):
        for llave in lista_llaves:
            self.insertar(llave)
        return self

def crear_arbol_desde_lista(lista_llaves):
    arbol = ArbolRojoNegro()
    arbol.crear_desde_lista(lista_llaves)
    return arbol
```

---

## Demostración con Entradas Aleatorias

Se crearon tres árboles rojo-negro con entradas aleatorias de 8 elementos cada uno. Posteriormente, se borró un nodo aleatorio de cada árbol para demostrar que las propiedades del árbol rojo-negro se mantienen.

```python
import random
from arbol_rojo_negro import ArbolRojoNegro

def main():
    print("DEMOSTRACIÓN DE ÁRBOL ROJO-NEGRO")
    
    # Generar las entradas aleatorias
    entradas = [
        random.sample(range(1, 50), 8),
        random.sample(range(1, 50), 8),
        random.sample(range(1, 50), 8)
    ]
    
    print("\nPASO 1: INSERCIÓN CON ENTRADAS ALEATORIAS")
    
    arboles = []
    for i, entrada in enumerate(entradas, 1):
        print(f"\nÁrbol {i} - Entrada: {entrada}")
        arbol = ArbolRojoNegro()
        for valor in entrada:
            arbol.insertar(valor)
        
        arbol.generar_imagen(f"arbol_{i}_insercion", 
                           f"Árbol {i} - Inserción: {entrada}")
        arboles.append((arbol, entrada))
    
    print("\nPASO 2: BORRADO ALEATORIO")
    
    for i, (arbol, entrada) in enumerate(arboles, 1):
        nodo_a_borrar = random.choice(entrada)
        print(f"\nÁrbol {i} - Borrando: {nodo_a_borrar}")
        
        arbol.borrar_por_llave(nodo_a_borrar)
        
        nodos_restantes = sorted([n for n in entrada if n != nodo_a_borrar])
        
        arbol.generar_imagen(f"arbol_{i}_borrado", 
                           f"Árbol {i} - Después de borrar {nodo_a_borrar}")
        print(f"Nodos restantes: {nodos_restantes}")

if __name__ == "__main__":
    main()
```

---

## Resultados

### Ejecución del programa

Al ejecutar el código de demostración con entradas aleatorias, se obtuvieron los siguientes resultados:

```
DEMOSTRACIÓN DE ÁRBOL ROJO-NEGRO

PASO 1: INSERCIÓN CON ENTRADAS ALEATORIAS

Árbol 1 - Entrada: [16, 27, 21, 32, 34, 22, 28, 7]
Imagen: arbol_1_insercion.png

Árbol 2 - Entrada: [8, 40, 30, 29, 31, 33, 13, 16]
Imagen: arbol_2_insercion.png

Árbol 3 - Entrada: [40, 19, 31, 28, 23, 35, 8, 14]
Imagen: arbol_3_insercion.png

PASO 2: BORRADO ALEATORIO

Árbol 1 - Borrando: 22
Imagen: arbol_1_borrado.png
Nodos restantes: [7, 16, 21, 27, 28, 32, 34]

Árbol 2 - Borrando: 33
Imagen: arbol_2_borrado.png
Nodos restantes: [8, 13, 16, 29, 30, 31, 40]

Árbol 3 - Borrando: 23
Imagen: arbol_3_borrado.png
Nodos restantes: [8, 14, 19, 28, 31, 35, 40]
```

---

### Visualización de los Árboles

#### Árbol 1

**Después de inserción** con entrada `[16, 27, 21, 32, 34, 22, 28, 7]`:

![Árbol 1 - Inserción](/~andres.cruz/arbol_1_insercion.png)

**Después de borrar el nodo 22**:

![Árbol 1 - Borrado](/~andres.cruz/arbol_1_borrado.png)

---

#### Árbol 2

**Después de inserción** con entrada `[8, 40, 30, 29, 31, 33, 13, 16]`:

![Árbol 2 - Inserción](/~andres.cruz/arbol_2_insercion.png)

**Después de borrar el nodo 33**:

![Árbol 2 - Borrado](/~andres.cruz/arbol_2_borrado.png)

---

#### Árbol 3

**Después de inserción** con entrada `[40, 19, 31, 28, 23, 35, 8, 14]`:

![Árbol 3 - Inserción](/~andres.cruz/arbol_3_insercion.png)

**Después de borrar el nodo 23**:

![Árbol 3 - Borrado](/~andres.cruz/arbol_3_borrado.png)

---

## Análisis de las Visualizaciones

En las imágenes generadas se puede observar cómo los nodos rojos aparecen en color rojo y los nodos negros en color negro, mientras que los nodos centinela NIL se representan como rectángulos grises. Después de cada operación de inserción y borrado, el árbol mantiene correctamente las cinco propiedades rojo-negro gracias a los procedimientos de fixup que realizan las rotaciones y cambios de color necesarios para preservar el balance de la estructura.

## Conclusión

El desarrollo de esta tarea permitió comprender de manera práctica el funcionamiento de los árboles rojo-negro y su importancia como estructura de datos auto-balanceada. Aunque los procedimientos de fixup presentan múltiples casos a considerar, la lógica subyacente se centra en preservar las cinco propiedades fundamentales del árbol mediante rotaciones y cambios de color. La implementación en Python, junto con la generación de visualizaciones gráficas, facilitó la verificación del correcto funcionamiento de las operaciones de inserción y borrado, demostrando que el árbol mantiene su balance después de cada modificación.

---

## Referencias

Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). Introduction to algorithms (3ra ed.). MIT Press. Capítulo 13: Red-Black Trees.

