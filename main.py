import numpy as np
import sympy as sp
import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use('TkAgg')

sp.init_printing()
x,y = sp.symbols('x y')

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

#okno pobieranie
layout = [[sg.Text("Wykres wariacie")],
            [sg.Text("Ux ="),sg.InputText()],
            [sg.Text("Uy ="),sg.InputText()],
            [sg.Text("Xo ="),sg.InputText()],
            [sg.Text("Yo ="),sg.InputText()],
            [sg.Button('Dalej')]]

window = sg.Window('Essa gaming', layout, finalize=True, element_justification='center',font='Helvetica 18')

event, wsp = window.read()

window.close()
#WYKRESIORY

#wykres linii prądu
Y,X = np.mgrid[1:20:100j,1:20:100j]
V,U = np.mgrid[1:20:100j,1:20:100j]

f = sp.integrate(1/sp.sympify(wsp[0]),x)
g = sp.integrate(1/sp.sympify(wsp[1]),y)
#
wynik = sp.sympify(sp.solve(sp.Eq(f,g),y))

sp.pprint(f, use_unicode=True)
sp.pprint(g, use_unicode=True)
sp.pprint(wynik[0], use_unicode=True)

for i in range(100):
    for j in range(100):
        x1 = X[i,j]
        y1 = Y[i,j]
        V[i, j] = wynik[0].subs({x: x1, y: y1})

fig1 = plt.figure(figsize=(12, 7), dpi=200)

ax0 = fig1.add_subplot(1,1,1)
strm = ax0.streamplot(X, Y, X, V, density=1,color=V,cmap='winter',linewidth=1)
fig1.colorbar(strm.lines)
ax0.set_title('Varying Density')
ax0.grid(True)

#wykres toru

Y,X = np.mgrid[1:20,1:20]
V,U = np.mgrid[1:20,1:20]

f = sp.integrate(sp.sympify(wsp[0]),x)
g = sp.integrate(sp.sympify(wsp[1]),y)
# sp.pprint(g, use_unicode=True)
# sp.pprint(f, use_unicode=True)

for i in range(19):
    for j in range(19):
        x1 = X[i,j]
        y1 = Y[i,j]
        U[i,j] = sp.sympify(wsp[0]).subs({x:x1, y:y1})
        V[i,j] = sp.sympify(wsp[1]).subs({x:x1, y:y1})

fig2 = plt.figure(figsize=(12, 7), dpi=200)

ax0 = fig2.add_subplot(1,1,1)
strm = ax0.streamplot(X, Y, U, V, density=1,color=V,cmap='winter',linewidth=1)
fig2.colorbar(strm.lines)
ax0.set_title('Varying Density')
ax0.grid(True)

#okno wykresiory

lista_wykresow = ["Linie prądu","Tor elementu płynu"]

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

window = sg.Window('Essa gaming', layout, finalize=True, element_justification='center',font='Helvetica 18',location=(0, 0),resizable=True)

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
window.close()
