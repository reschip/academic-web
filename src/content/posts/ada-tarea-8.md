---
title: "Tarea 8: Creación de un árbol binario"
description: "Pseudocódigo e implementación en Python de un árbol de búsqueda binario con todas sus operaciones básicas."
pubDate: 2025-11-11
heroImage: "/~andres.cruz/images/posts/Tarea8.png"
tags: ["árbol binario", "BST", "estructuras de datos", "algoritmos"]
course: "Análisis y Diseño de Algoritmos"
readTime: "12 min read"
imageType: 1
---

## Información de la Tarea

**Estudiante:** Andrés Cruz Chipol  
**Curso:** Análisis y Diseño de Algoritmos  
**Fecha de entrega:** Martes 11 de noviembre, 2025

## Descripción de la Tarea

Hacer el pseudocódigo y el código en Python para crear un árbol de búsqueda binario a partir de una lista de llaves.

---

# Árbol de Búsqueda Binario

## Introducción

Un **árbol de búsqueda binario** (BST, por sus siglas en inglés) es una estructura de datos fundamental que permite realizar operaciones de búsqueda, inserción y eliminación de manera eficiente. La propiedad principal de un BST es que para cada nodo, todos los valores en el subárbol izquierdo son menores que el valor del nodo y todos los valores en el subárbol derecho son mayores.

## Operaciones del Árbol de Búsqueda Binario

- **buscar**: Encuentra un nodo con una llave específica
- **minimo**: Encuentra el nodo con la llave mínima
- **maximo**: Encuentra el nodo con la llave máxima
- **sucesor**: Encuentra el sucesor de un nodo
- **predecesor**: Encuentra el predecesor de un nodo
- **insertar**: Inserta un nuevo nodo en el árbol
- **borrar**: Elimina un nodo del árbol
- **recorrido_inorder**: Recorre el árbol en orden
- **recorrido_preorder**: Recorre el árbol en preorden
- **recorrido_postorder**: Recorre el árbol en postorden

Todas estas operaciones se realizan en un tiempo **O(h)**, donde **h** es la altura del árbol.

## Pseudocódigo

### Estructura del Nodo

```
Nodo:
    key: valor almacenado en el nodo
    izq: puntero al hijo izquierdo
    der: puntero al hijo derecho
    p: puntero al padre
```

### Estructura del Árbol

```
ArbolBusquedaBinaria:
    raiz: puntero a la raíz del árbol
    
    Si raiz == NIL entonces el árbol está vacío
```

### Crear árbol desde una lista

```
crear_arbol_desde_lista(A, lista_llaves):
    A.raiz = NIL
    para cada llave en lista_llaves:
        insertar_arbol(A, crear_nodo(llave))
    retornar A
```

### Buscar

```
buscar_arbol(x, k):
    if x == NIL or k == x.key
        return x
    if k < x.key
        return buscar_arbol(x.izq, k)
    else
        return buscar_arbol(x.der, k)
```

### Mínimo

```
minimo_arbol(x):
    while x.izq != NIL
        x = x.izq
    return x
```

### Máximo

```
maximo_arbol(x):
    while x.der != NIL
        x = x.der
    return x
```

### Sucesor

```
sucesor_arbol(x):
    if x.der != NIL
        return minimo_arbol(x.der)
    y = x.p
    while y != NIL and x == y.der
        x = y
        y = y.p
    return y
```

### Predecesor

```
predecesor_arbol(x):
    if x.izq != NIL
        return maximo_arbol(x.izq)
    y = x.p
    while y != NIL and x == y.izq
        x = y
        y = y.p
    return y
```

### Insertar

```
insertar_arbol(A, z):
    y = NIL
    x = A.raiz
    while x != NIL
        y = x
        if z.llave < x.llave
            x = x.izq
        else
            x = x.der
    z.p = y
    if y == NIL
        A.raiz = z
    else if z.llave < y.llave
        y.izq = z
    else
        y.der = z
```

### Transplantar (función auxiliar para borrar)

```
transplantar(A, u, v):
    if u.p == NIL
        A.raiz = v
    else
        if u == u.p.izq
            u.p.izq = v
        else
            u.p.der = v
    if v != NIL
        v.p = u.p
```

### Borrar

```
borrar_nodo_en_arbol(A, z):
    if z.izq == NIL
        transplantar(A, z, z.der)
    else 
        if z.der == NIL
            transplantar(A, z, z.izq)
        else
            y = minimo_arbol(z.der)
            if y.p != z
                transplantar(A, y, y.der)
                y.der = z.der
                y.der.p = y
            transplantar(A, z, y)
            y.izq = z.izq
            y.izq.p = y
```

### Recorrido Inorder

```
recorrido_inorder(x):
    if x != NIL
        recorrido_inorder(x.izq)
        imprimir(x.key)
        recorrido_inorder(x.der)
```

### Recorrido Preorder

```
recorrido_preorder(x):
    if x != NIL
        imprimir(x.key)
        recorrido_preorder(x.izq)
        recorrido_preorder(x.der)
```

### Recorrido Postorder

```
recorrido_postorder(x):
    if x != NIL
        recorrido_postorder(x.izq)
        recorrido_postorder(x.der)
        imprimir(x.key)
```

## Implementación en Python

