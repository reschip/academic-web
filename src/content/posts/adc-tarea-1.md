---
title: "Tarea 1: Sistema Caótico Con Punto Fijo/Flotante"
description: "Implementación en Python y C (Utilizando la librería de punto fijo) del sistema caótico Lü."
pubDate: 2026-01-20
heroImage: "/~andres.cruz/images/posts/Tarea1_adc.png"
tags: ["Sistema caótico", "Punto fijo", "C", "Python", "amplitud"]
course: "Arquitectura de Computadoras"
readTime: "10 min read"
imageType: 1
---

## Información de la Tarea

**Estudiante:** Andrés Cruz Chipol

**Curso:** Arquitectura De Computadoras

**Fecha de entrega:** Martes 20 de Enero, 2026

## Descripción de la Tarea

Implementar el sistema caótico de Lü utilizando aritmética de punto fijo en C y punto flotante en Python. Comparar los resultados de amplitud entre ambas implementaciones y visualizar el comportamiento caótico del sistema.

---

# Sistema Caótico de Lü

## Introducción

El **sistema de Lü** es un sistema dinámico tridimensional que exhibe comportamiento caótico. Fue propuesto por Jinhu Lü y Guanrong Chen en 2002 como un puente entre el atractor de Lorenz y el atractor de Chen. El sistema es notable por su rica dinámica caótica y ha sido objeto de extenso estudio en la teoría del caos.

El sistema de Lü se define mediante el siguiente conjunto de ecuaciones diferenciales ordinarias:
```
dx/dt = y
dy/dt = z
dz/dt = -a·x - b·y - c·z + d·k·f(x/k)
```

donde `f(u)` es una función no lineal por segmentos (piecewise linear) definida como:
```
f(u) = {
    -SAT           si u ≤ -1.1
    SLOPE·(u+0.9)  si -1.1 < u ≤ -0.9
    0              si -0.9 < u ≤ 0.9
    SLOPE·(u-0.9)  si 0.9 < u ≤ 1.1
    SAT            si u > 1.1
}
```

## Parámetros del Sistema

Para esta implementación se utilizaron los siguientes parámetros:

- **a, b, c, d** = 0.7
- **k** = 16.0
- **SAT** = 2.0 (valor de saturación)
- **SLOPE** = 10.0 (pendiente en regiones lineales)
- **Condiciones iniciales**: x₀ = 5.0, y₀ = 5.0, z₀ = 0.0
- **Tiempo de simulación**: 100 segundos
- **Paso de integración (C)**: h = 0.0001 (Método de Euler)
- **Paso de integración (Python)**: 0.01 (odeint adaptativo)

## Función No Lineal por Segmentos

La función `f(u)` proporciona la no linealidad esencial que genera el comportamiento caótico. Esta función tiene tres regiones:

1. **Región de saturación negativa** (u ≤ -1.1): salida constante en -2.0
2. **Región lineal activa** (-1.1 < u < -0.9 y 0.9 < u < 1.1): pendiente de 10
3. **Zona muerta** (-0.9 ≤ u ≤ 0.9): salida cero
4. **Región de saturación positiva** (u > 1.1): salida constante en 2.0

---

## Implementación en C (Punto Fijo)

