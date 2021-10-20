#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
import math as m

from matplotlib import colors

# Liczba próbek w gradiencie
samples = 1024
# Lista punktów tworząca odcinki na sześcianie
rgbBw = [[0,0,0],[1,1,1]]
rgbGbr = [[0,1,0],[0,0,1],[1,0,0]]
rgbGbrFull = [[0,1,0],[0,1,1],[0,0,1],[1,0,1],[1,0,0]]
rgbWbCustom = [[1,1,1],[1,0,1],[0,0,1],[0,1,1],[0,1,0],[1,1,0],[1,0,0],[0,0,0]]
# Lista punktów tworzących odcinki na stożku
hsvBw = [[0,0,0],[0,0,1]]
hsvGBR = [[120,1,1],[180,1,1],[240,1,1],[300,1,1],[360,1,1]]
hsvUnknown = [[120,0.5,1],[60,0.5,1],[0,0.5,1]]
hsvCustom = [[0,1,1],[120,0.9,1],[180,0.7,1],[240,0.5,1],[300,0.3,1],[310,0,1]]

# Funkcja sprawdza w jakim miejscu sześcianu znajduje się punkt na podstawie listy odcinków
def getPointInCube(listPoints,point):
    # Sprawdzanie, na którym odcinku znajduje się punkt
    element, skala = getElement(listPoints, point)
    finalPoint = []
    for i in range(len(listPoints[element])):
        lewyZakres = listPoints[element][i] # lewy koniec odcinka
        prawyZakres = listPoints[element + 1][i] # prawy koniec odcinka
        div = prawyZakres - lewyZakres
        if div != 0:
            finalPoint.append(lewyZakres + (1 / (div)) * skala) # Na podstawie wzoru Talesa
        else:
            finalPoint.append(lewyZakres) # Uniknięcie dzielenia przez 0
    return finalPoint

#  Funkcja sprawdza, na którym odcinku znajduje się punkt
def getElement(listPoints, point):
    element = m.trunc(point * (len(listPoints) - 1))
    if element == len(listPoints) - 1:
        element = len(listPoints) - 2
    skala = point * (len(listPoints) - 1) - element
    return element, skala

# Funkcja sprawdza w jakim miejscu stożka znajduje się punkt
def getPointInCone(listPoints,point):
    element,skala = getElement(listPoints,point)
    finalPoint = []
    for i in range(len(listPoints[element])):
        lewyZakres = listPoints[element][i] # lewy koniec odcinka
        prawyZakres = listPoints[element + 1][i] # prawy koniec odcinka
        div = prawyZakres - lewyZakres
        finalPoint.append(lewyZakres + div * skala)
    return finalPoint


def plot_color_gradients(gradients, names):
    rc('legend', fontsize=10)
    column_width_pt = 400
    pt_per_inch = 72
    size = column_width_pt / pt_per_inch
    fig, axes = plt.subplots(nrows=len(gradients), sharex=True, figsize=(size, 0.75 * size))
    fig.subplots_adjust(top=1.00, bottom=0.05, left=0.25, right=0.95)

    for ax, gradient, name in zip(axes, gradients, names):

        img = np.zeros((2, samples, 3))
        for i, v in enumerate(np.linspace(0, 1, samples)):
            img[:, i] = gradient(v)
        # wizualizacja z interpolacją
        # im = ax.imshow(img, aspect='auto')
        # Interpolacja została wyłączona, żeby lepiej zwizualizować zmiany w liczbie próbek
        im = ax.imshow(img, aspect='auto',interpolation='none')
        im.set_extent([0, 1, 0, 1])
        ax.yaxis.set_visible(False)

        pos = list(ax.get_position().bounds)
        x_text = pos[0] - 0.25
        y_text = pos[1] + pos[3]/2.
        fig.text(x_text, y_text, name, va='center', ha='left', fontsize=10)
    fig.savefig('my-gradients1024.pdf')
    plt.close()

# Funkcja konwertuje z hsv do rgb
def hsv2rgb(h, s, v):
    vs = v*s
    if h > 0:
        while h > 360:
            h -= 360
    else:
        while h < 0:
            h += 360
    hue = h/60
    x = vs * (1 - abs((hue % 2) -1))
    # W zależności od tego w jakiej cześci okręgu się znajduje kolor
    switcher = {
        0: [vs,x,0],
        1: [x,vs,0],
        2: [0,vs,x],
        3: [0,x,vs],
        4: [x,0,vs],
        5: [vs,0,x],
        6: [vs,x,0]
    }
    rgb = switcher.get(m.trunc(hue),[0,0,0])
    match = v-vs
    rgb = [i+match for i in rgb]
    return rgb

def gradient_rgb_bw(v):
   return getPointInCube(rgbBw,v)

def gradient_rgb_gbr(v):
    return getPointInCube(rgbGbr,v)

def gradient_rgb_gbr_full(v):
    return getPointInCube(rgbGbrFull,v)

def gradient_rgb_wb_custom(v):
    #TODO
    return getPointInCube(rgbWbCustom,v)

def gradient_hsv_bw(v):
    hsv = getPointInCone(hsvBw,v)
    return hsv2rgb(hsv[0], hsv[1], hsv[2])

def gradient_hsv_gbr(v):
    hsv = getPointInCone(hsvGBR,v)
    return hsv2rgb(hsv[0], hsv[1], hsv[2])

def gradient_hsv_unknown(v):
    hsv = getPointInCone(hsvUnknown, v)
    return hsv2rgb(hsv[0], hsv[1], hsv[2])


def gradient_hsv_custom(v):
    hsv = getPointInCone(hsvCustom, v)
    return hsv2rgb(hsv[0], hsv[1], hsv[2])

if __name__ == '__main__':
    def toname(g):
        return g.__name__.replace('gradient_', '').replace('_', '-').upper()

    gradients = (gradient_rgb_bw, gradient_rgb_gbr, gradient_rgb_gbr_full, gradient_rgb_wb_custom,
                 gradient_hsv_bw, gradient_hsv_gbr, gradient_hsv_unknown, gradient_hsv_custom)

    plot_color_gradients(gradients, [toname(g) for g in gradients])

