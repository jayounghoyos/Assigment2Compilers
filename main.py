import sys

def leer_entrada():
    """Leer toda la entrada de stdin, eliminando líneas vacías"""
    datos = [linea for linea in sys.stdin.read().strip().splitlines() if linea.strip()]
    num_casos = int(datos[0])  # Leer el número de casos desde la primera línea
    indice = 1
    casos = []

    # Parsear los casos de entrada
    for _ in range(num_casos):
        # Leer el número de no terminales y el número de cadenas a analizar
        num_no_terminales, num_cadenas = map(int, datos[indice].split())
        indice += 1

        # Inicializar el diccionario de gramática
        gramatica = {}
        for _ in range(num_no_terminales):
            linea = datos[indice].split()
            no_terminal = linea[0]  # El primer elemento es el no terminal
            producciones = linea[1:]  # El resto son las producciones

            # Si el no terminal no está en el diccionario, agregarlo
            if no_terminal not in gramatica:
                gramatica[no_terminal] = []

            # Agregar cada producción a la gramática
            for prod in producciones:
                if len(prod) > 1:  # Si la producción es binaria (dos símbolos)
                    gramatica[no_terminal].append(tuple(prod))  # Agregar como tupla
                else:  # Si es una producción unitaria (un solo símbolo)
                    gramatica[no_terminal].append(
                        (prod,)
                    )  # Agregar como una tupla de un solo elemento
            indice += 1

        # Leer las cadenas de entrada a analizar
        cadenas = []
        for _ in range(num_cadenas):
            cadenas.append(datos[indice])  # Agregar cada cadena de entrada
            indice += 1

        # Guardar la gramática y las cadenas para este caso
        casos.append((gramatica, cadenas))

    return casos  # Devolver todos los casos parseados


def algoritmo_cky(gramatica, cadena_entrada):
    """Algoritmo CKY"""
    n = len(cadena_entrada)  # Longitud de la cadena de entrada

    # Crear una tabla vacía de tamaño n x n+1 inicializada con conjuntos vacíos
    tabla = [[set() for _ in range(n + 1)] for _ in range(n)]

    # Rellenar la tabla para subcadenas de longitud 1 (terminales)
    for i in range(n):
        for (
            izq,
            producciones,
        ) in gramatica.items():  # Para cada no terminal y sus producciones
            for prod in producciones:
                if (
                    len(prod) == 1 and prod[0] == cadena_entrada[i]
                ):  # Si es una producción unitaria
                    tabla[i][i + 1].add(
                        izq
                    )  # Agregar el no terminal que produce el símbolo

    # Rellenar la tabla para subcadenas más largas
    for longitud in range(2, n + 1):  # Para cada longitud de subcadena >= 2
        for i in range(n - longitud + 1):  # Iterar sobre todas las subcadenas posibles
            j = i + longitud
            for k in range(i + 1, j):  # Separar la subcadena en dos partes
                for izq, producciones in gramatica.items():  # Para cada no terminal
                    for prod in producciones:
                        if (
                            len(prod) == 2
                            and prod[0] in tabla[i][k]
                            and prod[1] in tabla[k][j]
                        ):
                            # Si ambas partes de la producción están en la tabla, agregar el no terminal
                            tabla[i][j].add(izq)

    # Verificar si el símbolo inicial 'S' está en la tabla en la posición correspondiente
    return "S" in tabla[0][n]


def main():
    casos = leer_entrada()  # Parsear la entrada

    # Procesar cada caso
    for num_caso, (gramatica, cadenas) in enumerate(casos, 1):
        for cadena_entrada in cadenas:
            resultado = algoritmo_cky(
                gramatica, cadena_entrada
            )  # Ejecutar el algoritmo CKY para cada cadena
            if resultado:
                print("yes")  # "yes" si es generada
            else:
                print("no")  # "no" Si no es generada


if __name__ == "__main__":
    main()  # Ejecutar la función principal
