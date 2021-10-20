
import gradient as gr
import matplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
import math as m

# Funkcja rysująca mapę
def drawMap(mapa,nazwaPliku):
    fig = plt.figure()
    plt.imshow(mapa)
    plt.show()
    fig.savefig(nazwaPliku)

# Wczytywanie punktów na mapie oraz wyskości, szerokości mapy i dystansu między punktami
def loadMapPoints(fileName):
    with open(fileName) as file:
        mapa = file.read().splitlines()
    mapa = [i.split(' ') for i in mapa]
    mapHeight= int(mapa[0][0]) # wysokość mapy
    mapWidth = int(mapa[0][1]) # szerokość mapy
    distance = int(mapa[0][2]) # dystans pomiędzy punktami
    del mapa[0]
    for i in range(len(mapa)):
        del mapa[i][-1]
        mapa[i] = [ float(point) for point in mapa[i]] # Zamiana łańcucha znaków na float
    return mapa,mapWidth,mapHeight,distance

# Tworzenie macierzy kolorów HSV
def createHSVmatrix(mapHeight,mapWidth):
    hsvMatrix = []
    for i in range(mapHeight):
        hsvMatrix.append([])
        for j in range(mapWidth):
            hsvMatrix[i].append([0,1,1])
    return hsvMatrix


def simpleShading(mapa,mapHeight,mapWidth,distance):
    minimum = np.min(mapa)  # Minimum wysokości potrzebne do normalizacji
    maximum = np.max(mapa) - minimum# Maximum wyskokości potrzebne do normalizacji
    mapaHSV = createHSVmatrix(mapHeight, mapWidth)  # Macierz, która jest uzupełniana kolorami HSV na podstawie obliczeń
    for i in range(mapHeight):
        for j in range(mapWidth):
            # Obliczanie koloru między zielonym (120 - hue) a czerwonym (0)
            mapaHSV[i][j][0] = (1 - ((mapa[i][j] - minimum) / maximum)) * 120
            if j == 0:
                div = mapa[i][j] - mapa[i][j+1] # Różnica między wysokością punktu a jego prawym sąsiadem
            else:
                div = mapa[i][j] - mapa[i][j-1] # Różnica między wysokością punktu a jego lewym sąsiadem
            div = div*7 / maximum
            if div > 0:
                mapaHSV[i][j][1] -= abs(div)
            else:
                mapaHSV[i][j][2] -= abs(div)
            mapaHSV[i][j] = gr.hsv2rgb(mapaHSV[i][j][0], mapaHSV[i][j][1], mapaHSV[i][j][2])
    return mapaHSV

# Określanie koloru i cieniowania na podstawie kąta pomiędzy wektorem normalnym powierzchni a wektorem słońca
def vectorShading(mapa, mapHeight, mapWidth, distance):
    minimum = np.min(mapa) # Minimum wysokości potrzebne do normalizacji
    maximum = np.max(mapa) - minimum # Maximum wyskokości potrzebne do normalizacji
    sun = np.array([-distance, 50, -distance]) # Wektor słońca
    mapaHSV = createHSVmatrix(mapHeight,mapWidth) # Macierz, która jest uzupełniana kolorami HSV na podstawie obliczeń
    matrixOfAngles = np.zeros([mapHeight,mapWidth]) # Macierz kątów między słońcem a wektorem normalnym powierzchni
    for i in range(mapHeight):
        for j in range(mapWidth):
            # Określanie trójkąta w celu obliczenia wektora normalnego powierzchni
            mainPoint = np.array([i*distance,mapa[i][j],j*distance]) # Główny punkt trójkąta
            if i % 2 == 0:
                if j < mapWidth-1:
                    secondPoint = np.array([i*distance,mapa[i][j+1],distance*(j+1)]) # Drugi punkt trójkata
                    thirdPoint = np.array([(i+1)*distance,mapa[i+1][j],j*distance]) # Trzeci punkt trójkąta
                else:
                    secondPoint = np.array([i * distance, mapa[i][j - 1], distance * (j - 1)])# Drugi punkt trójkata
                    thirdPoint = np.array([(i + 1) * distance, mapa[i + 1][j], j * distance])# Trzeci punkt trójkata
            else:
                if j > 0:
                    secondPoint = np.array([i*distance,mapa[i][j-1],(j-1)*distance])# Drugi punkt trójkata
                    thirdPoint = np.array([(i-1)*distance,mapa[i-1][j],j*distance])# Trzeci punkt trójkata
                else:
                    secondPoint = np.array([i * distance, mapa[i][j + 1], (j + 1) * distance])# Drugi punkt trójkata
                    thirdPoint = np.array([(i - 1) * distance, mapa[i - 1][j], j * distance])# Trzeci punkt trójkata

            vectorToSun = sun - mainPoint # Wektor między punktem a słońcem
            normal = np.cross(secondPoint - mainPoint,thirdPoint - mainPoint) # Wektor normalny powierzchni. Prostopadły do powierzchni trójkąta
            # Obliczanie kąta między wektorem normalnym i wektorem słońca
            angleSun_Surface = m.degrees(np.arccos(np.clip(np.dot(normal,vectorToSun)/(np.linalg.norm(normal)*np.linalg.norm(vectorToSun)),-1,1)))
            matrixOfAngles[i][j] = angleSun_Surface
    # Posortowana lista kątów. Żeby lepiej uwidocznić cieniowanie
    angles = np.sort(np.reshape(matrixOfAngles,-1))
    minAngle = np.min(angles)
    maxAngle = np.max(angles)
    # Określanie stopnia przyciemnienia na podstawie odchyleń kąta.
    for i in range(mapHeight):
        for j in range(mapWidth):
            mapaHSV[i][j][0] = (1-((mapa[i][j]-minimum)/maximum))*120
            normalized = ((matrixOfAngles[i][j]-minAngle)/(maxAngle-minAngle))*2 - 1  # Otrzymanie kąta w zakresie <-1,1>
            position = np.where(angles == matrixOfAngles[i][j])[0] # Sprawdzenie jak bardzo odchylony jest kąt w stosunku do wszystkich kątów
            position = position[0]/len(angles)
            # Określenie S i V na podstawie pozycji kąta
            div = position - 0.5
            if div < 0:
                mapaHSV[i][j][1] = 1 -np.sin(matrixOfAngles[i][j])*abs(div)
            else:
                mapaHSV[i][j][2] = 1 - np.sin(matrixOfAngles[i][j])*abs(div)
            # Normalizowanie kąta i dodatkowe obliczenia uśredniające wynik
            if normalized < 0:
                mapaHSV[i][j][1] = ((1+normalized) + mapaHSV[i][j][1])/2
            else:
                mapaHSV[i][j][2] = ((1-normalized) + mapaHSV[i][j][2])/2
            # Zamiana HSV na RGB
            mapaHSV[i][j] = gr.hsv2rgb(mapaHSV[i][j][0],mapaHSV[i][j][1],mapaHSV[i][j][2])
    return mapaHSV

if __name__ == '__main__':
    mapa, mapHeight, mapWidth, distance = loadMapPoints("big.dem")
    mapaSimple = simpleShading(mapa,mapHeight,mapWidth,distance)
    drawMap(mapaSimple,"simpleMap.pdf")
    mapaVector = vectorShading(mapa, mapHeight, mapWidth, distance)
    drawMap(mapaVector,"vectorMap.pdf")
    plt.close()
