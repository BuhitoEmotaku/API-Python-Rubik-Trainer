import sys

#Clase Cube para generar mezclas aleatorias y shufflearlas
class Cube:
    #Init original de los datos
    def __init__(self):
        self.cube = [['w', 'w', 'w', 'w', 'w', 'w', 'w', 'w'], ['o', 'o', 'o', 'o', 'o', 'o', 'o', 'o'], ['g', 'g', 'g', 'g', 'g', 'g', 'g', 'g'], ['r', 'r', 'r', 'r', 'r', 'r', 'r', 'r'], ['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'], ['y', 'y', 'y', 'y', 'y', 'y', 'y', 'y']]

    #Funcion para asignar caras
    def faceMove(self, x):
        self.cube[x][0], self.cube[x][6], self.cube[x][4], self.cube[x][2] = self.cube[x][6], self.cube[x][4], self.cube[x][2], self.cube[x][0]
        self.cube[x][1], self.cube[x][7], self.cube[x][5], self.cube[x][3] = self.cube[x][7], self.cube[x][5], self.cube[x][3], self.cube[x][1]
        return

    #Funcion para asignar caras primas
    def faceMovePrime(self, x):
        self.cube[x][0], self.cube[x][2], self.cube[x][4], self.cube[x][6] = self.cube[x][2], self.cube[x][4], self.cube[x][6], self.cube[x][0]
        self.cube[x][1], self.cube[x][3], self.cube[x][5], self.cube[x][7] = self.cube[x][3], self.cube[x][5], self.cube[x][7], self.cube[x][1]
        return

    #Funcion para hacer el shuffle entre ellas
    def swap(self, x1, x2, x3, x4, y1, y2, y3, y4):
        self.cube[x1][y1], self.cube[x2][y2], self.cube[x3][y3], self.cube[x4][y4] = self.cube[x2][y2], self.cube[x3][y3], self.cube[x4][y4], self.cube[x1][y1]

    #funcion para printear la solucion de fomar bonita y en 2d
    def printCube(self):
        print(
                                                            "    " + self.cube[0][0] + self.cube[0][1] + self.cube[0][2] + "\n" +
                                                            "    " + self.cube[0][7] + "w" + self.cube[0][3] + "\n" +
                                                            "    " + self.cube[0][6] + self.cube[0][5] + self.cube[0][4] + "\n\n" +
                    self.cube[1][0] + self.cube[1][1] + self.cube[1][2] + " " + self.cube[2][0] + self.cube[2][1] + self.cube[2][2] + " " + self.cube[3][0] + self.cube[3][1] + self.cube[3][2] + " " + self.cube[4][0] + self.cube[4][1] + self.cube[4][2] + "\n" +
                    self.cube[1][7] + "o" + self.cube[1][3] + " " + self.cube[2][7] + "g" + self.cube[2][3] + " " + self.cube[3][7] + "r" + self.cube[3][3] + " " + self.cube[4][7] + "b" + self.cube[4][3] + "\n" +
                    self.cube[1][6] + self.cube[1][5] + self.cube[1][4] + " " + self.cube[2][6] + self.cube[2][5] + self.cube[2][4] + " " + self.cube[3][6] + self.cube[3][5] + self.cube[3][4] + " " + self.cube[4][6] + self.cube[4][5] + self.cube[4][4] + "\n\n" +
                                                            "    " + self.cube[5][0] + self.cube[5][1] + self.cube[5][2] + "\n" +
                                                            "    " + self.cube[5][7] + "y" + self.cube[5][3] + "\n" +
                                                            "    " + self.cube[5][6] + self.cube[5][5] + self.cube[5][4] + "\n"
                )

    


