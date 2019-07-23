import pygame as pg

pg.init()

fondo = pg.image.load('fondo.png')

# fichas
anchoficha = 60
altoficha = 60
x = pg.image.load('x.png')
o = pg.image.load('o.png')
Y = pg.image.load('Y.png')
esp = pg.image.load('esp.png')
# textos
fuente36 = pg.font.Font('8-BIT-WONDER.TTF', 36)
fuente24 = pg.font.Font('8-BIT-WONDER.TTF', 24)

# Colores
Negro = (0, 0, 0)
Amarillo = (206, 206, 0)
Violeta = (206, 0, 206)


class Ficha:
    def __init__(self, valor, fil, col):
        self.valor = valor
        self.col = col
        self.fil = fil
        self.px = 140 + col * anchoficha
        self.py = 290 + fil * altoficha
        self.foto = pg.image.load(valor + '.png')
        self.rc = self.foto.get_rect(topleft=(self.px, self.py))


class Tabla:
    def __init__(self, t):
        tab = []
        fila = 0
        for linea in t.split(','):
            arr = []
            columna = 0
            for l in range(0, len(linea)):
                if linea[l] == "x":
                    f = Ficha('x', fila, columna)
                elif linea[l] == "o":
                    f = Ficha('o', fila, columna)
                else:
                    f = Ficha('esp', fila, columna)
                columna += 1
                arr.append(f)
            tab.append(arr)
            fila += 1
        self.t = tab
        self.anterior = ""
        self.fichas = len(t) - len(t.replace('x', ''))
        self.comidas = 0
        self.puntaje = 0

    def redibujar(self):
        def valor(t: str, y: int):
            x = 910
            texto = fuente36.render(t, True, Amarillo)
            ancho = texto.get_width()
            pantalla.blit(texto, (x - ancho, y))
            pg.draw.rect(pantalla, Negro, (x - ancho - 2, y + 20, texto.get_width() + 4, 3))

        def titulo(t: str, y: int, sub: bool = True, ):
            x = 720
            texto = fuente36.render(t, True, Amarillo)
            ancho = texto.get_width()
            pantalla.blit(texto, (x, y))
            pg.draw.rect(pantalla, Negro, (x - 2, y + 15, ancho + 4, 5))
            if sub: pg.draw.rect(pantalla, Violeta, (x, y + texto.get_height() + 2, 260, 10))

        pantalla.blit(fondo, (0, 0))
        for l in self.t:
            for f in l:
                pantalla.blit(f.foto, (f.px, f.py))
                f.rc.move(f.px, f.py)

        titulo("PUNTOS", 250)
        valor(str(self.puntaje), 305)
        titulo("FICHAS", 360)
        valor(str(self.fichas), 415)
        titulo("COMIDAS", 470)
        valor(str(self.comidas), 525)
        titulo("NIVEL ", 580)
        valor(str(nivel), 635)

    def mover(self, f):
        def pone(f, v):
            self.t[f.fil][f.col] = Ficha(v, f.fil, f.col)

        def marca(f):
            if self.anterior:
                pone(self.anterior, 'x')
            pone(f, 'Y')
            self.anterior = f

        def errado(n):
            pg.mixer.music.load('no.mp3')
            pg.mixer.music.play(0)
            print(n)

        # ----- MOVER
        ant = self.anterior
        d = f.valor
        if (d == "esp ") or ((d == "o") and (ant == "")):
            errado("No hay ficha ahí")
            return
        if d in "xY":
            marca(f)
            return
        if (f.col != ant.col) and (f.fil != ant.fil):
            errado("No puedo mover diagonal")
            return
        if (abs(f.col - ant.col) + abs(f.fil - ant.fil)) != 2:
            errado("No puedo saltar tan lejos")
            return
        if f.col == ant.col:
            salto = self.t[int((f.fil + ant.fil) / 2)][f.col]
        else:
            salto = self.t[f.fil][int((f.col + ant.col) / 2)]
        if salto.valor != "x":
            errado("Debe haber una ficha al medio")
            return
        else:
            pone(ant, 'o')
            pone(salto, 'o')
            pone(f, 'Y')
            self.anterior = f
            self.fichas -= 1
            self.comidas += 1
            self.puntaje += 100
            if sonido != 0:
                pg.mixer.music.load('ok.mp3')
                pg.mixer.music.play(0)
            if self.fichas == 1:
                return "Next"


