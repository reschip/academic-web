---
title: "Análisis y Diseño de Algoritmos - Tarea 5"
description: "Quinta tarea del curso de Análisis y Diseño de Algoritmos enfocada en algoritmos aleatorizados."
pubDate: 2025-10-9
heroImage: "/~andres.cruz/images/posts/Tarea5.png"
tags: ["algoritmos", "aleatorizados", "probabilidad"]
course: "Algorithm Analysis and Design"
readTime: "1 min read"
imageType: 1
---

## Descripción de la Tarea

En esta tarea implementamos y analizamos dos algoritmos aleatorizados en Python: un enfoque clásico de contratación aleatoria y un algoritmo de tipo Las Vegas. Para cada caso mostramos la implementación, su análisis de comportamiento esperado y resultados experimentales con distribución empírica.

## Algoritmo de Contratación Aleatorizado

El problema consiste en entrevistar candidatos en orden aleatorio y contratar a un candidato solo cuando supera la mejor calificación observada hasta el momento. Este procedimiento produce un número de contrataciones aleatorio cuyo valor esperado es aproximadamente Hₙ (n-ésimo número armónico), es decir, cercano a ln(n) + γ.

### Funcionamiento

- **Entrada**: número de candidatos n.
- **Proceso**: se genera un orden aleatorio de candidatos con calificaciones únicas y se cuenta cada vez que aparece un nuevo máximo.
- **Salida**: número total de contrataciones.

### Implementacion del Algoritmo en python

```python
import random

def contratar_asistente_aleatorio(num_candidatos):

    candidatos = random.sample(range(0, 101), num_candidatos)  # calificaciones únicas 0–100
    random.shuffle(candidatos)  
    
    mejor_calificacion = -1
    contrataciones = 0

    for calificacion in candidatos:
        if calificacion > mejor_calificacion:
            mejor_calificacion = calificacion
            contrataciones += 1

    return contrataciones


if __name__ == "__main__":
    num_candidatos = 100
    
    resultado = contratar_asistente_aleatorio(num_candidatos)
    print(f"Con {num_candidatos} candidatos, se realizaron {resultado} contrataciones.")
```

### Uso y pruebas

- Ejecuta desde terminal:
```bash
python algoritmo_contratacion.py
```
- Resultado típico (n = 100): número de contrataciones alrededor de ln(100) ≈ 4.6–5.3 en promedio, con variación natural por aleatoriedad.

### Distribución empírica (simulaciones)

<div style="text-align: center; margin: 1.5rem 0;">
  <img src="/~andres.cruz/distribucion_contrataciones.png" alt="Distribución de contrataciones" style="max-width: 680px; width: 100%; border-radius: 8px;" />
</div>

La figura muestra la distribución de contrataciones tras múltiples corridas con n fijo. Se observa la concentración cerca de Hₙ, con caídas a ambos lados propias de la dispersión.

---

## Algoritmo tipo Las Vegas (búsqueda aleatoria hasta éxito)

En este enfoque, el algoritmo reordena aleatoriamente el arreglo y realiza selecciones aleatorias hasta encontrar un elemento objetivo. Es un algoritmo de tipo Las Vegas: siempre retorna una solución correcta cuando termina, pero su tiempo de ejecución es aleatorio.

Para un arreglo con proporción p del objetivo, el número de intentos sigue distribución geométrica con esperanza 1/p. Por ejemplo, si p = 0.5, el número esperado de intentos es 2.

### Funcionamiento

- **Entrada**: arreglo A con símbolos (p. ej., 'a' y 'b').
- **Proceso**: barajar A, luego seleccionar índices aleatorios hasta encontrar 'a'.
- **Salida**: cantidad de intentos hasta el primer éxito.

### Implementacion del Algoritmo en python

```python
import random

def encuentra_las_vegas(A):

    array = A.copy()
        
    random.shuffle(array)
    
    intentos = 0
    
    while True:
        # Seleccionar una posición aleatoria
        q = random.randint(0, len(array) - 1)
        intentos += 1
        
        if array[q] == 'a':
            break
    return intentos


if __name__ == "__main__":
    tamaño_arreglo = 1000
    porcentaje_a = 0.5  
    
    num_a = int(tamaño_arreglo * porcentaje_a)
    num_b = tamaño_arreglo - num_a
    
    arreglo = ['a'] * num_a + ['b'] * num_b
    
    resultado = encuentra_las_vegas(arreglo)
    print(f"Con un arreglo de {tamaño_arreglo} elementos (50% 'a', 50% 'b')")
    print(f"Se encontró 'a' después de {resultado} intentos.")
```

### Uso y pruebas

- Ejecuta desde terminal:

```bash
python algoritmo_las_vegas.py
```
- Resultado típico (p = 0.5): intentos cercanos a 2 en promedio, con distribución geométrica.

### Distribución empírica (simulaciones)

<div style="text-align: center; margin: 1.5rem 0;">
  <img src="/~andres.cruz/distribucion_las_vegas.png" alt="Distribución de intentos en Las Vegas" style="max-width: 680px; width: 100%; border-radius: 8px;" />
</div>

La figura confirma la forma geométrica esperada: alta probabilidad de éxito temprano, decreciendo exponencialmente conforme aumentan los intentos.

---

## Conclusiones

- **Contratación aleatorizada**: el número esperado de contrataciones crece lentamente (≈ Hₙ), con baja varianza relativa.
- **Las Vegas**: la esperanza de intentos depende de p (1/p), con caídas exponenciales en la cola.
- Las simulaciones concuerdan con la teoría y validan las implementaciones en Python.
