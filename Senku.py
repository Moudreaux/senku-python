from array import *

class tablero():
    """ Create the board"""
    def __init__(self,numero):
        def linea(texto):
            arr = []
            for l in range(0, len(texto)):
                arr.append(texto[l])
            return arr

        lineas = [[], [], [], [], [], [], []]
        lineas[0] = linea("  xxx  ")
        lineas[1] = linea("  xxx  ")
        lineas[2] = linea("xxxxxxx")
        lineas[3] = linea("xxx0xxx")
        lineas[4] = linea("xxxxxxx")
        lineas[5] = linea("  xxx  ")
        lineas[6] = linea("  xxx  ")
        self.t=lineas
        self.anterior = ""

    def dibujar(self):
        import os
        clear = lambda: os.system('cls')
        clear()
        tc = "  "
        for f in range(0, 7):
            tc = tc + " " + str(f)
        print(tc)
        tf = 0
        for fila in self.t:
            col = str(tf) + " "
            for columna in fila:
                col = col + " " + columna
            print(col)
            tf = tf + 1

    def mover(self,num):
        def poner(n,cont):
                self.t[int(n[1])][int(n[0])] = cont

        def dame(n):
            return self.t[int(n[1])][int(n[0])]

        def marco(num):
            if dame(num) != "x":
                return "No hay ficha ahí"
            else:
                if self.anterior != "":
                    poner(self.anterior, 'x')
                poner(num, 'X')
                self.anterior = num
                return ""

        def medio(n1,n2,i):
            return str(int((int(n1[i]) + int(n2[i]))/2))

        def muevo(num):
            ant=self.anterior
            if dame(num) != "0":
                return "Debo mover a agujero"
            if (num[0] != ant[0]) and (num[1] != ant[1]):
                return "No puedo mover diagonal"
            if (abs(int(num[0])-int(ant[0]))+abs(int(num[1])-int(ant[1]))) != 2:
                return "No puedo saltar tan lejos"
            if (num[0] == self.anterior[0]):
                salto = num[0] + medio(num,ant,1)
            else:
                salto = medio(num, ant, 0) + num[1]
            if dame(salto) !="x":
                return("Debe haber una ficha al medio")
            else:
                poner(ant,'0')
                poner(salto,'0')
                poner(num,'X')
                self.anterior=num
                return "Muevo a: "+num

        """"Loop principal"""
        msj = ""
        if len(num)==2:
            msj = marco(num)
        elif (num[0] == "+") and (len(num) == 3):
            msj = muevo(num[1]+num[2])
        else:
            if num.lower() != "salir":
                msj = "Comando erróneo: "+num
        self.dibujar()
        if len(msj)>0:
            print(msj)


senku=tablero(10)
senku.dibujar()

move=""
while move.lower() != "salir":
    move=input("Orden:")
    senku.mover(move)