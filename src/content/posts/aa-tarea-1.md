---
title: "Tarea 1: Regresión lineal"
description: "Implementación en Python de la Regresion Lineal, Errores RMS, R al cuadrado de 1 a 10 Grados."
pubDate: 2026-01-23
heroImage: "/~andres.cruz/images/posts/Tarea1_aa.png"
tags: ["ML", "Regresión Lineal", "RMS", "Python", "sklearn", "matplotlib"]
course: "Aprendizaje Automático"
readTime: "7 min read"
imageType: 1
---

## Información de la Tarea

**Estudiante:** Andrés Cruz Chipol

**Curso:** Aprendizaje Automático

**Fecha de entrega:** Martes 22 de Enero, 2026

## Descripción de la Tarea

Ajustar estos datos a polinomios de grado n = 1, ..., 10.
Mostrar una tabla con los valores de los coeficientes obtenidos, las gráficas de los datos contra el modelo y una última tabla de n contra la medida del error RMS y el valor del R^2

---
# Regresión Lineal
Se trabajó con un conjunto de 14 puntos de datos que muestran una relación no lineal entre las variables x e y:

```
0.0 0.16243453636632418
0.483321946706122 0.403547530678761
0.966643893412244 0.7701666906673108
1.449965840118366 0.8854120118824369
1.933287786824488 1.0215570056178827
2.41660973353061 0.4329687885527672
2.899931680236732 0.4137968407092061
3.383253626942854 -0.31543635437706774
3.866575573648976 -0.6312187486350851
4.349897520355098 -0.9599532802331557
4.83321946706122 -0.8464980803935567
5.316541413767342 -1.028997936843422
5.799863360473464 -0.49696489244511993
6.283185307179586 -0.03840543546684181
```

## Codigo
Esta es la implementacion completa del codigo:

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model

data = np.loadtxt("datos.csv")

x = data[:, 0]
y = data[:, 1]

# Imprimir Grados
data_extend = x.reshape(-1, 1)

print("\nMatriz de Grados")
for i in range(2, 11):
    data_extend = np.column_stack((data_extend, x**i))

for fila in data_extend:
    for valor in fila:
        print(f"{valor:12.2f}", end="")
    print()

fig, axes = plt.subplots(2, 5, figsize=(18, 7))
axes = axes.flatten()

vx = np.linspace(x.min(), x.max(), 300)

grados = []
rms_list = []
r2_list = []
coef_por_grado = []
interceptos = []

for grado in range(1, 11):

    regresor = linear_model.LinearRegression()
    regresor.fit(data_extend[:, :grado], y)

    coef_por_grado.append(regresor.coef_)
    interceptos.append(regresor.intercept_)

    y_hat = regresor.intercept_
    for i in range(grado):
        y_hat += regresor.coef_[i] * x**(i + 1)

    rms = np.sqrt(np.mean((y - y_hat) ** 2))

    ss_res = np.sum((y - y_hat) ** 2)
    ss_tot = np.sum((y - y.mean()) ** 2)
    r2 = 1 - ss_res / ss_tot

    grados.append(grado)
    rms_list.append(rms)
    r2_list.append(r2)

    vy = regresor.intercept_
    for i in range(grado):
        vy += regresor.coef_[i] * vx**(i + 1)

    ax = axes[grado - 1]
    ax.scatter(x, y, s=20, c="royalblue")
    ax.plot(vx, vy, color="#FF5733")
    ax.set_title(f"Grado {grado}")
    ax.set_xlabel("x")
    ax.set_ylabel("y")

plt.tight_layout()
plt.show()

print("\nCoeficientes por grado")
print("Grado | Intercepto | Coeficientes")

for i in range(len(grados)):
    coef_str = ", ".join(f"{c:.6f}" for c in coef_por_grado[i])
    print(f"{grados[i]:5d} | {interceptos[i]:10.6f} | [{coef_str}]")

print("\nErrores")
print("Grado |    RMS    |    R^2")

for i in range(len(grados)):
    print(f"{grados[i]:5d} | {rms_list[i]:8.4f} | {r2_list[i]:8.4f}")

fig, ax1 = plt.subplots()

ax1.plot(grados, rms_list, marker="D", color="tab:blue", label="RMS")
ax1.set_xlabel("Grado del polinomio (n)")
ax1.set_ylabel("Error RMS", color="tab:blue")
ax1.tick_params(axis="y", labelcolor="tab:blue")
ax1.grid(True)

