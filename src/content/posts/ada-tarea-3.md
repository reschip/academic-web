---
title: "Análisis y Diseño de Algoritmos - Tarea 3"
description: "Tercera tarea del curso de Análisis y Diseño de Algoritmos enfocada en Búsqueda del subarreglo máximo
."
pubDate: 2025-10-01
heroImage: "/~andres.cruz/images/posts/Tarea3.png"
tags: ["python", "algoritmos", "divide y venceras"]
course: "Algorithm Analysis and Design"
readTime: "5 min read"
imageType: 1
---

## Descripción de la Tarea
Programar en python y verificar el resultado del problema del subarreglo máximo.

## ¿Qué es el Algoritmo de Subarreglo Máximo?

El algoritmo de subarreglo máximo encuentra la secuencia contigua de elementos en un arreglo que tiene la suma más grande. Es un problema fundamental en análisis de algoritmos y tiene aplicaciones en finanzas, procesamiento de señales y análisis de datos.

## Funcionamiento del Algoritmo

### Estrategia Divide y Vencerás

El algoritmo divide el problema en tres casos posibles:

1. **Caso 1**: El subarreglo máximo está completamente en la mitad izquierda
2. **Caso 2**: El subarreglo máximo está completamente en la mitad derecha  
3. **Caso 3**: El subarreglo máximo cruza el punto medio

### Proceso Recursivo

1. **División**: Divide el arreglo en dos mitades
2. **Conquista**: Resuelve recursivamente cada mitad
3. **Combinación**: Encuentra el subarreglo que cruza el medio
4. **Selección**: Retorna el subarreglo con mayor suma entre los tres casos

### Función Auxiliar para Caso Cruzado

La función `encuentra_max_subarreglo_cruzando()` implementa:
- Búsqueda hacia la izquierda desde el punto medio
- Búsqueda hacia la derecha desde el punto medio
- Combinación de ambos resultados

## Análisis de Complejidad

### Complejidad Temporal

**T(n) = 2T(n/2) + O(n)**

- **T(n/2)**: Dos llamadas recursivas en mitades de tamaño n/2
- **O(n)**: Función auxiliar que cruza el medio en tiempo lineal
- **Solución**: **O(n log n)**

### Desglose de la Complejidad

- **Altura del árbol**: log₂(n) niveles
- **Trabajo por nivel**: O(n) para la función cruzada
- **Total**: O(n) × O(log n) = **O(n log n)**

### Complejidad Espacial

- **Pila de recursión**: O(log n) niveles de profundidad
- **Variables locales**: O(1) por nivel
- **Total**: **O(log n)**

## Ventajas del Enfoque Divide y Vencerás

- **Conceptualmente claro**: Fácil de entender y implementar
- **Paralelizable**: Las llamadas recursivas pueden ejecutarse en paralelo
- **Base teórica**: Demuestra principios fundamentales de algoritmos
- **Extensible**: Puede adaptarse para otros problemas similares

## Limitaciones
- **Overhead de recursión**: Llamadas a función adicionales
- **Memoria**: Usa espacio de pila para recursión

## Implementacion del Algoritmo en python

