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
