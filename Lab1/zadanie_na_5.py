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

markers = 'ovDsd'


plt.figure(figsize=(6.7, 6.7))
plt.subplot(1, 2, 1)
plt.tick_params(top=True, right=True, bottom=True, left=True, direction='in')

plt.rcParams['font.serif'] = ['Times New Roman'] + plt.rcParams['font.serif']


plt.ylim((60, 100))
plt.xlim((0, 500))

for i in range(len(colors)):
    plotName = names[i]
    nameOfDataset = files[i]
    color = colors[i]
    marker = markers[i]

    x = []
    y = []
    file = open(nameOfDataset).read().strip().split('\n')
    for line in file[1:]:
        data = line.split(',')
        x.append(float(data[1]) / 1000)
        y.append(100 * mean(map(float, data[2:])))

    plt.plot(x, y, color=color, marker=marker, markevery=25,
             markeredgecolor='black', linewidth=1, label=plotName)

plt.grid(True, dashes=(1, 7), linestyle=':')
plt.legend(loc='lower right', edgecolor='0.3', numpoints=2)
plt.xlabel('Rozegranych gier (x1000)')
plt.ylabel('Odsetek wygranych gier [%]')

top = plt.gca().twiny()
top.set_xticks(list(range(0, 201, 40)))
top.set_xlabel('Pokolenie')
plt.subplot(1, 2, 2)

plt.grid(True, dashes=(1, 7), linestyle=':')
plt.tick_params(top=True, right=True, bottom=True, left=True, direction='in')
plt.gca().yaxis.set_label_position("right")
plt.gca().yaxis.tick_right()

BOXPLOT = {}
for i in range(len(files)):
    nameOfDataset = files[i]
    nameOfAlgorithm = names[i]

    file = open(nameOfDataset).read().strip().split('\n')

    BOXPLOT[nameOfAlgorithm] = []
    for value in file[-1].split(',')[2:]:
        BOXPLOT[nameOfAlgorithm].append(float(value) * 100)


plt.boxplot(BOXPLOT.values(), 1, medianprops={'color': 'r'}, boxprops={'color': 'b'}, showmeans=True,
            flierprops={'marker': '+', 'markeredgecolor': 'b'}, capprops={'color': 'b'},
            meanprops={'marker': 'o', 'markerfacecolor': 'b',
                       'markeredgecolor': '0', 'markeredgewidth': 1},
            whiskerprops={'linestyle': '--', 'color': 'b', 'dashes': (4, 4)}
            )
ax = plt.gca()
ax.set_xticklabels(BOXPLOT.keys(), rotation=18)
plt.ylim((60, 100))
plt.show()
