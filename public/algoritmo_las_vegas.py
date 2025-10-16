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