```python
import sys

def encuentra_max_subarreglo_cruzando(A, bajo, medio, alto):
    """
    Encuentra el subarreglo máximo que cruza el punto medio.
    
    Args:
        A: Lista de números
        bajo: Índice inferior
        medio: Índice medio
        alto: Índice superior
    
    Returns:
        Tupla (max_izq, max_der, suma_total)
    """
    suma_izq = float('-inf')
    suma = 0
    max_izq = medio
    
    # Buscar hacia la izquierda desde el medio
    for i in range(medio, bajo - 1, -1):
        suma += A[i]
        if suma > suma_izq:
            suma_izq = suma
            max_izq = i
    
    suma_der = float('-inf')
    suma = 0
    max_der = medio + 1
    
    # Buscar hacia la derecha desde el medio
    for j in range(medio + 1, alto + 1):
        suma += A[j]
        if suma > suma_der:
            suma_der = suma
            max_der = j
    
    return (max_izq, max_der, suma_izq + suma_der)


def encuentra_subarreglo_maximo(A, bajo, alto):
    """
    Encuentra el subarreglo máximo usando divide y vencerás.
    
    Args:
        A: Lista de números
        bajo: Índice inferior
        alto: Índice superior
    
    Returns:
        Tupla (inicio, fin, suma)
    """
    # Caso base: un solo elemento
    if bajo == alto:
        return (bajo, alto, A[bajo])
    else:
        medio = (bajo + alto) // 2
        
        # Encontrar máximo en la mitad izquierda
        (bajo_izq, alto_izq, suma_izq) = encuentra_subarreglo_maximo(A, bajo, medio)
        
        # Encontrar máximo en la mitad derecha
        (bajo_der, alto_der, suma_der) = encuentra_subarreglo_maximo(A, medio + 1, alto)
        
        # Encontrar máximo que cruza el medio
        (bajo_cruza, alto_cruza, suma_cruza) = encuentra_max_subarreglo_cruzando(A, bajo, medio, alto)
        
        # Retornar el máximo de los tres
        if suma_izq >= suma_der and suma_izq >= suma_cruza:
            return (bajo_izq, alto_izq, suma_izq)
        elif suma_der >= suma_izq and suma_der >= suma_cruza:
            return (bajo_der, alto_der, suma_der)
        else:
            return (bajo_cruza, alto_cruza, suma_cruza)


def leer_datos_archivo(nombre_archivo):
    """
    Lee datos de un archivo y retorna una lista de números.
    
    Args:
        nombre_archivo: Ruta del archivo
    
    Returns:
        Lista de números
    """
    datos = []
    try:
        with open(nombre_archivo, 'r') as archivo:
            for linea in archivo:
                linea = linea.strip()
                if linea and not linea.startswith('#'):
                    # Dividir y tomar el segundo valor (precio)
                    partes = linea.split()
                    if len(partes) >= 2:
                        try:
                            precio = float(partes[1])
                            datos.append(precio)
                        except ValueError:
                            continue
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo {nombre_archivo}")
        return []
    except Exception as e:
        print(f"Error al leer el archivo {nombre_archivo}: {e}")
        return []
    
    return datos


def main():
    """
    Función principal que ejecuta el algoritmo con el archivo especificado.
    Uso: python max_subarray.py <archivo>
    """
    if len(sys.argv) != 2:
        print("Uso: python max_subarray.py <archivo>")
        print("Ejemplo: python max_subarray.py datos1.txt")
        sys.exit(1)
    
    archivo = sys.argv[1]
    
    print(f"Procesando archivo: {archivo}\n\n")
    
    datos = leer_datos_archivo(archivo)
    
    if not datos:
        print(f"No se pudieron leer datos de {archivo}")
        sys.exit(1)
    
    print(f"Datos leídos: {datos}\n\n")
    print(f"Número de elementos: {len(datos)}\n\n")
    
    if len(datos) == 0:
        print("No hay datos para procesar\n\n")
        sys.exit(1)
    
    # Ejecutar el algoritmo
    inicio, fin, suma_maxima = encuentra_subarreglo_maximo(datos, 0, len(datos) - 1)
    
    print(f"\nResultado del subarreglo máximo:")
    print(f"Índice de inicio: {inicio}")
    print(f"Índice de fin: {fin}")
    print(f"Suma máxima: {suma_maxima}")
    print(f"Subarreglo: {datos[inicio:fin+1]}")
    
    # suma para verificar si el resultado es correcto
    suma_verificacion = sum(datos[inicio:fin+1])
    print(f"\n\nVerificación de suma: {suma_verificacion}")


if __name__ == "__main__":
    main()
```





## Doc  de max_subarray.py

El archivo `max_subarray.py` implementa el algoritmo de subarreglo máximo usando el enfoque de divide y vencerás. Para utilizarlo, sigue estos pasos:

1. **Prepara un archivo de datos**  
   El archivo debe contener los datos en formato de dos columnas:  
   - La primera columna es el índice o día (puede ser ignorada por el programa).
   - La segunda columna es el valor numérico (por ejemplo, precio).  
   Ejemplo (`datos1.txt`):

   ```bash
   0  100
   1  113
   2  110
   3   85
   4  105
   5  102
   6   86
   7   63
   8   81
   9  101
   10  94
   11 106
   12 101
   13  79
   14  94
   15  90
   16  97
   ```

2. **Ejecuta el script desde la terminal**  
   Usa el siguiente comando, reemplazando `datos1.txt` por el nombre de tu archivo de datos:

   ```bash
   python max_subarray.py datos1.txt
   ```

3. **Salida esperada**  
   El programa mostrará:
   - Los datos leídos
   - El número de elementos
   - El resultado del subarreglo máximo: índices de inicio y fin, suma máxima y el subarreglo correspondiente
   - Una verificación de la suma

   Ejemplo de salida:

   ```bash
   Procesando archivo: datos1.txt

   Datos leídos: [100.0, 113.0, 110.0, 85.0, 105.0, 105.0, 102.0, 86.0, 63.0, 81.0, 101.0, 94.0, 106.0, 101.0, 79.0, 94.0, 90.0, 97.0]

   Número de elementos: 17

   Resultado del subarreglo máximo:
   Índice de inicio: 0
   Índice de fin: 11
   Suma máxima: 1087.0
   Subarreglo: [100.0, 113.0, 110.0, 85.0, 105.0, 102.0, 86.0, 63.0, 81.0, 101.0, 94.0, 106.0]

   Verificación de suma: 1087.0
   ```
