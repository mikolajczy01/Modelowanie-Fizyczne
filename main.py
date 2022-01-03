import numpy as np
import sympy as sp
import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use('TkAgg')
sp.init_printing()
x,y,z = sp.symbols('x y z',real = True)

def draw_figure(canvas, figure, loc=(0, 0)):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


def delete_fig_agg(fig_agg):
    fig_agg.get_tk_widget().forget()
    fig_agg.get_tk_widget().delete('all')

def LiniePola(wykres,x1,y1):
    for c in range(-100,100,1):
        wykres.plot(x1,y1+c, c=(0.5, 0.5, 0.5, 0.5))
    wykres.grid(True)
    wykres.set_xlim(0,20)
    wykres.set_ylim(0,20)

def rot(ux,uy,uz=0):
    A = sp.diff(sp.sympify(uz),y)-sp.diff(sp.sympify(uy),z)
    B = sp.diff(sp.sympify(ux),z)-sp.diff(sp.sympify(uz),x)
    C = sp.diff(sp.sympify(uy),x)-sp.diff(sp.sympify(uy),y)
    return A,B,C

def div(ux,uy,uz=0):
    A = sp.diff(sp.sympify(ux),x)
    B = sp.diff(sp.sympify(uy),y)
    C = sp.diff(sp.sympify(uz),z)
    return A+B+C

#okno pobieranie
sg.theme('DarkBlue1')
layout = [[sg.Text("Podaj Ux i Uy")],
            [sg.Text("Ux ="),sg.InputText()],
            [sg.Text("Uy ="),sg.InputText()],
            # [sg.Text("Xo ="),sg.InputText()],
            # [sg.Text("Yo ="),sg.InputText()],
            [sg.Button('Dalej')]]
window = sg.Window('Pole Prędkości', layout, finalize=True, element_justification='center',font='Helvetica 18')

event, wsp = window.read()

window.close()
#WYKRESIORY


# wykres linii prądu
Y,X = np.mgrid[1:20:100j,1:20:100j]
V,U = np.mgrid[1:20:100j,1:20:100j]
diver,miver = np.mgrid[1:20:100j,1:20:100j]

f = sp.integrate(1/sp.sympify(wsp[0]),x)
g = sp.integrate(1/sp.sympify(wsp[1]),y)
wynik = sp.sympify(sp.solve(sp.Eq(f,g),y))

# sp.pprint(f, use_unicode=True)
# sp.pprint(g, use_unicode=True)
# sp.pprint(wynik[0], use_unicode=True)

for i in range(100):
    for j in range(100):
        V[i, j] = wynik[0].subs({x: X[i, j]})
        diver[i, j] = sp.sympify(div(wsp[0], wsp[1])).subs({x: X[i, j]})

fig1 = plt.figure(figsize=(12, 7), dpi=200)

ax0 = fig1.add_subplot(1,1,1)
strm = ax0.streamplot(X, Y, X, V, density=1,color=diver,cmap='winter',linewidth=1)
fig1.colorbar(strm.lines)
ax0.set_title('Linie prądu')
ax0.grid(True)

#wykres toru

X=np.linspace(1,20,100)
Y=np.linspace(1,20,100)

f = sp.integrate(1/sp.sympify(wsp[0]),x)
g = sp.integrate(1/sp.sympify(wsp[1]),y)
wynik = sp.sympify(sp.solve(sp.Eq(f,g),y))

for i in range(100):
        Y[i]=wynik[0].subs({x: X[i]})

fig2 = plt.figure(figsize=(12, 7), dpi=200)

ax0 = fig2.add_subplot(1,1,1)
strm = ax0.plot(X, Y)
# print(X[50])
# print(Y[50])
# print(X[51])
# print(Y[51])
# ax0.arrow(X[50],Y[50],X[51]-X[50],Y[51]-Y[50], shape='full', lw=0, length_includes_head=True)
ax0.set_title('Tor elementu płynu')
ax0.grid(True)

#wykres roatcji
fig3 = plt.figure(figsize=(12,7),dpi=200)
ax0 = fig3.add_subplot(1,1,1,projection='3d')
X,Y,Z=np.meshgrid(np.arange(1, 20),np.arange(1, 20),np.arange(1, 20))
U,V,W = rot(wsp[0],wsp[1])

strm=ax0.quiver(X,Y,Z,U,V,W)
ax0.set_title('Rotacja')
ax0.grid(True)

#progressbar
sg.theme('DarkGrey8')
progressbar = [
    [sg.ProgressBar(1000, orientation='h', size=(50, 20), key='progressbar')]
]

layout = [
    [sg.Frame('Wczytywanie',layout= progressbar)],
    [sg.Submit('Start'),sg.Cancel()]
]
window = sg.Window('Pole prędkości', layout)
progress_bar = window['progressbar']
while True:
    event, values = window.read(timeout=10)
    if event == 'Cancel'  or event is None:
        break
    elif event == 'Start':
        for i in range(0,1000):
            progress_bar.UpdateBar(i + 1)
        window.close()

#okno wykresiory
sg.theme('DarkBlue2')
lista_wykresow = ["Linie prądu","Tor elementu płynu","Rotacja"]

wybor_wykresu = [
    [sg.Text("Dostępne wykresy: ")],
    [sg.Listbox(values=lista_wykresow, enable_events=True, size=(40, 20), key="-WYKRESY-")]
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

window = sg.Window('Pole Prędkości', layout, finalize=True, element_justification='center',font='Helvetica 18',location=(0, 0),resizable=True)

window["-WYKRESY-"].update(set_to_index=0)

fig_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig1)

while True:

    event, values = window.read()

    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    if event == '-WYKRESY-':
        if fig_agg is not None:
            delete_fig_agg(fig_agg)
            window.Refresh()
        if values['-WYKRESY-'][0]=="Linie prądu":
            fig_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig1)
        elif(values['-WYKRESY-'][0]=="Tor elementu płynu"):
            fig_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig2)
        elif(values['-WYKRESY-'][0]=="Rotacja"):
            fig_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig3)
window.close()
