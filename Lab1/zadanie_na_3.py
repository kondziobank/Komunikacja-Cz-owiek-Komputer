import matplotlib.pyplot as plt


def mean(l):
    l = list(l)
    return sum(l) / len(l)


names = [
    '1-Coev-RS',
    '1-Coev',
    '1-Evol-RS',
    '2-Coev',
    '2-Coev-RS'
]

files = [
    'cel-rs.csv',
    'cel.csv',
    'rsel.csv',
    '2cel.csv',
    '2cel-rs.csv'
]

colors = [
    '#00ff00',
    '#000000',
    '#0000ff',
    '#ff8da1',
    '#ff0000'
]

plt.figure(figsize=(6.7, 6.7))
plt.tick_params(top=True, right=True, bottom=True, left=True, direction='in')
plt.xlim((0, 200))
plt.ylim((0.6, 1))

for i in range(len(files)):
    nameOfAlgorithm = names[i]
    nameOfDataset = files[i]
    color = colors[i]

    x = []
    y = []
    file = open(nameOfDataset).read().strip().split('\n')
    for line in file[1:]:
        data = line.split(',')
        x.append(float(data[0]))
        y.append(mean(map(float, data[2:])))

    plt.plot(x, y, label=nameOfAlgorithm, linewidth=0.9, color=color)

plt.xlabel('Rozegranych gier')
plt.ylabel('Odsetek wygranych gier')
plt.legend(fontsize='xx-large', loc='lower right', fancybox=False)
plt.show()
