import random
from arbol_rojo_negro import ArbolRojoNegro
"""
Árbol Rojo-Negro con Graphviz
- Inserción con entradas aleatorias
- Borrado aleatorio de nodos
- Visualización gráfica con colores
"""
def main():
    print("DEMOSTRACION DE ARBOL ROJO-NEGRO")  
    # Generar las entradas
    entradas = [
        random.sample(range(1, 50), 8),
        random.sample(range(1, 50), 8),
        random.sample(range(1, 50), 8)
    ]
    
    print("\nPASO 2: INSERCION CON ENTRADAS ALEATORIAS")
    
    arboles = []
    for i, entrada in enumerate(entradas, 1):
        print(f"\nÁrbol {i} - Entrada: {entrada}")
        arbol = ArbolRojoNegro()
        for valor in entrada:
            arbol.insertar(valor)
        
        arbol.generar_imagen(f"arbol_{i}_insercion", f"Árbol {i} - Inserción: {entrada}")
        arboles.append((arbol, entrada))
    
    print("\nPASO 3: BORRADO ALEATORIO")
    
    for i, (arbol, entrada) in enumerate(arboles, 1):
        nodo_a_borrar = random.choice(entrada)
        print(f"\nÁrbol {i} - Borrando: {nodo_a_borrar}")
        
        arbol.borrar_por_llave(nodo_a_borrar)
        
        nodos_restantes = sorted([n for n in entrada if n != nodo_a_borrar])
        
        arbol.generar_imagen(f"arbol_{i}_borrado", f"Árbol {i} - Después de borrar {nodo_a_borrar}")
        print(f"Nodos restantes: {nodos_restantes}")

if __name__ == "__main__":
    main()