ax2 = ax1.twinx()
ax2.plot(grados, r2_list, marker="8", color="tab:red", label="R^2")
ax2.set_ylabel("R^2", color="tab:red")
ax2.tick_params(axis="y", labelcolor="tab:red")
ax2.set_ylim(0, 1.05)

plt.title("RMS - R^2 vs Grado del Polinomio")
plt.show()



```

### Fórmulas Utilizadas

**Error RMS:**
```
RMS = √(Σ(yi - ŷi)² / n)
```
donde yi son los valores reales, ŷi son los valores predichos, y n es el número de puntos.

**Coeficiente R²:**
```
R² = 1 - (SS_res / SS_tot)
donde:
  SS_res = Σ(yi - ŷi)²  (suma de cuadrados residuales)
  SS_tot = Σ(yi - ȳ)²   (suma de cuadrados totales)
```

Un R² cercano a 1 indica un mejor ajuste del modelo a los datos.

---

## Resultados

De los datos de prueba, generé "manualmente" con numpy una matriz de características, para luego iterar sobre ella misma.
A continuacion se muestran las tablas que imprime el programa.

```python
for i in range(2, 11):
    data_extend = np.column_stack((data_extend, x**i))

```

La matriz de características muestra los valores de x elevados a diferentes potencias para cada punto de datos.
Con esta matriz podemos ajustar nuestras regresioines, El programa imprime la Matriz(La matriz esta formateada para que se vea bien pero mantiene los datos reales con su punto flotante real.):

```python
for fila in data_extend:
    for valor in fila:
        print(f"{valor:12.2f}", end="")
    print()

```

```
Matriz de Grados
0.00        0.00        0.00        0.00        0.00        0.00        0.00        0.00        0.00        0.00
0.48        0.23        0.11        0.05        0.03        0.01        0.01        0.00        0.00        0.00
0.97        0.93        0.90        0.87        0.84        0.82        0.79        0.76        0.74        0.71
1.45        2.10        3.05        4.42        6.41        9.29       13.47       19.54       28.33       41.08
1.93        3.74        7.23       13.97       27.01       52.21      100.94      195.15      377.28      729.40
2.42        5.84       14.11       34.11       82.42      199.18      481.33     1163.19     2810.99     6793.06
2.90        8.41       24.39       70.72      205.09      594.74     1724.70     5001.52    14504.07    42060.81
3.38       11.45       38.73      131.02      443.27     1499.71     5073.90    17166.29    58077.91   196492.31
3.87       14.95       57.81      223.51      864.24     3341.64    12920.68    49958.80   193169.49   746904.42
4.35       18.92       82.31      358.03     1557.38     6774.45    29468.17   128183.52   557585.19  2425438.43
4.83       23.36      112.90      545.69     2637.44    12747.33    61610.62   297777.67  1439224.83  6956089.49
5.32       28.27      150.28      798.94     4247.62    22582.67   120061.68   638312.88  3393616.88 18042304.66
5.80       33.64      195.10     1131.54     6562.79    38063.31   220762.01  1280389.48  7426084.02 43070272.65
6.28       39.48      248.05     1558.55     9792.63    61528.91   386597.53  2429063.94 15262258.86 95895600.62
```

## Coeficientes Obtenidos

Para cada grado de polinomio, se obtuvieron los siguientes coeficientes:
```
Coeficientes por grado
Grado | Intercepto | Coeficientes
    1 |   0.764626 | [-0.248563]
    2 |   0.776337 | [-0.260678, 0.001928]
    3 |   0.001496 | [1.564829, -0.751925, 0.079986]
    4 |   0.057007 | [1.300315, -0.546002, 0.027839, 0.004150]
    5 |   0.145077 | [0.468313, 0.513630, -0.443096, 0.089736, -0.005449]
    6 |   0.161147 | [0.152352, 1.115621, -0.852565, 0.215370, -0.023220, 0.000943]
    7 |   0.162843 | [0.074743, 1.321316, -1.049090, 0.304478, -0.043981, 0.003344, -0.000109]
    8 |   0.160143 | [0.417721, 0.140609, 0.435088, -0.611988, 0.264666, -0.054456, 0.005542, -0.000225]
    9 |   0.164001 | [-1.304670, 7.362527, -10.869690, 8.342425, -3.764026, 1.019322, -0.162270, 0.013978, -0.000502]
   10 |   0.161511 | [3.927505, -17.968691, 36.261081, -37.310379, 22.177689, -8.094801, 1.841696, -0.254431, 0.019517, -0.000637]

