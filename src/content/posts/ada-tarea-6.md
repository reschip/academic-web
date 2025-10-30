---
title: "Tarea 6: Ordenamiento del montón"
description: "Implementación en Python del algoritmo Heapsort con múltiples ejecuciones y datos de entrada variados."
pubDate: 2025-10-28
heroImage: "/~andres.cruz/images/posts/Tarea6.png"
tags: ["heapsort", "algoritmos", "ordenamiento", "heap"]
course: "Análisis y Diseño de Algoritmos"
readTime: "8 min read"
imageType: 1
---

## Información de la Tarea

**Estudiante:** Andrés Cruz Chipol  
**Curso:** Análisis y Diseño de Algoritmos  
**Fecha de entrega:** Martes 28 de octubre, 2025

## Descripción de la Tarea

Programar en python el ordenamiento del montón. Mostrar al menos tres ejecuciones con datos de entrada distintos, tal vez revolviendo aleatoriamente el arreglo de entrada.

---

# Algoritmo Heapsort

## Introducción

El algoritmo **heapsort** es un algoritmo de ordenamiento que combina las mejores características de otros algoritmos de ordenamiento. Como merge sort, tiene un tiempo de ejecución de **O(n lg n)**, pero a diferencia de merge sort, heapsort ordena **in situ** (en el lugar), requiriendo solo un número constante de elementos del arreglo almacenados fuera del arreglo de entrada en cualquier momento.

El heapsort introduce una técnica de diseño de algoritmos importante: el uso de una estructura de datos llamada **"heap"** (montón) para gestionar información.

## Estructura de Datos Heap

### Definición
Un **heap binario** es una estructura de datos de arreglo que se puede ver como un árbol binario casi completo. Cada nodo del árbol corresponde a un elemento del arreglo. El árbol está completamente lleno en todos los niveles excepto posiblemente el más bajo, que se llena de izquierda a derecha.

### Propiedades del Heap
- **Raíz**: El elemento en la posición `A[1]`
- **Padre de i**: `PARENT(i) = ⌊i/2⌋`
- **Hijo izquierdo de i**: `LEFT(i) = 2i`
- **Hijo derecho de i**: `RIGHT(i) = 2i + 1`

### Análisis de Complejidad
- **MAX-HEAPIFY**: O(lg n)
- **BUILD-MAX-HEAP**: O(n)
- **HEAPSORT**: O(n lg n)

## Implementación en Python