# print(cube.cube)
#Funcuion para hacer el shuffle con cada cara y cada pieza dependiendo de la letra
def move(cube, m, x):
    #Hay que hacer 3 shuffles con cada letra
    if(m == 'U'):
        cube.faceMove(x)
        cube.swap(1,2,3,4,0,0,0,0)
        cube.swap(1,2,3,4,1,1,1,1)
        cube.swap(1,2,3,4,2,2,2,2)
    elif(m == "U'"):
        cube.faceMovePrime(x)
        cube.swap(1,4,3,2,0,0,0,0)
        cube.swap(1,4,3,2,1,1,1,1)
        cube.swap(1,4,3,2,2,2,2,2)
    elif(m == 'U2'):
        move(cube, 'U', x)
        move(cube, 'U', x)
    elif(m == 'D'):
        cube.faceMove(x)
        cube.swap(1,4,3,2,4,4,4,4)
        cube.swap(1,4,3,2,5,5,5,5)
        cube.swap(1,4,3,2,6,6,6,6)
    elif(m == "D'"):
        cube.faceMovePrime(x)
        cube.swap(1,2,3,4,4,4,4,4)
        cube.swap(1,2,3,4,5,5,5,5)
        cube.swap(1,2,3,4,6,6,6,6)
    elif(m == 'D2'):
        move(cube, 'D', x)
        move(cube, 'D', x)
    elif(m == 'R'):
        cube.faceMove(x)
        cube.swap(0,2,5,4,2,2,2,6)
        cube.swap(0,2,5,4,3,3,3,7)
        cube.swap(0,2,5,4,4,4,4,0)
    elif(m == "R'"):
        cube.faceMovePrime(x)
        cube.swap(0,4,5,2,2,6,2,2)
        cube.swap(0,4,5,2,3,7,3,3)
        cube.swap(0,4,5,2,4,0,4,4)
    elif(m == 'R2'):
        move(cube, 'R', x)
        move(cube, 'R', x)
    elif(m == 'L'):
        cube.faceMove(x)
        cube.swap(0,4,5,2,6,2,6,6)
        cube.swap(0,4,5,2,7,3,7,7)
        cube.swap(0,4,5,2,0,4,0,0)
    elif(m == "L'"):
        cube.faceMovePrime(x)
        cube.swap(0,2,5,4,6,6,6,2)
        cube.swap(0,2,5,4,7,7,7,3)
        cube.swap(0,2,5,4,0,0,0,4)
    elif(m == 'L2'):
        move(cube, 'L', x)
        move(cube, 'L', x)
    elif(m == 'F'):
        cube.faceMove(x)
        cube.swap(0,1,5,3,4,2,0,6)
        cube.swap(0,1,5,3,5,3,1,7)
        cube.swap(0,1,5,3,6,4,2,0)
    elif(m == "F'"):
        cube.faceMovePrime(x)
        cube.swap(0,3,5,1,4,6,0,2)
        cube.swap(0,3,5,1,5,7,1,3)
        cube.swap(0,3,5,1,6,0,2,4)
    elif(m == 'F2'):
        move(cube, 'F', x)
        move(cube, 'F', x)
    elif(m == 'B'):
        cube.faceMove(x)
        cube.swap(0,3,5,1,0,2,4,6)
        cube.swap(0,3,5,1,1,3,5,7)
        cube.swap(0,3,5,1,2,4,6,0)
    elif(m == "B'"):
        cube.faceMovePrime(x)
        cube.swap(0,1,5,3,0,6,4,2)
        cube.swap(0,1,5,3,1,7,5,3)
        cube.swap(0,1,5,3,2,0,6,4)
    elif(m == 'B2'):
        move(cube, 'B', x)
        move(cube, 'B', x)

#Funcion para hacer un scramble y sacar las letras
def scramble(scr, len):
    #Ejecutamos todo lo de arriba en secuencia para generar la mezcla y codigo de colores
    cube = Cube()
    moves = ['U', 'L', 'F', 'R', 'B', 'D']
    print(scr)
    for x in scr:
        move(cube, str(x[0])+str(x[1]), moves.index(x[0]))

    scr = ''.join(str(scr[x][0]) + str(scr[x][1]) + ' ' for x in range(len)) + "[" + str(len) + "]"
    cube.printCube()
