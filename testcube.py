import random
import sys

moves = ["U", "D", "F", "B", "R", "L"]
dir = ["", "'", "2"]
slen = random.randint(25, 28)
#ESTA ES LA BUENA
#Funcion para generar un scramble con un numero de movimientos dentro del rango
def gen_scramble():
    # Checkea si el siguiente movimiento es igual para hacerlo doble ex R2
    # Modifica aquellas letras con igual patron para cambiarlo
    s = valid([[random.choice(moves), random.choice(dir)] for x in range(slen)])
    

    # Formatear la mezcla a string
    return ''.join(str(s[x][0]) + str(s[x][1]) + ' ' for x in range(len(s))) + "[" + str(slen) + "]"
#Funcion para validar la mezcla
def valid(ar):
    # Checkea si el siguiente movimiento es igual para hacerlo doble ex R2
    # Modifica aquellas letras con igual patron para cambiarlo
    for x in range(1, len(ar)):
        while ar[x][0] == ar[x-1][0]:
            ar[x][0] = random.choice(moves)
    for x in range(2, len(ar)):
        while ar[x][0] == ar[x-2][0] or ar[x][0] == ar[x-1][0]:
            ar[x][0] = random.choice(moves)
    return ar
#Crea el scramble
s = gen_scramble()
print(s)