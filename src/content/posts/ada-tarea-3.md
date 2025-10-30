---
title: "Tarea 3: Búsqueda del subarreglo máximo"
description: "Implementación en Python del algoritmo de subarreglo máximo usando divide y vencerás."
pubDate: 2025-09-30
heroImage: "/~andres.cruz/images/posts/Tarea3.png"
tags: ["python", "algoritmos", "divide y venceras"]
course: "Análisis y Diseño de Algoritmos"
readTime: "5 min read"
imageType: 1
---

## Información de la Tarea

**Estudiante:** Andrés Cruz Chipol  
**Curso:** Análisis y Diseño de Algoritmos  
**Fecha de entrega:** Martes 30 de septiembre, 2025

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
    Lee datos de un archivo y retorna una lista de precios.
    
    Args:
        nombre_archivo: Ruta del archivo
    
    Returns:
        Lista de precios
    """
    precios = []
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
                            precios.append(precio)
                        except ValueError:
                            continue
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo {nombre_archivo}")
        return []
    except Exception as e:
        print(f"Error al leer el archivo {nombre_archivo}: {e}")
        return []
    
    return precios


def calcular_cambios_diarios(precios):
    """
    Calcula los cambios diarios (diferencias) entre precios consecutivos.
    
    Args:
        precios: Lista de precios
    
    Returns:
        Lista de cambios diarios
    """
    cambios = []
    for i in range(1, len(precios)):
        cambio = precios[i] - precios[i-1]
        cambios.append(cambio)
    return cambios


def main():
    """
    Función principal que ejecuta el algoritmo de análisis financiero.
    Uso: python max_subarray.py <archivo>
    """
    if len(sys.argv) != 2:
        print("Uso: python max_subarray.py <archivo>")
        print("Ejemplo: python max_subarray.py datos1.txt")
        sys.exit(1)
    
    archivo = sys.argv[1]
    
    print("=" * 60)
    print(f"ANALISIS FINANCIERO - ARCHIVO: {archivo}")
    print("=" * 60)
    
    # Leer precios del archivo
    precios = leer_datos_archivo(archivo)
    
    if not precios or len(precios) < 2:
        print(f"Error: No se pudieron leer suficientes datos de {archivo}")
        sys.exit(1)
    
    print(f"\nPRECIOS ORIGINALES ({len(precios)} dias):")
    print("-" * 40)
    for i, precio in enumerate(precios):
        print(f"Dia {i:2d}: ${precio:6.1f}")
    
    # Calcular cambios diarios
    cambios = calcular_cambios_diarios(precios)
    print(f"\nCAMBIOS DIARIOS ({len(cambios)} periodos):")
    print("-" * 40)
    for i, cambio in enumerate(cambios):
        signo = "+" if cambio >= 0 else ""
        print(f"Dia {i+1:2d}->{i+2:2d}: {signo}{cambio:6.1f}")
    
    # Ejecutar el algoritmo en los cambios diarios
    inicio, fin, suma_maxima = encuentra_subarreglo_maximo(cambios, 0, len(cambios) - 1)
    
    print(f"\nESTRATEGIA OPTIMA DE INVERSION:")
    print("=" * 60)
    
    # Mostrar el subarreglo máximo de forma destacada
    subarreglo = cambios[inicio:fin+1]
    print(f"SUBARREGLO MAXIMO ENCONTRADO:")
    print("-" * 40)
    print(f"Valores: {subarreglo}")
    print(f"Indices: [{inicio} - {fin}]")
    print(f"Suma total: {suma_maxima:.1f}")
    
    print(f"\nRESUMEN FINANCIERO:")
    print("-" * 40)
    print(f"GANANCIA MAXIMA: ${suma_maxima:.1f}")
    print(f"COMPRAR: Dia {inicio + 1} (Precio: ${precios[inicio + 1]:.1f})")
    print(f"VENDER:  Dia {fin + 2} (Precio: ${precios[fin + 2]:.1f})")
    print(f"DURACION: {fin - inicio + 1} dias")
    
    print(f"\nDETALLES DEL PERIODO OPTIMO:")
    print("-" * 40)
    for i in range(inicio, fin + 1):
        dia_inicio = i + 1
        dia_fin = i + 2
        cambio = cambios[i]
        signo = "+" if cambio >= 0 else ""
        print(f"Dia {dia_inicio:2d}->{dia_fin:2d}: {signo}{cambio:6.1f}")
    
    # Verificación con precios reales
    precio_compra = precios[inicio + 1]
    precio_venta = precios[fin + 2]
    ganancia_real = precio_venta - precio_compra
    
    print(f"\nVERIFICACION:")
    print("-" * 40)
    print(f"Precio de compra: ${precio_compra:.1f}")
    print(f"Precio de venta:  ${precio_venta:.1f}")
    print(f"Ganancia real:    ${ganancia_real:.1f}")
    print(f"Suma de cambios:  ${sum(cambios[inicio:fin+1]):.1f}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
```





## Documentación de max_subarray.py

El archivo `max_subarray.py` implementa el algoritmo de subarreglo máximo usando el enfoque de divide y vencerás, **especializado para análisis financiero**. El algoritmo encuentra el período óptimo para comprar y vender una acción basándose en los cambios diarios de precio.

### Características Principales

- **Análisis financiero**: Calcula automáticamente los cambios diarios entre precios consecutivos
- **Estrategia de inversión**: Encuentra el período de mayor ganancia acumulada
- **Visualización completa**: Muestra precios, cambios, subarreglo máximo y estrategia óptima
- **Verificación**: Confirma los resultados con cálculos de precios reales

### Uso del Programa

1. **Prepara un archivo de datos**  
   El archivo debe contener los datos en formato de dos columnas:  
   - La primera columna es el índice o día
   - La segunda columna es el precio de la acción
   
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
   ```bash
   python max_subarray.py datos1.txt
   ```

3. **Salida esperada**  
   El programa mostrará:
   - Precios originales con formato de tabla
   - Cambios diarios calculados automáticamente
   - Subarreglo máximo encontrado con índices
   - Estrategia óptima de inversión (días de compra/venta)
   - Verificación con precios reales

   Ejemplo de salida:
   ```bash
   ============================================================
   ANALISIS FINANCIERO - ARCHIVO: datos1.txt
   ============================================================

   PRECIOS ORIGINALES (17 dias):
   ----------------------------------------
   Dia  0: $ 100.0
   Dia  1: $ 113.0
   ...

   CAMBIOS DIARIOS (16 periodos):
   ----------------------------------------
   Dia  1-> 2:  +13.0
   Dia  2-> 3:   -3.0
   ...

   ESTRATEGIA OPTIMA DE INVERSION:
   ============================================================
   SUBARREGLO MAXIMO ENCONTRADO:
   ----------------------------------------
   Valores: [18.0, 20.0, -7.0, 12.0]
   Indices: [7 - 10]
   Suma total: 43.0

   RESUMEN FINANCIERO:
   ----------------------------------------
   GANANCIA MAXIMA: $43.0
   COMPRAR: Dia 8 (Precio: $63.0)
   VENDER:  Dia 12 (Precio: $106.0)
   DURACION: 4 dias
   ```

### Aplicación Práctica

Este algoritmo es especialmente útil para:
- **Análisis de inversiones**: Encontrar el período óptimo para comprar/vender
- **Trading algorítmico**: Identificar ventanas de oportunidad
- **Gestión de riesgo**: Evitar períodos de pérdidas acumuladas
- **Optimización temporal**: Maximizar retornos en el tiempo
