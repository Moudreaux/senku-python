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
fuente = pg.font.SysFont('Impact', 36)
texto = fuente.render('Some Text', True, (0, 0, 0))


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

    def redibujar(self):
        def texto(t: str, x: int, y: int):
            texto = fuente.render(t, False, (255, 255, 0))
            pantalla.blit(texto, (x, y))

        pantalla.blit(fondo, (0, 0))
        for l in self.t:
            for f in l:
                pantalla.blit(f.foto, (f.px, f.py))
                f.rc.move(f.px, f.py)
        texto(str(self.fichas), 820, 480)
        texto(str(self.comidas), 820, 610)

    def mover(self, f):
        def pone(f, v):
            self.t[f.fil][f.col] = Ficha(v, f.fil, f.col)

        def marca(f):
            if self.anterior != "":
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
            pg.mixer.music.load('ok.mp3')
            pg.mixer.music.play(0)
            if self.fichas == 1:
                return "fin"


niveles = []
niveles.append("  oxo  ,  xoxo ,oxoxo  ,xox    ,oxoxo  , ox x  ,    oxx")
niveles.append("  ooo  , oxxo  ,xxooo  ,  xox  ,  ooo  , oooxx , xxooo ")
niveles.append("   x   ,   x   ,  ooo  , oxxxo ,oxooxoo,ooxoxxo,   o   ")
niveles.append(" oxoxo , ooxxo , xxoxo , oxooo ,  ooo  ,ooooooo,       ")
niveles.append("ooooooo,xxoooxo,oxo xoo,ooxoxxo,ooo oox,xxo xxo,xoxooxx")
niveles.append("  xxx  ,  xxx  ,xxxxxxx,xxx0xxx,xxxxxxx,  xxx  ,  xxx  ")

# Parte gráfica
size = 800, 600
pantalla = pg.display.set_mode((1090, 800))
pg.display.set_caption('SENKU - La revancha')
pantalla.blit(fondo, (0, 0))
senku = Tabla(niveles[0])
senku.redibujar()

run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.MOUSEBUTTONUP:
            pos = pg.mouse.get_pos()
            for fila in senku.t:
                for f in fila:
                    if f.rc.collidepoint(pos):
                        if f.valor != "esp":
                            senku.mover(f)
                            senku.redibujar()
        if event.type == pg.K_s:
            pg.quit()
    pg.display.flip()
pg.quit()
