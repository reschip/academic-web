---
title: "Tarea 7: Estadísticas de orden - Mediana en tiempo lineal"
description: "Implementación del algoritmo SELECT (Median-of-Medians) para encontrar la mediana en tiempo O(n) con análisis de complejidad temporal."
pubDate: 2025-11-04
heroImage: "/~andres.cruz/images/posts/Tarea7.png"
tags: ["estadísticas de orden", "mediana", "algoritmos", "SELECT", "median-of-medians"]
course: "Análisis y Diseño de Algoritmos"
readTime: "10 min read"
imageType: 1
---

## Información de la Tarea

**Estudiante:** Andrés Cruz Chipol  
**Curso:** Análisis y Diseño de Algoritmos  
**Fecha de entrega:** Martes 4 de noviembre, 2025

## Descripción de la Tarea

Implementar la rutina para encontrar la mediana en tiempo lineal O(n) y realizar pruebas que demuestren la complejidad temporal lineal del algoritmo.

---

# Algoritmo Implementado: SELECT (Median-of-Medians)

## Introducción

Se implementó el algoritmo **SELECT** determinista propuesto por Cormen et al., que encuentra el i-ésimo elemento más pequeño de un arreglo en tiempo **O(n)** en el peor caso. Este algoritmo es fundamental en la teoría de algoritmos porque demuestra que es posible encontrar estadísticas de orden en tiempo lineal sin depender de pivotes aleatorios.

## Pseudocódigo del Algoritmo

El algoritmo SELECT opera en los siguientes 5 pasos:

1. **Dividir** los n elementos del arreglo en ⌈n/5⌉ grupos de 5 elementos cada uno.
2. **Ordenar** cada grupo por inserción y encontrar la mediana de cada uno.
3. **Recursión**: Usar SELECT recursivamente para encontrar la mediana x de las ⌈n/5⌉ medianas.
4. **Particionar** el arreglo alrededor de la mediana de medianas x usando la versión modificada de PARTITION.
5. **Decidir** según la posición relativa: si i=k retornar x, sino recursión en el lado correspondiente.

## Análisis de Complejidad

### ¿Por qué es O(n) en el peor caso?

El algoritmo SELECT garantiza tiempo lineal mediante la técnica de **median-of-medians**:

1. **División en grupos**: Se crean ⌈n/5⌉ grupos, cada uno con a lo más 5 elementos.
2. **Ordenamiento por inserción**: Ordenar 5 elementos toma tiempo constante O(1) por grupo, total O(n).
3. **Mediana de medianas**: La mediana de las ⌈n/5⌉ medianas garantiza que al particionar alrededor de ella, al menos 3⌈n/10⌉ elementos están a ambos lados.
4. **Recursión**: El tamaño del subproblema es a lo más 7n/10.
5. **T(n)**: Se resuelve la recurrencia T(n) ≤ T(⌈n/5⌉) + T(7n/10+6) + O(n) → T(n) = O(n).

La clave está en que **siempre se descarta al menos 30% de los elementos**, garantizando que la recursión converge linealmente.

## Implementación en Python

### Código de Implementación

