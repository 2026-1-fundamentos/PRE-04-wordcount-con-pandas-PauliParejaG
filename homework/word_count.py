"""Taller evaluable"""

import glob
import os
import string

def load_input(input_directory):
    """Lee las líneas de texto de todos los archivos en el directorio de entrada."""
    sequence = []
    files = glob.glob(f"{input_directory}/*")
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            for line in f:
                sequence.append((file, line))
    return sequence

def mapper(sequence):
    """Fase de Mapper: Pasa a minúsculas, quita puntuación y genera pares (palabra, 1)."""
    pairs = []
    for _, line in sequence:
        line = line.lower()
        line = line.translate(str.maketrans("", "", string.punctuation))
        words = line.split()
        for word in words:
            pairs.append((word, 1))
    return pairs

def reducer(pairs_sequence):
    """Fase de Reducer: Suma las frecuencias de las palabras agrupadas."""
    result = []
    for key, value in pairs_sequence:
        if result and result[-1][0] == key:
            result[-1] = (key, result[-1][1] + value)
        else:
            result.append((key, value))
    return result

def save_output(output_directory, sequence):
    """Guarda los resultados separados por tabulador y crea el archivo de éxito."""
    # Limpiar el directorio si ya existe para evitar errores
    if os.path.exists(output_directory):
        for file in glob.glob(f"{output_directory}/*"):
            os.remove(file)
        os.rmdir(output_directory)
    os.makedirs(output_directory)
    
    # Escribir el archivo part-00000
    with open(os.path.join(output_directory, "part-00000"), "w", encoding="utf-8") as f:
        for key, value in sequence:
            f.write(f"{key}\t{value}\n")
            
    # Escribir el archivo bandera _SUCCESS
    with open(os.path.join(output_directory, "_SUCCESS"), "w", encoding="utf-8") as f:
        f.write("")

#
# Escriba la función job, la cual orquesta las funciones anteriores.
#
def run_job(input_directory, output_directory):
    """Job"""
    # 1. Cargar datos
    sequence = load_input(input_directory)
    
    # 2. Fase de Map
    pairs = mapper(sequence)
    
    # 3. Shuffle & Sort (Ordenar alfabéticamente para que el reducer funcione)
    pairs = sorted(pairs)
    
    # 4. Fase de Reduce
    reduced = reducer(pairs)
    
    # 5. Guardar resultados
    save_output(output_directory, reduced)

if __name__ == "__main__":
    run_job(
        "files/input",
        "files/output",
    )