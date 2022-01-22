import numpy as np
import sympy as sp
import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib

#ciekawe przypadki
#xy xy, xy x, x^2 -y^2 dywergecja, sin(x) cos(y)

matplotlib.use('TkAgg')

# x,y,z = sp.symbols('x y z')

x,z,roty = sp.symbols('x z roty')
y = sp.Function("y")(x)
C1 = sp.Symbol('C1')

#progressbar
def bar(n,nazwa):
    sg.theme('DarkGrey8')
    progressbar = [
        [sg.ProgressBar(n,orientation='h', size=(50, 20), key='progressbar')]
    ]

    layout =[
        [sg.Frame(nazwa,layout= progressbar)]
    ]
    window = sg.Window('Pole prędkości', layout,no_titlebar=True, alpha_channel=1, grab_anywhere=True)
    return window

#rysowanie wykresow na canvasie
def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

#usuwanie wykresow z canvasu
def delete_fig_agg(fig_agg):
    fig_agg.get_tk_widget().forget()
    fig_agg.get_tk_widget().delete('all')

#rotacja
def rotX(uy,uz='0'):
    uz = uz.replace('y(x)', 'roty')
    uy = uy.replace('y(x)', 'roty')
    A = sp.sympify(sp.diff(sp.sympify(uz),roty)-sp.diff(sp.sympify(uy),z))
    return A

def rotY(ux,uz='0'):
    ux = ux.replace('y(x)', 'roty')
    uz = uz.replace('y(x)', 'roty')
    B = sp.sympify(sp.diff(sp.sympify(ux), z) - sp.diff(sp.sympify(uz), x))
    return B

def rotZ(ux,uy):
    ux = ux.replace('y(x)', 'roty')
    uy = uy.replace('y(x)', 'roty')
    C = sp.sympify(sp.diff(sp.sympify(uy), x) - sp.diff(sp.sympify(ux), roty))
    return C

#dywergencja
def div(ux,uy,uz=0):
    ux = ux.replace('y(x)', 'roty')
    uy = uy.replace('y(x)', 'roty')
    A = sp.diff(sp.sympify(ux),x)
    B = sp.diff(sp.sympify(uy),roty)
    C = sp.diff(sp.sympify(uz),z)
    return A+B+C

#okno pobierania wzorow
def okno_wprowadzania():
    sg.theme('DarkBlue1')
    layout = [[sg.Text("Podaj Ux i Uy")],
                [sg.Text("Ux ="),sg.InputText()],
                [sg.Text("Uy ="),sg.InputText()],
                [sg.Button('Dalej')]]
    window = sg.Window('Pole Prędkości', layout, finalize=True, element_justification='center',font='Helvetica 18')

    event, wsp = window.read()

    if event == sg.WIN_CLOSED:
        exit()

    window.close()

    return wsp

#okno bledu
def blad():
    sg.theme('DarkBlue1')
    layout = [[sg.Text("Error 404")],
              [sg.Text("Wpisz nowe dane")],
              [sg.Button('OK')]]
    window2 = sg.Window('Pole Prędkości', layout, finalize=True, element_justification='center', font='Helvetica 20')
    window2.read()
    window2.close()

#WYKRESY

while(True):
    try:

        wsp = okno_wprowadzania()

        for i, j in wsp.items():
            wsp[i] = j.replace('y', 'y(x)')

        pochodna = sp.Derivative(y)
        rownanie = sp.Eq(pochodna / sp.sympify(wsp[1]), 1 / sp.sympify(wsp[0]))
        wynik = sp.solve(sp.dsolve(rownanie, y), y)

        if(wynik == []):
            raise NameError('pusta tablica')
    except Exception:
        blad()
    else:
        break

#wykres linii prądu
Y, X = np.mgrid[-10:10:21j, -10:10:21j]

progressbar = bar(21*21, "Wykres linii pola")

c=[l for l in range(-10,10)]

for i in range(21):
    for j in range(21):

        try:
            Y[i, j] = wynik[0].subs({x: X[i, j], C1:c[i%21]})
        except Exception:
            Y[i, j]=np.NaN
            X[i, j]=np.NaN
        finally:
            progressbar.Read(timeout=0)
            progressbar['progressbar'].UpdateBar(i * 21 + j)

progressbar.close()

fig1 = plt.figure(figsize=(12, 7), dpi=200)

ax0 = fig1.add_subplot(1,1,1)

for i in range(21):
        ax0.plot(X[i], Y[i])

ax0.set_xlabel('X')
ax0.set_ylabel('Y')
ax0.set_xlim(-10,10)
ax0.set_ylim(-10,10)
ax0.set_title('Linie prądu')
ax0.grid(True)

#wykres toru
X=np.linspace(-10,10,41)
Y=np.linspace(-10,10,41)

progressbar = bar(41, "Wykres toru ruchu")

for i in range(41):
    try:
        Y[i]=wynik[0].subs({x: X[i], C1:1})
    except Exception:
        Y[i]=np.NaN
    finally:
        progressbar.Read(timeout=0)
        progressbar['progressbar'].UpdateBar(i)

progressbar.close()

fig2 = plt.figure(figsize=(12, 7), dpi=200)

ax0 = fig2.add_subplot(1,1,1)
strm = ax0.plot(X, Y)
ax0.set_title('Tor elementu płynu')
ax0.set_xlabel('X')
ax0.set_ylabel('Y')
ax0.grid(True)

#wykres dywergencji

Y, X = np.mgrid[-10:10:21j, -10:10:21j]
diver,miver = np.meshgrid(np.zeros(21), np.zeros(21))

fig4 = plt.figure(figsize=(12, 7), dpi=200)
ax0 = fig4.add_subplot(1,1,1)