```python
from random import random, randint
import time

def obtener_hijo_izq(posicion):
    """Retorna el índice del hijo izquierdo."""
    return 2 * posicion + 1

def obtener_hijo_der(posicion):
    """Retorna el índice del hijo derecho."""
    return 2 * posicion + 2

def obtener_padre(posicion):
    """Retorna el índice del padre."""
    return (posicion - 1) // 2

def restaurar_monton_maximo(lista, posicion, tamano_heap):
    """Mantiene la propiedad del monton máximo."""
    hijo_izq = obtener_hijo_izq(posicion)
    hijo_der = obtener_hijo_der(posicion)
    maximo = posicion
    
    if hijo_izq < tamano_heap and lista[hijo_izq] > lista[maximo]:
        maximo = hijo_izq
    
    if hijo_der < tamano_heap and lista[hijo_der] > lista[maximo]:
        maximo = hijo_der
    
    if maximo != posicion:
        lista[posicion], lista[maximo] = lista[maximo], lista[posicion]
        restaurar_monton_maximo(lista, maximo, tamano_heap)

def crear_monton_maximo(lista):
    """Construye un monton máximo a partir de un arreglo desordenado."""
    n = len(lista)
    inicio = n // 2 - 1
    
    for i in range(inicio, -1, -1):
        restaurar_monton_maximo(lista, i, n)

def ordenamiento_monton(lista):
    if not lista or len(lista) <= 1:
        return lista
    
    crear_monton_maximo(lista)
    tamano_heap = len(lista)
    
    for i in range(len(lista) - 1, 0, -1):
        lista[0], lista[i] = lista[i], lista[0]
        tamano_heap -= 1
        restaurar_monton_maximo(lista, 0, tamano_heap)
    
    return lista

def mezclar_arreglo(lista):
    """Revuelve aleatoriamente los elementos de un arreglo."""
    n = len(lista)
    for i in range(n):
        j = int(random() * n)
        lista[i], lista[j] = lista[j], lista[i]
    return lista

def crear_arreglo_aleatorio(tamano, min_val=1, max_val=100):
    """Genera un arreglo aleatorio de enteros."""
    return [randint(min_val, max_val) for _ in range(tamano)]

def mostrar_resultado(original, ordenado, tiempo):
    print(f"Original: {original}")
    print(f"Ordenado: {ordenado}")
    print(f"Tiempo: {tiempo:.6f}s")

def main():
    # Prueba 1: Arreglo pequeño con números aleatorios
    print("PRUEBA 1: Arreglo pequeño (10 elementos)")
    arr1 = crear_arreglo_aleatorio(10, 1, 50)
    arr1_copia = arr1.copy()
    
    inicio = time.time()
    resultado1 = ordenamiento_monton(arr1_copia)
    fin = time.time()
    
    mostrar_resultado(arr1, resultado1, fin - inicio)
    print()
    
    # Arreglo grande con números aleatorios
    print("PRUEBA: Arreglo grande (50 elementos)")
    arr3 = crear_arreglo_aleatorio(20, 1, 200)
    arr3_copia = arr3.copy()
    inicio = time.time()
    resultado3 = ordenamiento_monton(arr3_copia)
    fin = time.time()
    mostrar_resultado(arr3, resultado3, fin - inicio)
    print()
    # Arreglo grande con números aleatorios
    print("PRUEBA: Arreglo grande 30 elementos)")
    arr3 = crear_arreglo_aleatorio(30, 1, 200)
    arr3_copia = arr3.copy()
    inicio = time.time()
    resultado3 = ordenamiento_monton(arr3_copia)
    fin = time.time()
    mostrar_resultado(arr3, resultado3, fin - inicio)
    print()
    # Arreglo grande con números aleatorios
    print("PRUEBA: Arreglo grande (50 elementos)")
    arr3 = crear_arreglo_aleatorio(10, 1, 200)
    arr3_copia = arr3.copy()
    inicio = time.time()
    resultado3 = ordenamiento_monton(arr3_copia)
    fin = time.time()
    mostrar_resultado(arr3, resultado3, fin - inicio)
    print()

    # Prueba 4: Casos especiales
    print("PRUEBA: Casos especiales")
    print()
    
    # Arreglo ordenado
    arr_ordenado = [1, 2, 3, 4, 5]
    arr_ordenado_copia = arr_ordenado.copy()
    inicio = time.time()
    resultado_ordenado = ordenamiento_monton(arr_ordenado_copia)
    fin = time.time()
    print(f"Ya ordenado: {arr_ordenado} -> {resultado_ordenado} ({fin - inicio:.6f}s)")
    
    # Arreglo descendente
    arr_descendente = [5, 4, 3, 2, 1]
    arr_descendente_copia = arr_descendente.copy()
    inicio = time.time()
    resultado_descendente = ordenamiento_monton(arr_descendente_copia)
    fin = time.time()
    print(f"Descendente: {arr_descendente} -> {resultado_descendente} ({fin - inicio:.6f}s)")
    
    # Arreglo con elementos repetidos
    arr_repetidos = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
    arr_repetidos_copia = arr_repetidos.copy()
    inicio = time.time()
    resultado_repetidos = ordenamiento_monton(arr_repetidos_copia)
    fin = time.time()
    print(f"Con repetidos: {arr_repetidos} -> {resultado_repetidos} ({fin - inicio:.6f}s)")
    

if __name__ == "__main__":
    main()
```

## Resultados de las Pruebas

```
PRUEBA 1: Arreglo pequeño (10 elementos)
Original: [7, 44, 24, 9, 24, 11, 1, 1, 38, 18]
Ordenado: [1, 1, 7, 9, 11, 18, 24, 24, 38, 44]
Tiempo: 0.000013s

PRUEBA: Arreglo grande (50 elementos)
Original: [78, 65, 130, 176, 22, 22, 102, 39, 72, 171, 101, 181, 50, 175, 18, 131, 127, 123, 96, 47]
Ordenado: [18, 22, 22, 39, 47, 50, 65, 72, 78, 96, 101, 102, 123, 127, 130, 131, 171, 175, 176, 181]
Tiempo: 0.000020s

PRUEBA: Arreglo grande 30 elementos)
Original: [123, 196, 185, 83, 42, 165, 48, 113, 95, 144, 95, 2, 85, 149, 180, 74, 189, 82, 123, 175, 41, 92, 67, 98, 59, 130, 76, 15, 40, 87]
Ordenado: [2, 15, 40, 41, 42, 48, 59, 67, 74, 76, 82, 83, 85, 87, 92, 95, 95, 98, 113, 123, 123, 130, 144, 149, 165, 175, 180, 185, 189, 196]
Tiempo: 0.000031s

PRUEBA: Arreglo grande (50 elementos)
Original: [151, 60, 22, 39, 45, 116, 171, 85, 175, 2]
Ordenado: [2, 22, 39, 45, 60, 85, 116, 151, 171, 175]
Tiempo: 0.000008s

PRUEBA: Casos especiales

Ya ordenado: [1, 2, 3, 4, 5] -> [1, 2, 3, 4, 5] (0.000004s)
Descendente: [5, 4, 3, 2, 1] -> [1, 2, 3, 4, 5] (0.000004s)
Con repetidos: [3, 1, 4, 1, 5, 9, 2, 6, 5, 3] -> [1, 1, 2, 3, 3, 4, 5, 5, 6, 9] (0.000009s)
```

## Conclusión

El algoritmo heapsort es una excelente opción para ordenamiento cuando se requiere un rendimiento garantizado y memoria limitada. Su implementación demuestra la eficacia de usar estructuras de datos especializadas (heaps) para resolver problemas de ordenamiento de manera eficiente.

---
Referencias

Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). Introduction to algorithms (3ra ed.). MIT Press.
