import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

eqip = ["GER", "SWE", "MEX", "KOR"]
status = [[(), (2, 1), (0, 1), ()], [(), (), (), (1, 0)], [(), (), (), (2, 1)], [(), (), (), ()]]



def calcPlaceD():

    teamStatus = [[0, 0], [0, 0], [0, 0], [0, 0]]
    for i in range(4):
        for j in range(4):
            g = status[i][j]
            if len(g) != 0:
                d = g[0] - g[1]
                teamStatus[i][0] += d
                teamStatus[j][0] -= d
                p0 = 3 if (g[0] > g[1]) else 1 if g[0] == g[1] else 0
                p1 = 3 if (g[1] > g[0]) else 1 if g[0] == g[1] else 0
                teamStatus[i][1] += p0
                teamStatus[j][1] += p1

    l = sorted(range(len(teamStatus)), key=lambda k: teamStatus[k][1] * 100 + teamStatus[k][0])
    pos = 3-l.index(0)

    return pos


placeD = calcPlaceD()
print("GER now", placeD)

dz = []
x = []
y = []
color = []

for i in range(7):
    for j in range(7):
        status[0][3] = (3 - i, 0)  ## GER -- KOR
        status[1][2] = (3 - j, 0)  ## SWE -- MEX
        placeD = calcPlaceD()
        print("GER--KOR dif:", 3 - i, "SWE--MEX diff:", 3 - j, "is GER: ", placeD + 1)
        dz.append(placeD+1)
        c = '#00ceaa' if placeD <= 1 else '#ceaa00'
        color.append(c)
        x.append(3 - i)
        y.append(3 - j)

# setup the figure and axes
fig = plt.figure(figsize=(8, 6))
ax1 = fig.gca(projection='3d')
dx = np.ones(len(x)) / 2
dy = np.ones(len(x)) / 2
z = np.zeros(len(x))

ax1.bar3d(x, y, z, dx, dy, dz, color, shade=True)
ax1.view_init(ax1.elev, ax1.azim + 90)
ax1.set_xlabel("GER--KOR")
ax1.set_ylabel("SWE--MEX")
ax1.set_zticks([1,2,3,4])
plt.show()
