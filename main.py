import numpy as np
import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use('TkAgg')

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

#okno pobieranie
layout = [[sg.Text("Wykres wariacie")],
            [sg.Text("a ="),sg.Input()],
            [sg.Text("b ="),sg.Input()],
            [sg.Button('Dalej')]]

window = sg.Window('Essa gaming', layout, finalize=True, element_justification='center',font='Helvetica 18')

event, wsp = window.read()

window.close()

#wykresiory
# x = np.arange(-10,11,1)
#plt.subplot(1)
# plt.grid(True)
plt.xlim(-10, 10)

fig = matplotlib.figure.Figure(figsize=(16, 9), dpi=100)
x = np.arange(-10,11,1)

wykresy = fig.add_subplot(1,1,1)
wykresy.plot(x,x*float(wsp[0])+float(wsp[1]))
wykresy.grid(True)


# wykresy = fig.add_subplot(1,2,2)
# wykresy.plot(x,x*float(wsp[1])+float(wsp[0]))
# wykresy.grid(True)

#okno wykresiory
wybor_wykresu = [
    [
        sg.Listbox(
            values=["essa","lessa"], enable_events=True, size=(40, 20), key="-FILE LIST-"
        )
    ],
]

wykres = [
    [sg.Text('Wykresior')],
    [sg.Canvas(key='CANVAS')]
]

layout = [
    [
        sg.Column(wybor_wykresu),
        sg.VSeperator(),
        sg.Column(wykres),
    ]
]

window = sg.Window('Essa gaming', layout, finalize=True, element_justification='center',font='Helvetica 18',location=(0, 0),)

fig_canvas_agg = draw_figure(window['CANVAS'].TKCanvas, fig)

while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

window.close()