```python
class Nodo:
    def __init__(self, key):
        self.key = key
        self.izq = None
        self.der = None
        self.p = None

class ArbolBusquedaBinaria:    
    def __init__(self):
        self.raiz = None
    
    def insertar(self, key):
        z = Nodo(key)
        y = None
        x = self.raiz
        
        while x is not None:
            y = x
            if z.key < x.key:
                x = x.izq
            else:
                x = x.der
        z.p = y
        if y is None:
            self.raiz = z
        elif z.key < y.key:
            y.izq = z
        else:
            y.der = z
    
    def crear_desde_lista(self, lista_llaves):
        self.raiz = None
        for llave in lista_llaves:
            self.insertar(llave)
        return self
    
    def buscar(self, x, k):
        if x is None or k == x.key:
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
        while x is not None and x.izq is not None:
            x = x.izq
        return x
    
    def maximo(self, x=None):
        if x is None:
            x = self.raiz
        while x is not None and x.der is not None:
            x = x.der
        return x
    
    def sucesor(self, x):
        if x.der is not None:
            return self.minimo(x.der)
        y = x.p
        while y is not None and x == y.der:
            x = y
            y = y.p
        return y
    
    def predecesor(self, x):
        if x.izq is not None:
            return self.maximo(x.izq)
        y = x.p
        while y is not None and x == y.izq:
            x = y
            y = y.p
        return y
    
    def transplantar(self, u, v):
        if u.p is None:
            self.raiz = v
        elif u == u.p.izq:
            u.p.izq = v
        else:
            u.p.der = v
        if v is not None:
            v.p = u.p
    
    def borrar(self, z):
        if z.izq is None:
            self.transplantar(z, z.der)
        elif z.der is None:
            self.transplantar(z, z.izq)
        else:
            y = self.minimo(z.der)
            if y.p != z:
                self.transplantar(y, y.der)
                y.der = z.der
                y.der.p = y
            self.transplantar(z, y)
            y.izq = z.izq
            y.izq.p = y
    
    def recorrido_inorder(self, x):
        if x is not None:
            self.recorrido_inorder(x.izq)
            print(x.key, end=' ')
            self.recorrido_inorder(x.der)
    
    def imprimir_inorder(self):
        self.recorrido_inorder(self.raiz)
        print()
    
    def recorrido_preorder(self, x):
        if x is not None:
            print(x.key, end=' ')
            self.recorrido_preorder(x.izq)
            self.recorrido_preorder(x.der)
    
    def imprimir_preorder(self):
        self.recorrido_preorder(self.raiz)
        print()
    
    def recorrido_postorder(self, x):
        if x is not None:
            self.recorrido_postorder(x.izq)
            self.recorrido_postorder(x.der)
            print(x.key, end=' ')
    
    def imprimir_postorder(self):
        self.recorrido_postorder(self.raiz)
        print()
    
    def altura(self, x):
        if x is None:
            return -1
        return 1 + max(self.altura(x.izq), self.altura(x.der))
    
    def altura_arbol(self):
        return self.altura(self.raiz)

def crear_arbol_desde_lista(lista_llaves):
    arbol = ArbolBusquedaBinaria()
    arbol.crear_desde_lista(lista_llaves)
    return arbol

if __name__ == "__main__":
    llaves = [15, 6, 18, 3, 7, 17, 20, 2, 4, 13, 9]
    
    print("Creando árbol desde lista:", llaves)
    arbol = crear_arbol_desde_lista(llaves)
    
    print("\nRecorrido Inorder (ordenado):")
    arbol.imprimir_inorder()
    
    print("\nRecorrido Preorder:")
    arbol.imprimir_preorder()
    
    print("\nRecorrido Postorder:")
    arbol.imprimir_postorder()
    
    print("\nMínimo:", arbol.minimo().key if arbol.minimo() else None)
    print("Máximo:", arbol.maximo().key if arbol.maximo() else None)
    
    print("\nBuscando nodo con llave 7:")
    nodo = arbol.buscar_nodo(7)
    if nodo:
        print("Encontrado:", nodo.key)
        if arbol.sucesor(nodo):
            print("Sucesor:", arbol.sucesor(nodo).key)
        if arbol.predecesor(nodo):
            print("Predecesor:", arbol.predecesor(nodo).key)
    
    print("\nAltura del árbol:", arbol.altura_arbol())
```

## Resultados

### Ejecución del programa

Al ejecutar el código con la lista de llaves `[15, 6, 18, 3, 7, 17, 20, 2, 4, 13, 9]`, se obtienen los siguientes resultados:

```
Creando árbol desde lista: [15, 6, 18, 3, 7, 17, 20, 2, 4, 13, 9]

Recorrido Inorder (ordenado):
2 3 4 6 7 9 13 15 17 18 20 

Recorrido Preorder:
15 6 3 2 4 7 13 9 18 17 20 

Recorrido Postorder:
2 4 3 9 13 7 6 17 20 18 15 

Mínimo: 2
Máximo: 20

Buscando nodo con llave 7:
Encontrado: 7
Sucesor: 9
Predecesor: 6

Altura del árbol: 4
```

### Representación Visual del Árbol

La siguiente imagen muestra la estructura del árbol de búsqueda binario creado a partir de la lista `[15, 6, 18, 3, 7, 17, 20, 2, 4, 13, 9]`:

![Árbol de Búsqueda Binaria](/~andres.cruz/arbol_busqueda_binaria.png)


## Conclusión

La implementación del árbol de búsqueda binaria funciona correctamente. El método `crear_desde_lista()` permite construir el árbol a partir de una lista de llaves, y todas las operaciones básicas (buscar, insertar, borrar, recorridos, etc.) se ejecutan como se espera. La complejidad temporal de las operaciones es O(h), donde h es la altura del árbol.

El árbol de búsqueda binario es una estructura de datos fundamental que sirve como base para estructuras más avanzadas como árboles AVL y árboles Rojo-Negro, que mantienen el árbol balanceado para garantizar operaciones en tiempo O(log n).

---

## Referencias

Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). Introduction to algorithms (3ra ed.). MIT Press.