def jugar(n):
    pantalla.blit(fondo, (0, 0))
    mensaje("NIVEL " + str(n), 350, 450, 2000)
    senku = Tabla(niveles[n])

    senku.redibujar()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return "salir"
            if event.type == pg.MOUSEBUTTONUP:
                pos = pg.mouse.get_pos()
                for fila in senku.t:
                    for f in fila:
                        if f.rc.collidepoint(pos):
                            if f.valor != "esp":
                                m = senku.mover(f)
                                if m == "Next":
                                    return "Next"
                                senku.redibujar()
            keys = pg.key.get_pressed()
            if keys[pg.K_s]:
                return "s"
        pg.display.flip()


def mensaje(t, x, y, tiempo: int = 0):
    texto = fuente24.render(t, True, Amarillo)
    ancho = texto.get_width() / 2
    pantalla.blit(texto, (x - ancho, y))
    pg.draw.rect(pantalla, Negro, (x - ancho - 2, y + 14, texto.get_width() + 4, 3))
    if tiempo != 0:
        pg.display.flip()
        pg.time.delay(tiempo)


def felicitaciones(n):
    pg.draw.rect(pantalla, Negro, (60, 250, 580, 500))
    mensaje("FELICITACIONES II", 350, 350)
    mensaje("HAS VENCIDO EL NIVEL " + str(n), 350, 450)
    bono = (n + 1) * 100
    mensaje("RECOMPENSA " + str(bono) + " PUNTOS", 350, 550, 3000)


niveles = []
niveles.append("       ,       , xxo   ,       ,       ,       ,       ")
niveles.append("       ,   x   , xxo   ,   o   ,       ,       ,       ")
niveles.append("  oxo  ,  xoxo ,oxoxo  ,xox    ,oxoxo  , ox x  ,    oxx")
niveles.append("  ooo  , oxxo  ,xxooo  ,  xox  ,  ooo  , oooxx , xxooo ")
niveles.append("   x   ,   x   ,  ooo  , oxxxo ,oxooxoo,ooxoxxo,   o   ")
niveles.append(" oxoxo , ooxxo , xxoxo , oxooo ,  ooo  ,ooooooo,       ")
niveles.append("ooooooo,xxoooxo,oxo xoo,ooxoxxo,ooo oox,xxo xxo,xoxooxx")
niveles.append("  xx   ,o oxxo ,xoox o ,  xx   , ooo   , x x   ,ox oxo ")
niveles.append("       , o o x , oxoxo , oxoxx , oooox , xoooo ,xxoxoxo")
niveles.append("xoo    ,oxx    ,oxo    ,ooxo   ,ooooxoo,xxoxxxo,oxoooox")
niveles.append("oxoxooo,xxoxoxx,oxxooxo,   oox ,    xx ,    xo ,       ")
niveles.append("   o   ,  xxx  ,  xxx  ,  xoo  ,  xxo  , ooooo ,xxo oxx")
niveles.append("   o   ,  xxo  , ooxoo ,ooxoooo,  oxo  ,  xxx  ,  xxx  ")
niveles.append(" x o   , x o   ,oooxox ,xoooxo ,oxxxoo ,oxxxox ,oxxxoo ")
niveles.append(" oxo  x, xox  x, ooxoxo, xxxoxo, xoooox,    xxo,       ")
niveles.append("     x , oxoxo , oxoxx , oxxox , xoxxo ,xxoxxxx,       ")
niveles.append("  xxx  ,  xxx  ,xxxxxxx,xxx0xxx,xxxxxxx,  xxx  ,  xxx  ")

# Parte gráfica
pantalla = pg.display.set_mode((1090, 800))
pg.display.set_caption('SENKU - La revancha')
nivel = 0
sonido = 0

while True:
    r = jugar(nivel)
    if r == "Next":
        felicitaciones(nivel)
        nivel += 1
    elif r == "salir":
        print("El SENKU te ha vencido!")
        break
pg.quit()
