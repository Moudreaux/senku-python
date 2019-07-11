from random import randrange


class Tabla:
    def __init__(self, t):
        tab = []
        for linea in t.split(','):
            arr = []
            for l in range(0, len(linea)):
                arr.append(linea[l])
            tab.append(arr)
        self.t = tab
        self.anterior = ""
        self.tot_fil = len(t.split(','))
        self.tot_col = len(linea)
        self.fichas = len(t) - len(t.replace('x', ''))

    def limpiar(self):
        import os
        clear = lambda: os.system('cls')
        clear()

    def dibujar(self):
        self.limpiar()
        # Títulos de columnas
        print("   ", end="")
        for f in range(0, self.tot_col):
            print(str(f), end=" ")
        print("")
        # Títulos de filas
        tf = 0
        for fila in self.t:
            col = str(tf) + " "
            for columna in fila:
                col = col + " " + columna
            print(col)
            tf += 1
        print("")

    def mover(self, num):
        def pone(n, cont):
            self.t[int(n[1])][int(n[0])] = cont

        def dame(n):
            return self.t[int(n[1])][int(n[0])]

        def marca(num):
            if self.anterior != "":
                pone(self.anterior, 'x')
            pone(num, 'X')
            self.anterior = num

        def medio(n1, n2, i):
            return str(int((int(n1[i]) + int(n2[i])) / 2))

        def felicitar():
            print("¡¡FELICITACIONES!!")

        def muevo(num):
            ant = self.anterior
            d = dame(num)
            if (d == " ") or ((d == "o") and (ant == "")):
                return "No hay ficha ahí!"
            if d in "xX":
                marca(num)
                return ""
            if (num[0] != ant[0]) and (num[1] != ant[1]):
                return "No puedo mover diagonal"
            if (abs(int(num[0]) - int(ant[0])) + abs(int(num[1]) - int(ant[1]))) != 2:
                return "No puedo saltar tan lejos"
            if num[0] == self.anterior[0]:
                salto = num[0] + medio(num, ant, 1)
            else:
                salto = medio(num, ant, 0) + num[1]
            if dame(salto) != "x":
                return ("Debe haber una ficha al medio")
            else:
                pone(ant, 'o')
                pone(salto, 'o')
                pone(num, 'X')
                self.anterior = num
                self.fichas -= 1
                if self.fichas == 1:
                    return ""
                else:
                    return "Faltan: " + str(self.fichas - 1)

        def errado(n):
            mal = []
            mal.append("¿Qué significa '{}'?")
            mal.append("Ja ja! '{}' muy divertido!")
            mal.append("Keyboard error: {}")
            mal.append("Mas '{}' serás vos")
            mal.append("'{}', ¿Es en serio?")
            mal.append("Había una vez un {}. Fin.")
            return mal[int(randrange(len(mal)))].format(n)

        # Loop principal
        try:
            a = int(num)
            if len(num) != 2:
                msj = "Coordenadas erradas"
            elif (int(num[0]) < self.tot_col) and (int(num[1]) < self.tot_fil):
                msj = muevo(num)
            else:
                msj = "Coordenadas erradas"
        except ValueError:
            msj = errado(num)
        if num.lower() != "s":
            self.dibujar()
            print(msj)


def jugar(n):
    senku = Tabla(n)
    senku.dibujar()
    move = ""
    while True:
        move = input("Orden:")
        if move.lower() == "s":
            return 0
        elif move:
            senku.mover(move)
            if senku.fichas == 1:
                print("Felicitaciones!!!")
                return 1
        else:
            senku.dibujar()


def tutorial():
    def obliga(n):
        m = ""
        while m != n:
            print("Escribe " + n + " y presiona Enter")
            m = input("Orden:")
        demo.mover(n)

    demo = Tabla(' xxox ')
    demo.limpiar()
    print("Bienvenido a Senku")
    print("El objetivo del juego es ir eliminando fichas (x) hasta que quede una sola.")
    nada = input("Presiona Enter para mostrar el tablero")
    demo.dibujar()
    obliga("10")
    print("Como verás la x de columna 1 y fila 0 se marco en X para indicar que está seleccionada")
    obliga("30")
    print("Como verás la X saltó sobre la x eliminándola y cambiando de posición a 3 0")
    obliga("40")
    print("Si seleccionas otra ficha distinta a la seleccionada se cambia la selección")
    obliga("20")
    print("Felicitaciones. Has vencido este nivel")
    print("Ya estas listo para jugar")


niveles = []
niveles.append("  oxo  ,  xoxo ,oxoxo  ,xox   ,oxoxo  , ox x  ,    oxx")
niveles.append("  ooo , oxxo ,xxooo ,  xox ,  ooo , oooxx, xxooo")
niveles.append("   x   ,   x   ,  ooo  , oxxxo ,oxooxoo,ooxoxxo,   o   ")
niveles.append(" oxoxo , ooxxo , xxoxo , oxooo ,  ooo  ,ooooooo")
niveles.append("ooooooo,xxoooxo,oxo xoo,ooxoxxo,ooo oox,xxo xxo,xoxooxx")
niveles.append("  xxx  ,  xxx  ,xxxxxxx,xxx0xxx,xxxxxxx,  xxx  ,  xxx  ")

# jugar(niveles[3])


print("Bienvenido a Senku")
print("------------------")
print("1 - Tutorial")
print("2 - Jugar")
print("S - Salir")
tutorial()
