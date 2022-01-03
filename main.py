import numpy as np
import sympy as sp
import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib

matplotlib.use('TkAgg')
sp.init_printing()
x,y,z = sp.symbols('x y z')
#progressbar
def bar(n,i,j,k):
    sg.theme('DarkGrey8')
    progressbar = [
        [sg.ProgressBar(n,orientation='h', size=(50, 20), key='progressbar')]
    ]

    layout =[
        [sg.Frame('Wczytywanie',layout= progressbar)],
        [sg.Cancel()]
    ]
    window = sg.Window('Pole prędkości', layout,no_titlebar=True, alpha_channel=1, grab_anywhere=True)
    progress_bar = window['progressbar']
    while True:
        event, values = window.read(timeout=10)
        if event == 'Cancel' or event is None:
            break
        else:
            for i in range(0, n):
                progress_bar.UpdateBar(i + j+k)
        window.close()
    return progress_bar
def draw_figure(canvas, figure, loc=(0, 0)):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def delete_fig_agg(fig_agg):
    fig_agg.get_tk_widget().forget()
    fig_agg.get_tk_widget().delete('all')

def rotX(uy,uz=0):
    A = sp.diff(sp.sympify(uz),y)-sp.diff(sp.sympify(uy),z)
    return A

def rotY(ux,uz=0):
    B = sp.diff(sp.sympify(ux), z) - sp.diff(sp.sympify(uz), x)
    return B

def rotZ(ux,uy):
    C = sp.diff(sp.sympify(uy), x) - sp.diff(sp.sympify(ux), y)
    return C

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

sp.pprint(f, use_unicode=True)
sp.pprint(g, use_unicode=True)
sp.pprint(wynik[0], use_unicode=True)

progressbar=bar(10000,100,100,0)
for i in range(100):
    for j in range(100):
        V[i, j] = wynik[0].subs({x: X[i, j]})
        diver[i, j] = sp.sympify(div(wsp[0], wsp[1])).subs({x: X[i, j], y: Y[i, j]})
        progressbar.UpdateBar(i * 100 + j)

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

progressbar(1000,100,0)
for i in range(100):
        Y[i]=wynik[0].subs({x: X[i]})
        progressbar.UpdateBar(i)
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
X,Y,Z = np.meshgrid(np.arange(1,20),np.arange(1,20),np.arange(1,20))
U,V,W = np.meshgrid(np.arange(1,20),np.arange(1,20),np.arange(1,20))

wynikx = sp.sympify(rotX(wsp[1]))
wyniky = sp.sympify(rotY(wsp[0]))
wynikz = sp.sympify(rotZ(wsp[0],wsp[1]))

sp.pprint(wynikx, use_unicode=True)
sp.pprint(wyniky, use_unicode=True)
sp.pprint(wynikz, use_unicode=True)

progressbar(8000,20,20,20)

for i in range(19):
    for j in range(19):
        for k in range(19):
            U[i, j, k]=wynikx.subs({z: Z[i, j], y: Y[i, j],x: X[i,j]})
            V[i, j, k]=wyniky.subs({z: Z[i, j], y: Y[i, j],x: X[i,j]})
            W[i, j, k]=wynikz.subs({z: Z[i, j], y: Y[i, j],x: X[i,j]})
            progressbar.UpdateBar(i*20+j*20+k)
strm=ax0.quiver(X,Y,Z,U,V,W, length=0.1)
ax0.set_title('Rotacja')
ax0.grid(True)

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