```


## Análisis de Errores
También se imprime la siguiente tabla.

```
Errores
Grado |    RMS    |    R^2
    1 |   0.4724 |   0.5124
    2 |   0.4724 |   0.5125
    3 |   0.1387 |   0.9580
    4 |   0.1333 |   0.9612
    5 |   0.1068 |   0.9751
    6 |   0.1046 |   0.9761
    7 |   0.1046 |   0.9761
    8 |   0.1041 |   0.9763
    9 |   0.0997 |   0.9783
   10 |   0.0889 |   0.9827

```

### Análisis

**Salto Crítico de Grado 2 a 3**

El cambio más significativo ocurre entre los polinomios de grado 2 y 3:
- Reducción del error RMS: de 0.4724 a 0.1387
- Aumento del R²: de 0.5125 a 0.9580

La relación fundamental entre x e y es  no lineal y requiere al menos términos cúbicos para ser capturada adecuadamente.

**Punto Óptimo: Grado 5-6**

Los polinomios de grado 5 o 6 representan el mejor equilibrio entre precisión y complejidad:
- R² > 0.975 (explican más del 97.5% de la varianza)
- RMS < 0.11 (error promedio menor a 0.11 unidades)
- Coeficientes razonables
- Menos parámetros que grados superiores, evitando el sobreajuste.

**Sobreajuste en Grados Altos**

Los grados 9 y 10 muestran:
- Coeficientes muy grandes
- Mejoras marginales en métricas de error
- Complejidad innecesaria del modelo


### Visualización de Graficos de Resultados
El programa Tambien despliega todas las graficas que se iteraron.

<img src="/~andres.cruz/RegresionGradosRL.png" alt="Regresión Polinomial Grados 1-10" style="width: 100%; max-width: 1200px; height: auto; display: block; margin: 20px auto;">

Las gráficas ilustran claramente cómo cada polinomio se ajusta a los datos experimentales:

- **Grados 1-2**: Modelos inadecuados que muestran solo una línea recta, incapaces de capturar la estructura  de los datos.

- **Grado 3**: Primera aproximación razonable que captura la curvatura general y el cambio de dirección en los datos. Se observa una mejora en el seguimiento de los puntos.

- **Grados 4-6**: Los modelos siguen la tendencia de los datos muy de cerca, pasando por las regiones de mayor densidad de puntos y capturando las oscilaciones principales.

- **Grados 7-10**: Ajuste casi perfecto a los puntos de datos. Se puede observar como se sobreajuste cuando los grados van aumentando.

### Gráfica de Evolución de Errores

![Evolución de Errores RMS y R²](/~andres.cruz/erroresRL.png)

Esta gráfica es fundamental para entender el compromiso entre complejidad del modelo y precisión:

**RMS:**
- Decae exponencialmente, especialmente hasta el grado 5
- El mayor cambio (pendiente más pronunciada) ocurre entre grados 2 y 3
- A partir del grado 6, la curva se aplana, indicando mejoras marginales

**R²:**
- Crece asintóticamente hacia 1.0 (ajuste perfecto)
- Muestra un salto dramático entre grados 2 y 3
- Valores por encima de 0.975 generalmente se consideran excelentes ajustes

**Punto de Inflexión:**
- El grado 3 marca el cambio más significativo en ambas curvas
- Es el grado mínimo recomendado para estos datos

---

## Conclusiones

Los datos muestran una relación no lineal entre las variables, ya que el comportamiento cambia de dirección y presenta oscilaciones, por lo que un modelo lineal simple no es suficiente para describirlo correctamente. Aunque aumentar la complejidad del modelo mejora ligeramente los resultados, elevar el grado del polinomio más allá de 6 aporta beneficios mínimos: no hay mejora apreciable al pasar de 6 a 7 y, de 7 a 10, la reducción del error es muy pequeña. En contraste, este aumento de complejidad incrementa el riesgo de sobreajuste, haciendo que el modelo sea menos robusto sin un beneficio real significativo.
