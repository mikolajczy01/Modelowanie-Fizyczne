import numpy as np
import sympy as sp
import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use('TkAgg')

def draw_figure(canvas, figure, loc=(0, 0)):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


def delete_fig_agg(fig_agg):
    fig_agg.get_tk_widget().forget()
    fig_agg.get_tk_widget().delete('all')

def LiniePola(wykres,x,y):
    for c in range(-100,100,1):
        wykres.plot(x,y+c, c=(0.5, 0.5, 0.5, 0.5))
    wykres.grid(True)
    wykres.set_xlim(0,20)
    wykres.set_ylim(0,20)

#okno pobieranie
layout = [[sg.Text("Wykres wariacie")],
            [sg.Text("Ux ="),sg.Input()],
            [sg.Text("Uy ="),sg.Input()],
            [sg.Button('Dalej')]]

window = sg.Window('Essa gaming', layout, finalize=True, element_justification='center',font='Helvetica 18')

event, wsp = window.read()

window.close()

#WYKRESIORY

fig = matplotlib.figure.Figure(figsize=(5, 4), dpi=200)
fig2 = matplotlib.figure.Figure(figsize=(5, 4), dpi=200)
fig3 = matplotlib.figure.Figure(figsize=(5, 4), dpi=200)

x = np.arange(0,1000)

wykresy = fig.add_subplot(1,1,1)
y=x*float(wsp[0])+float(wsp[1])
LiniePola(wykresy,x,y)



wykresy = fig2.add_subplot(1,1,1)
y=x**2+x
LiniePola(wykresy,x,y)


wykresy = fig3.add_subplot(1,1,1)
y=(x**3)+float(wsp[0])
LiniePola(wykresy,x,y)

Y, X = np.mgrid[0:3,0:3]
U = X+1
V = Y**2

print(X)
print(Y)
print(U)
print(V)

fig4 = plt.figure(figsize=(12, 7), dpi=200)

ax0 = fig4.add_subplot(1,1,1)
strm = ax0.streamplot(X, Y, U, V, density=2,color=V,cmap='winter',linewidth=1)
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
