from array import *
from random import randrange

class Table():
    def __init__(self,t):
        tab=[]
        for linea in t.split(','):
            arr=[]
            for l in range(0, len(linea)):
                arr.append(linea[l])
            tab.append(arr)
        self.t=tab
        self.anterior = ""
        self.puntos=0

    def dibujar(self):
        import os
        clear = lambda: os.system('cls')
        clear()
        #Títulos de columnas
        print(" ",end="")
        for f in range(0, 7):
            print(str(f),end=" ")
        print("")
        #Títulos de filas
        tf = 0
        for fila in self.t:
            col = str(tf) + " "
            for columna in fila:
                col = col + " " + columna
            print(col)
            tf += 1

    def mover(self,num):
        def pone(n,cont):
            self.t[int(n[1])][int(n[0])] = cont

        def dame(n):
            return self.t[int(n[1])][int(n[0])]

        def marca(num):
            if dame(num) != "x":
                return "No hay ficha ahí"
            else:
                if self.anterior != "":
                    pone(self.anterior, 'x')
                pone(num, 'X')
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
            if num[0] == self.anterior[0]:
                salto = num[0] + medio(num,ant,1)
            else:
                salto = medio(num, ant, 0) + num[1]
            if dame(salto) !="x":
                return("Debe haber una ficha al medio")
            else:
                pone(ant,'0')
                pone(salto,'0')
                pone(num,'X')
                self.anterior=num
                self.puntos+=1
                return "Puntos: "+str(self.puntos)

        def errado(n):
            mal=[]
            mal.append("¿Qué significa '{}'?")
            mal.append("Ja ja! '{}' muy divertido!")
            mal.append("Keyboard error: {}")
            mal.append("Mas '{}' serás vos")
            mal.append("'{}', ¿Es en serio?")
            mal.append("Había una vez un {}. Fin.")
            return mal[int(randrange(len(mal)))].format(n)

        #Loop principal
        msj = ""
        try:
            a=int(num)
            if len(num)==2:
                msj = marca(num)
            elif (num[0] == "+") and (len(num) == 3):
                msj = muevo(num[1]+num[2])
        except ValueError:
            msj = errado(num)
        if num.lower() != "salir":
            self.dibujar()
            print(msj)


senku=Table('  xxx  ,  xxx  ,xxxxxxx,xxx0xxx,xxxxxxx,  xxx  ,  xxx  ')
senku.dibujar()

move=""
while move.lower() != "salir":
    move=input("Orden:")
    if move:
        senku.mover(move)
    else:
        senku.dibujar()