divvar = sp.sympify(div(wsp[0], wsp[1]))

progressbar = bar(21*21, "Wykres dywergencji")

for i in range(21):
    for j in range(21):
        try:
            diver[i, j] = divvar.subs({x: X[i, j], roty: Y[i, j]})
        except Exception:
            diver[i, j] = np.NaN
        finally:
            progressbar.Read(timeout=0)
            progressbar['progressbar'].UpdateBar(i * 21 + j)

progressbar.close()

strm = ax0.streamplot(X, Y, X ,Y, density=2,color=diver,cmap='winter',linewidth=1)
fig4.colorbar(strm.lines,label = 'Dywergencja')
ax0.set_title('Dywergencja')
ax0.set_xlabel('X')
ax0.set_ylabel('Y')
ax0.grid(True)


#wykres roatcji

wynikx = sp.sympify(rotX(wsp[1]))
wyniky = sp.sympify(rotY(wsp[0]))
wynikz = sp.sympify(rotZ(wsp[0],wsp[1]))

#jesli rotacja istnieje to program wygeneruje jej wykres
if(wynikx==0 and wyniky==0 and wynikz==0):

    rotacja = 0

else:

    fig3 = plt.figure(figsize=(12, 7), dpi=200)

    ax0 = fig3.add_subplot(1, 1, 1, projection='3d')
    X, Y, Z = np.meshgrid(np.linspace(-10, 10, 21), np.linspace(-10, 10, 21), np.linspace(-10, 10, 21))
    U, V, W = np.meshgrid(np.linspace(-10, 10, 21), np.linspace(-10, 10, 21), np.linspace(-10, 10, 21))

    progressbar = bar(21*21*21, "Wykres rotacji")

    for i in range(21):
        for j in range(21):
            for k in range(21):
                try:
                    U[i, j, k] = wynikx.subs({z: Z[i, j, k], roty: Y[i, j, k], x: X[i, j, k]})
                    V[i, j, k] = wyniky.subs({z: Z[i, j, k], roty: Y[i, j, k], x: X[i, j, k]})
                    W[i, j, k] = wynikz.subs({z: Z[i, j, k], roty: Y[i, j, k], x: X[i, j, k]})
                except Exception:
                    U[i, j, k]=np.NaN
                    V[i, j, k]=np.NaN
                    W[i, j, k]=np.NaN
                progressbar.Read(timeout=0)
                progressbar['progressbar'].UpdateBar(i * 21*21 + j * 21 + k)

    progressbar.close()

    skip = (slice(None, None, 5), slice(None, None, 5), slice(None, None, 5))
    strm = ax0.quiver(X[skip], Y[skip], Z[skip], U[skip], V[skip], W[skip])
    ax0.set_title('Rotacja')
    ax0.set_xlabel('X')
    ax0.set_ylabel('Y')
    ax0.set_zlabel('Z')
    ax0.grid(True)

    rotacja = 1

#okno wykresow
sg.theme('DarkBlue2')

for i,j in wsp.items():
    wsp[i]=j.replace('y(x)','y')

lista_wykresow = ["Linie prądu","Tor elementu płynu","Dywergencja"]

if(rotacja==1):
    lista_wykresow.append("Rotacja")

wybor_wykresu = [
    [sg.Text("Wykresy funkcji: ")],
    [sg.Text("Ux = " + str(wsp[0]))],
    [sg.Text("Uy = " + str(wsp[1]))],
    [sg.Text("")],
    [sg.HSeparator()],
    [sg.Text("")],
    [sg.Text("Linie prądu: ")],
    [sg.Text("y = " + str(wynik[0]))],
    [sg.Text("")],
    [sg.HSeparator()],
    [sg.Text("")],
    [sg.Text("Tor elementu płynu: ")],
    [sg.Text("y = " + str(wynik[0].subs({C1:1})))],
    [sg.Text("")],
    [sg.HSeparator()],
    [sg.Text("")],
    [sg.Text("Dywergencja: ")],
    [sg.Text("div(ux,uy) = " + str(divvar).replace('roty','y'))],
    [sg.Text("")],
    [sg.HSeparator()],
    [sg.Text("")],
    [sg.Text("Rotacja: ")],
    [sg.Text("rot(ux,uy,uz) = (" + str(wynikx).replace('roty','y')+", "+ str(wyniky).replace('roty','y')+", "+ str(wynikz).replace('roty','y') + ")")],
    [sg.Text("")],
    [sg.HSeparator()],
    [sg.Text("")],
    [sg.Text("Dostępne wykresy: ")],
    [sg.Listbox(values=lista_wykresow, enable_events=True, size=(40, len(lista_wykresow)),no_scrollbar=True, key="-WYKRESY-")]
]

wykres = [
    [sg.Canvas(key='-CANVAS-')]
]

layout = [
    [
        sg.Column(wybor_wykresu),
        sg.VSeperator(),
        sg.Column(wykres),
    ],
    [sg.Button('Exit')]
]

window = sg.Window('Pole Prędkości', layout, finalize=True,font='Helvetica 18',location=(0, 0),resizable=True)

window.Maximize()

window["-WYKRESY-"].update(set_to_index=0)

fig_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig1)

while True:

    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    if event == '-WYKRESY-':
        if fig_agg is not None:
            delete_fig_agg(fig_agg)
            window.Refresh()
        if values['-WYKRESY-'][0]=="Linie prądu":
            fig_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig1)
        elif(values['-WYKRESY-'][0]=="Tor elementu płynu"):
            fig_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig2)
        elif(values['-WYKRESY-'][0]=="Dywergencja"):
            fig_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig4)
        elif(values['-WYKRESY-'][0]=="Rotacja"):
            fig_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig3)

window.close()