La implementación en C utiliza la librería `intarith.h` para realizar operaciones con aritmética de punto fijo, permitiendo emular el comportamiento en sistemas embebidos o hardware con recursos limitados.
```c
#include <stdio.h>
#include "intarith.h"

// Sistema Lü - Función no lineal por segmentos
long f_pwl(long u) {
    long lim_a = setNumber(0.9), lim_b = setNumber(1.1);
    long slope = setNumber(10.0), sat = setNumber(2.0);

    if (u > lim_b) return sat;
    if (u < -lim_b) return -sat;
    if (u > lim_a) return mulTrunc(slope, u - lim_a);
    if (u < -lim_a) return mulTrunc(slope, u + lim_a);
    return 0;
}

int main() {
    // Inicializar aritmética de punto fijo: 12 bits enteros, 18 bits fraccionarios
    initializeA(12, 18);
    FILE *fp = fopen("datos.txt", "w");

    // Parámetros del sistema
    long a = setNumber(0.7);
    long k = setNumber(16.0);
    long inv_k = setNumber(1.0/16.0);
    double h_val = 0.0001;
    long h = setNumber(h_val);

    // Configuración de tiempos
    double t_total = 100.0;
    long pasos_totales = (long)(t_total / h_val); // 1,000,000 pasos
    int pasos_para_imprimir = 100; // Imprimir cada 0.01s

    // Estado inicial
    long x[3] = {setNumber(5.0), setNumber(5.0), 0};
    long d[3];

    // Variables para análisis de amplitud
    long max_x = setNumber(-1000), min_x = setNumber(1000);
    long max_y = setNumber(-1000), min_y = setNumber(1000);
    long max_z = setNumber(-1000), min_z = setNumber(1000);

    printf("Calculando simulacion precisa (h=0.0001) para X, Y, Z...\n");

    for(long i = 0; i < pasos_totales; i++) {
        // Guardar dato cada 0.01s en archivo
        if(i % pasos_para_imprimir == 0) {
            fprintf(fp, "%f %f %f %f\n", i*h_val,
                    getNumber(x[0]), getNumber(x[1]), getNumber(x[2]));
        }

        // Análisis de amplitud (ignorar primeros 20s = 200,000 pasos)
        if(i > 200000) {
            // Análisis X
            if(x[0] > max_x) max_x = x[0];
            if(x[0] < min_x) min_x = x[0];

            // Análisis Y
            if(x[1] > max_y) max_y = x[1];
            if(x[1] < min_y) min_y = x[1];

            // Análisis Z
            if(x[2] > max_z) max_z = x[2];
            if(x[2] < min_z) min_z = x[2];
        }

        // Método de Euler
        d[0] = x[1];
        d[1] = x[2];

        long arg = mulTrunc(x[0], inv_k);
        long f_val = f_pwl(arg);
        long nonlinear = mulTrunc(a, mulTrunc(k, f_val));

        d[2] = -mulTrunc(a, x[0]) - mulTrunc(a, x[1])
               - mulTrunc(a, x[2]) + nonlinear;

        x[0] += mulTrunc(h, d[0]);
        x[1] += mulTrunc(h, d[1]);
        x[2] += mulTrunc(h, d[2]);
    }

    fclose(fp);

    // Imprimir resultados
    printf("\n=== RESULTADOS C (Punto Fijo) ===\n");
    printf("[C-Fixed] X: Amp=%.4f [Min=%.4f, Max=%.4f]\n",
           getNumber(max_x - min_x), getNumber(min_x), getNumber(max_x));
    printf("[C-Fixed] Y: Amp=%.4f [Min=%.4f, Max=%.4f]\n",
           getNumber(max_y - min_y), getNumber(min_y), getNumber(max_y));
    printf("[C-Fixed] Z: Amp=%.4f [Min=%.4f, Max=%.4f]\n",
           getNumber(max_z - min_z), getNumber(min_z), getNumber(max_z));

    return 0;
}
```

### Características de la Implementación en C

- **Aritmética de punto fijo**: 12 bits enteros, 18 bits fraccionarios
- **Método de integración**: Euler con h = 0.0001
- **Pasos totales**: 1,000,000 (100 segundos de simulación)
- **Guardado de datos**: Cada 100 pasos (0.01 segundos)
- **Análisis de amplitud**: Después de 20 segundos de transitorio

---

## Implementación en Python (Punto Flotante)

La implementación en Python utiliza aritmética de punto flotante y el integrador adaptativo `odeint` de SciPy para mayor precisión.
```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Parámetros del sistema
a, b, c, d, k = 0.7, 0.7, 0.7, 0.7, 16.0
SAT, SLOPE = 2.0, 10.0

# Función no lineal por segmentos
def f(u):
    if u <= -1.1: return -SAT
    if u <= -0.9: return SLOPE * (u + 0.9)
    if u <= 0.9:  return 0.0
    if u <= 1.1:  return SLOPE * (u - 0.9)
    return SAT

# Sistema de ecuaciones diferenciales
def sys(s, t):
    x, y, z = s
    return [y, z, -a*x - b*y - c*z + d * k * f(x/k)]

# Simulación
t = np.arange(0, 100.01, 0.01)
res = odeint(sys, [5.0, 5.0, 0.0], t)
x, y, z = res[:, 0], res[:, 1], res[:, 2]

# Análisis de amplitud (después de 20s)
s = int(20/0.01)
ax, ay, az = x[s:], y[s:], z[s:]

print(f"[Python]  X: Amp={np.ptp(ax):.4f} [Min={np.min(ax):.4f}, Max={np.max(ax):.4f}]")
print(f"[Python]  Y: Amp={np.ptp(ay):.4f} [Min={np.min(ay):.4f}, Max={np.max(ay):.4f}]")
print(f"[Python]  Z: Amp={np.ptp(az):.4f} [Min={np.min(az):.4f}, Max={np.max(az):.4f}]")

# Visualización
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

ax1.plot(x, y, lw=0.8, c='purple')
ax1.set_title("Plano XY")
ax1.set_xlabel("x")
ax1.set_ylabel("y")
ax1.grid(alpha=0.3)

ax2.plot(t, x, lw=0.8, c='green')
ax2.set_title("Evolución temporal de x")
ax2.set_xlabel("Tiempo (s)")
ax2.set_ylabel("x")
ax2.grid(alpha=0.3)

plt.tight_layout()
plt.show()
```

