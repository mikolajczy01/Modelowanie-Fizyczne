import numpy as np
import sympy as sp
import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use('TkAgg')

sp.init_printing()
x,y = sp.symbols('x y')
h = sp.Symbol('h')
k = sp.Symbol('k')
def rozniczka_x(f):
    return (f.diff(x))

def rozniczka_y(f):
    return (f.diff(y))

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
            [sg.Button('Dalej')]]

window = sg.Window('Essa gaming', layout, finalize=True, element_justification='center',font='Helvetica 18')

event, wsp = window.read()

window.close()
#WYKRESIORY

fig = matplotlib.figure.Figure(figsize=(5, 4), dpi=200)
fig2 = matplotlib.figure.Figure(figsize=(5, 4), dpi=200)
fig3 = matplotlib.figure.Figure(figsize=(5, 4), dpi=200)

x1 = np.arange(0,1000)

wykresy = fig.add_subplot(1,1,1)
y1=x1
LiniePola(wykresy,x1,y1)



wykresy = fig2.add_subplot(1,1,1)
y1=x1**2+x1
LiniePola(wykresy,x1,y1)


wykresy = fig3.add_subplot(1,1,1)
y1=(x1**3)
LiniePola(wykresy,x1,y1)

Y,X = np.mgrid[0:20:100j,0:20:100j]
V,U = np.mgrid[0:20:100j,0:20:100j]

f = sp.integrate(sp.sympify(wsp[0]),x)
g = sp.integrate(sp.sympify(wsp[1]),y)
sp.pprint(g, use_unicode=True)
sp.pprint(f, use_unicode=True)

for i in range(3):
    for j in range(3):
        x1 = X[i,j]
        y1 = Y[i,j]
        U[i,j] = f.subs({x:x1, y:y1})
        V[i,j] = g.subs({x:x1, y:y1})

fig4 = plt.figure(figsize=(12, 7), dpi=200)

ax0 = fig4.add_subplot(1,1,1)
strm = ax0.streamplot(X, Y, U, V, density=1,color=V,cmap='winter',linewidth=1)
fig4.colorbar(strm.lines)
ax0.set_title('Varying Density')
ax0.grid(True)

#okno wykresiory

lista_wykresow = ["essa","lessa","julkakulka","Linie prądu"]

wybor_wykresu = [
    [sg.Text("Dostępne wykresy: ")],
    [
        sg.Listbox(
            values=lista_wykresow, enable_events=True, size=(40, 20), key="-WYKRESY-",
        )
    ]
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

window["-WYKRESY-"].update(set_to_index=3)

fig_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig4)

while True:

    event, values = window.read()

    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    if event == '-WYKRESY-':
        if fig_agg is not None:
            delete_fig_agg(fig_agg)
            window.Refresh()
        if values['-WYKRESY-'][0]=="essa":
            fig_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)
        elif(values['-WYKRESY-'][0]=="lessa"):
            fig_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig2)
        elif(values['-WYKRESY-'][0]=="julkakulka"):
            fig_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig3)
        elif(values['-WYKRESY-'][0]=="Linie prądu"):
            fig_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig4)

window.close()