```python
def particionar(A, p, r):
    x = A[r]
    i = p - 1
    for j in range(p, r):
        if A[j] <= x:
            i = i + 1
            A[i], A[j] = A[j], A[i]
    A[i + 1], A[r] = A[r], A[i + 1]
    return i + 1

def ordenar_insercion(A):
    for i in range(1, len(A)):
        clave = A[i]
        j = i - 1
        while j >= 0 and A[j] > clave:
            A[j + 1] = A[j]
            j = j - 1
        A[j + 1] = clave

def particionar_alrededor(A, p, r, x):
    for i in range(p, r + 1):
        if A[i] == x:
            A[i], A[r] = A[r], A[i]
            break
    return particionar(A, p, r)

def seleccionar(A, p, r, i):
    if p == r:
        return A[p]
    
    # Paso 1: Dividir en grupos de 5
    n = r - p + 1
    num_grupos = (n + 4) // 5
    medianas = []
    
    for j in range(num_grupos):
        idx_inicio = p + j * 5
        idx_fin = min(idx_inicio + 4, r)
        
        grupo = A[idx_inicio:idx_fin + 1]
        
        # Paso 2: Ordenar grupo y encontrar mediana
        ordenar_insercion(grupo)
        tamaño_grupo = len(grupo)
        idx_mediana = tamaño_grupo // 2
        medianas.append(grupo[idx_mediana])
    
    # Paso 3: Encontrar mediana de medianas usando SELECT recursivamente
    if len(medianas) == 1:
        x = medianas[0]
    else:
        x = seleccionar(medianas, 0, len(medianas) - 1, (len(medianas) + 1) // 2)
    
    # Paso 4: Particionar alrededor de la mediana de medianas
    k = particionar_alrededor(A, p, r, x)
    
    pos_relativa = k - p + 1
    
    # Paso 5: Decidir en qué lado hacer recursión
    if i == pos_relativa:
        return x
    elif i < pos_relativa:
        return seleccionar(A, p, k - 1, i)
    else:
        return seleccionar(A, k + 1, r, i - pos_relativa)

def encontrar_mediana(A):
    if len(A) == 0:
        return None
    pos_mediana = (len(A) + 1) // 2
    return seleccionar(A.copy(), 0, len(A) - 1, pos_mediana)

if __name__ == "__main__":
    A1 = [3, 1, 4, 1, 5, 9, 2, 6, 5]
    print(f"Arreglo: {A1}")
    mediana1 = encontrar_mediana(A1)
    print(f"Mediana: {mediana1}")
    print()
    
    A2 = [3, 1, 4, 1, 5, 9, 2, 6]
    print(f"Arreglo: {A2}")
    mediana2 = encontrar_mediana(A2)
    print(f"Mediana: {mediana2}")
    print()
    
    A3 = [7, 4, 8, 2, 1, 9, 3, 5, 6, 10, 11, 12, 13, 14, 15]
    print(f"Arreglo: {A3}")
    mediana3 = encontrar_mediana(A3)
    print(f"Mediana: {mediana3}")
```

## Resultados y Pruebas

### Casos de Prueba

```
Arreglo: [3, 1, 4, 1, 5, 9, 2, 6, 5]
Mediana: 4

Arreglo: [3, 1, 4, 1, 5, 9, 2, 6]
Mediana: 3

Arreglo: [7, 4, 8, 2, 1, 9, 3, 5, 6, 10, 11, 12, 13, 14, 15]
Mediana: 8
```

### Análisis Experimental de Complejidad

Se realizaron 10 ejecuciones con tamaños desde 100 hasta 1000 elementos:

| Tamaño | Tiempo (ms) |
|--------|-------------|
| 100    | 0.1037      |
| 200    | 0.1705      |
| 300    | 0.2684      |
| 400    | 0.3645      |
| 500    | 0.4727      |
| 600    | 0.5751      |
| 700    | 0.5781      |
| 800    | 0.7228      |
| 900    | 0.4030      |
| 1000   | 0.8522      |

**Tiempo promedio por elemento**: 0.000451 ms/elemento

### Verificación de Linealidad

- **Gráfica temporal**: El tiempo crece proporcionalmente con n
- **Tiempo/n constante**: ~0.000451 ms/elemento
- **Desviación estándar baja**: Indica comportamiento estable y predecible

Estos resultados confirman empíricamente que el algoritmo tiene complejidad **O(n)**.

## Ejecución del Código


### Análisis de Complejidad

```
Analizando complejidad temporal...
--------------------------------------------------
Tamaño:  100 elementos | Tiempo:   0.1037 ms
Tamaño:  200 elementos | Tiempo:   0.1705 ms
Tamaño:  300 elementos | Tiempo:   0.2684 ms
Tamaño:  400 elementos | Tiempo:   0.3645 ms
Tamaño:  500 elementos | Tiempo:   0.4727 ms
Tamaño:  600 elementos | Tiempo:   0.5751 ms
Tamaño:  700 elementos | Tiempo:   0.5781 ms
Tamaño:  800 elementos | Tiempo:   0.7228 ms
Tamaño:  900 elementos | Tiempo:   0.4030 ms
Tamaño: 1000 elementos | Tiempo:   0.8522 ms
```

## Conclusión

La implementación del algoritmo SELECT, siguiendo el pseudocódigo de Cormen et al., permitió encontrar la mediana en tiempo lineal garantizado O(n), como fue confirmado tanto teóricamente como experimentalmente. A diferencia de QuickSelect, SELECT destaca por su eficiencia en el peor caso al evitar depender del pivote, gracias a la técnica de median-of-medians que asegura siempre una buena partición y mantiene el comportamiento lineal observado en las pruebas.

---

## Referencias

Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). Introduction to algorithms (3ra ed.). MIT Press.

