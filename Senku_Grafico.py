import pygame as pg


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
    def __init__(self, t, p):
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
        self.puntaje = p

    def redibujar(self):
        def valor(t: str, y: int):
            x = 940
            texto = fuente36.render(t, True, Amarillo)
            ancho = texto.get_width()
            pantalla.blit(texto, (x - ancho, y))
            pg.draw.rect(pantalla, Negro, (x - ancho - 2, y + 18, texto.get_width() + 4, 5))

        def titulo(t: str, y: int):
            x = 720
            texto = fuente36.render(t, True, Amarillo)
            ancho = texto.get_width()
            pantalla.blit(texto, (x, y))
            pg.draw.rect(pantalla, Negro, (x - 2, y + 15, ancho + 4, 5))
            pg.draw.rect(pantalla, Violeta, (x, y + texto.get_height() + 2, 260, 10))

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
        pantalla.blit(reiniciar, (740, 700))
        if sonido != 0:
            pantalla.blit(ruido, (830, 700))
        else:
            pantalla.blit(silencio, (830, 700))
        pantalla.blit(salida, (920, 700))

    def mover(self, f, sonido):
        def pone(f, v):
            self.t[f.fil][f.col] = Ficha(v, f.fil, f.col)

        def marca(f):
            if self.anterior:
                pone(self.anterior, 'x')
            pone(f, 'Y')
            self.anterior = f

        def bip():
            if sonido != 0:
                pg.mixer.music.load('ok.mp3')
                pg.mixer.music.play(0)

        def errado():
            if sonido != 0:
                pg.mixer.music.load('no.mp3')
                pg.mixer.music.play(0)

        # ----- MOVER
        ant = self.anterior
        d = f.valor
        if (d == "esp ") or ((d == "o") and (ant == "")):
            errado()
            return
        if d in "xY":
            marca(f)
            return
        if ((f.col != ant.col) and (f.fil != ant.fil)) or ((abs(f.col - ant.col) + abs(f.fil - ant.fil)) != 2):
            errado()
            return
        if f.col == ant.col:
            salto = self.t[int((f.fil + ant.fil) / 2)][f.col]
        else:
            salto = self.t[f.fil][int((f.col + ant.col) / 2)]
        if salto.valor != "x":
            errado()
            return
        else:
            pone(ant, 'o')
            pone(salto, 'o')
            pone(f, 'Y')
            self.anterior = f
            self.fichas -= 1
            self.comidas += 1
            self.puntaje += 100
            bip()
            if self.fichas == 1:
                return "Next"


def jugar(n, puntos, sonido):
    pantalla.blit(fondo, (0, 0))
    mensaje("NIVEL " + str(n), 350, 450, 1000)
    senku = Tabla(niveles[n], puntos)
    senku.redibujar()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return "salir", senku.puntaje
            if event.type == pg.MOUSEBUTTONUP:
                pos = pg.mouse.get_pos()
                for fila in senku.t:
                    for f in fila:
                        if f.rc.collidepoint(pos):
                            if f.valor != "esp":
                                m = senku.mover(f, sonido)
                                print(sonido)
                                if m == "Next":
                                    return "Next", senku.puntaje
                                senku.redibujar()
                if salida.get_rect(topleft=(920, 700)).collidepoint(pos):
                    return "salir", senku.puntaje
                if reiniciar.get_rect(topleft=(740, 700)).collidepoint(pos):
                    return "r", senku.puntaje
                if ruido.get_rect(topleft=(830, 700)).collidepoint(pos):
                    sonido = 0
                if silencio.get_rect(topleft=(830, 700)).collidepoint(pos):
                    sonido = 1
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
    pg.draw.rect(pantalla, Negro, (710, 240, 280, 520))
    mensaje("NIVEL " + str(n) + " VENCIDO II", 350, 350)
    bono = (n + 1) * 100
    mensaje("RECOMPENSA " + str(bono) + " PUNTOS", 350, 450)
    mensaje("FELICITACIONES", 350, 550, 2000)


# Parte gráfica
pg.init()
pantalla = pg.display.set_mode((1090, 800))
pg.display.set_caption('SENKU - La revancha')
# Imágenes
splash = pg.image.load('splash.png')
fondo = pg.image.load('fondo.png')
ruido = pg.image.load('sonido.gif')
silencio = pg.image.load('silencio.gif')
reiniciar = pg.image.load('reiniciar.gif')
salida = pg.image.load('salida.gif')
# Fichas
anchoficha = 60
altoficha = 60
x = pg.image.load('x.png')
o = pg.image.load('o.png')
Y = pg.image.load('Y.png')
esp = pg.image.load('esp.png')
# Textos
fuente36 = pg.font.Font('8-BIT-WONDER.TTF', 36)
fuente24 = pg.font.Font('8-BIT-WONDER.TTF', 24)
# Colores
Negro = (0, 0, 0)
Amarillo = (206, 206, 0)
Violeta = (206, 0, 206)
# Variables
nivel = 0
sonido = 1
puntos = 0

niveles = []
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

pantalla.blit(splash, (0, 0))
pg.display.flip()
pg.time.delay(2000)

while True:
    r, puntos = jugar(nivel, puntos, sonido)
    if r == "Next":
        felicitaciones(nivel)
        puntos += nivel * 100
        nivel += 1
    elif r == "salir":
        pantalla.blit(fondo, (0, 0))
        mensaje("El SENKU TE HA VENCIDO", 350, 450, 1000)
        break
    print(puntos)
pg.quit()
