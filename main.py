import numpy as np
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

#okno pobieranie
layout = [[sg.Text("Wykres wariacie")],
            [sg.Text("a ="),sg.Input()],
            [sg.Text("b ="),sg.Input()],
            [sg.Button('Dalej')]]

window = sg.Window('Essa gaming', layout, finalize=True, element_justification='center',font='Helvetica 18')

event, wsp = window.read()

window.close()

#WYKRESIORY

fig = matplotlib.figure.Figure(figsize=(5, 4), dpi=100)
fig2 = matplotlib.figure.Figure(figsize=(5, 4), dpi=100)
wykresy = fig.add_subplot(1,1,1)
x = np.arange(-10,11,1)

wykresy.plot(x,x*float(wsp[0])+float(wsp[1]))
wykresy.grid(True)


wykresy = fig2.add_subplot(1,1,1)
wykresy.plot(x,x*2)
wykresy.grid(True)

#okno wykresiory

lista_wykresow = ["essa","lessa"]

wybor_wykresu = [
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

window = sg.Window('Essa gaming', layout, finalize=True, element_justification='center',font='Helvetica 18',location=(0, 0),)

window["-WYKRESY-"].update(set_to_index=0)

fig_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)

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
        else:
            fig_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig2)

window.close()
