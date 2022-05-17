import cv2
import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from tkinter.filedialog import askopenfilename
import os
import sys
import shutil
from sys import platform as sys_pf
# Matplotlib para Mac
if sys_pf == 'darwin':
    import matplotlib
    matplotlib.use("TkAgg")
    import matplotlib.pyplot as plt


class LineBuilder:

    def __init__(self, line, ax, color):
        self.line = line
        self.ax = ax
        self.color = color
        self.xs = []
        self.ys = []
        self.cid = line.figure.canvas.mpl_connect('button_press_event', self)
        self.counter = 0
        self.shape_counter = 0
        self.shape = {}
        self.precision = 10
        self.array = []

    def __call__(self, event):
        global polyarray
        global captura
        global nomeaqv
        print(self.array)
        if event.inaxes != self.line.axes:
            return
        if self.counter == 0:
            self.xs.append(event.xdata)
            xglobal = int(event.xdata)
            print("Coordenada X:", xglobal)
            self.ys.append(event.ydata)
            yglobal = int(event.ydata)
            print("Coordenada Y:", yglobal)
            self.array.append((int(xglobal), int(yglobal)))
            polyarray = np.array(self.array)
            print("Array:", self.array)
        if np.abs(event.xdata - self.xs[0]) <= self.precision and np.abs(
                event.ydata - self.ys[0]) <= self.precision and self.counter != 0:
            self.xs.append(self.xs[0])
            self.ys.append(self.ys[0])
            self.ax.scatter(self.xs, self.ys, s=120, color=self.color)
            self.ax.scatter(self.xs[0], self.ys[0], s=80, color='blue')
            self.ax.plot(self.xs, self.ys, color=self.color)
            self.line.figure.canvas.draw()
            self.shape[self.shape_counter] = [self.xs, self.ys]
            self.shape_counter = self.shape_counter + 1
            self.xs = []
            self.ys = []
            self.counter = 0

        else:
            if self.counter != 0:
                self.xs.append(event.xdata)
                xglobal = int(event.xdata)
                print("Coordenada X:", xglobal)
                self.ys.append(event.ydata)
                yglobal = int(event.ydata)
                print("Coordenada Y:", yglobal)
                self.array.append((int(event.xdata),int(event.ydata)))
                polyarray = self.array
                print("Array: ", self.array)
                nomefortext = str(nome)
                nomefin = nomefortext.split('.')
                nomeaqv = (nomefin[0]+".mask")
                print(nomeaqv)
                arq = open(nomeaqv, "w")
                arq.write(str(polyarray))
            self.ax.scatter(self.xs, self.ys, s=120, color=self.color)
            self.ax.plot(self.xs, self.ys, color=self.color)
            self.line.figure.canvas.draw()
            self.counter = self.counter + 1


def create_shape_on_image(data, cmap='jet'):
    def change_shapes(shapes):
        new_shapes = {}
        for i in range(len(shapes)):
            l = len(shapes[i][1])
            new_shapes[i] = np.zeros((l, 2), dtype='int')
            for j in range(l):
                new_shapes[i][j, 0] = shapes[i][0][j]
                new_shapes[i][j, 1] = shapes[i][1][j]
        return new_shapes

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_title('Máscara de Video')
    line = ax.imshow(data)
    ax.set_xlim(0, data[:, :, 0].shape[1])
    ax.set_ylim(0, data[:, :, 0].shape[0])
    linebuilder = LineBuilder(line, ax, 'red')
    plt.gca().invert_yaxis()
    plt.imshow(gframe)
    plt.show()
    new_shapes = change_shapes(linebuilder.shape)
    return new_shapes

def video():
    global gframe
    global nome
    refPt = []
    Tk().withdraw()
    filename = askopenfilename()
    nome = os.path.basename(filename)
    cap = cv2.VideoCapture(filename)
    ret, gframe = cap.read()
    captura = cap
    shapes = create_shape_on_image(gframe)[0]

def escolheraqv():
    janela = Tk()
    vjanela = Canvas
    janela.geometry("200x140+250+250")
    b1 = Button(janela, text="Ler uma Mascara", command=read_mask)
    b1.pack()
    b = Button(janela, text="Escolher Video", command=video)
    b.pack()
    opwin = Button(janela, text="Criar Poligono", command=mostrarpoli)
    opwin.pack()
    save = Button(janela, text="Salvar Mascara", command=savefunc)
    save.pack()
    b2 = Button(janela, text="Finalizar", command=sys.exit)
    b2.pack()
    janela.mainloop()

def mostrarpoli():
    polygon_creator()

def polygon_creator():
    print("Criando Poligono")
    recb = polyarray
    poly = np.array([recb], dtype=np.int32)
    mask_new = np.zeros_like(gframe)
    cv2.fillPoly(mask_new, poly, 255)
    mask_new = cv2.cvtColor(mask_new, cv2.COLOR_BGR2GRAY)
    plt.imshow(mask_new)
    plt.show()
    cv2.destroyAllWindows()
    captura.release()


def read_mask():
    nomefortext = str(nome)
    nomefin = nomefortext.split('.')
    nomeaqv = (nomefin[0] + ".mask")
    arq = open(nomeaqv, 'r', encoding="utf8")
    texto = arq.read()
    for linha in texto:
        print(linha, end="")
    arq.close()


def savefunc():
    nomefortext = str(nome)
    nomefin = nomefortext.split('.')
    nomeaqv = (nomefin[0] + ".mask")
    print(nomeaqv)

escolheraqv()
polygon_creator()