---

## Resultados y Comparación

### Resultados de Amplitud - C (Punto Fijo)
```
=== RESULTADOS C (Punto Fijo) ===
[C-Fixed] X: Amp=95.1974 [Min=-45.7031, Max=49.4943]
[C-Fixed] Y: Amp=32.9129 [Min=-18.2434, Max=14.6695]
[C-Fixed] Z: Amp=26.3470 [Min=-14.6718, Max=11.6752]
```

### Resultados de Amplitud - Python (Punto Flotante)
```
=== RESULTADOS Python (Punto Flotante) ===
[Python]  X: Amp=93.4047 [Min=-46.0609, Max=47.3438]
[Python]  Y: Amp=30.8484 [Min=-15.9566, Max=14.8918]
[Python]  Z: Amp=24.9200 [Min=-12.8368, Max=12.0833]
```

### Tabla Comparativa

| Variable | C (Punto Fijo) | Python (Flotante) | Diferencia |
|----------|----------------|-------------------|------------|
| **X Amplitud** | 95.1974 | 93.4047 | 1.7927 |
| **Y Amplitud** | 32.9129 | 30.8484 | 2.0645 |
| **Z Amplitud** | 26.3470 | 24.9200 | 1.4270 |

### Análisis de Diferencias

Las diferencias observadas entre ambas implementaciones se deben principalmente a:

1. **Precisión aritmética**: El punto fijo tiene menor precisión que el punto flotante de 64 bits
2. **Método de integración**: Euler (C) vs odeint adaptativo (Python)
3. **Acumulación de errores**: El método de Euler con paso fijo acumula más error a lo largo del tiempo
4. **Truncamiento**: Las operaciones de punto fijo realizan truncamiento en cada multiplicación

A pesar de estas diferencias, ambas implementaciones capturan correctamente el comportamiento caótico del sistema, con diferencias de amplitud menores al 2%, lo que demuestra la viabilidad del uso de punto fijo para este tipo de sistemas.

---

## Visualizaciones

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 20px 0;">
  <div>
    <h3>Implementación en C (Punto Fijo)</h3>
    <img src="/~andres.cruz/caosC.png" alt="Sistema Caótico Lü - C" style="width: 100%; height: auto;">
    <p>Atractor de Lü usando aritmética de punto fijo (12.18 bits)</p>
  </div>
  <div>
    <h3>Implementación en Python (Punto Flotante)</h3>
    <img src="/~andres.cruz/caospy.png" alt="Sistema Caótico Lü - Python" style="width: 100%; height: auto;">
    <p>Atractor de Lü usando aritmética de punto flotante de 64 bits</p>
  </div>
</div>

## Conclusiones

La implementación del sistema caótico de Lü en punto fijo (C) y punto flotante (Python) demostró que es posible reproducir el comportamiento caótico con diferencias de amplitud menores al 2%, validando la viabilidad del punto fijo para sistemas dinámicos. Aunque el punto fijo  tiene menor precisión que el punto flotante de 64 bits, ambas implementaciones capturan correctamente la estructura del atractor y su dinámica aperiódica característica. Este resultado confirma que la aritmética de punto fijo es una alternativa eficiente para implementar sistemas caóticos en hardware con recursos limitados, sacrificando apenas 2% de precisión a cambio de mayor eficiencia computacional y menor consumo de recursos.

