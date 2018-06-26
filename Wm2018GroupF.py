import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

eqip = ["GER", "SWE", "MEX", "KOR"]
status = [[(), (2, 1), (0, 1), ()], [(), (), (), (1, 0)], [(), (), (), (2, 1)], [(), (), (), ()]]

class teamStatus:

    points = 0
    diffGoals = 0
    goals = 0
    sumGoals = 0
    name = ""
    def __init__(self, n):
        self.name = n

    def toString(self):
        return self.name + ", " + str(self.goals) + ", " +str(self.diffGoals) + ", " + str(self.points)


def calcTable(table):
    for i in range(len(table)):
        for j in range(len(table)):
            g = status[i][j]
            if len(g) != 0:
                d = g[0] - g[1]
                table[i].goals += g[0]
                table[j].goals += g[1]
                table[i].diffGoals += d
                table[j].diffGoals -= d
                p0 = 3 if (g[0] > g[1]) else 1 if g[0] == g[1] else 0
                p1 = 3 if (g[1] > g[0]) else 1 if g[0] == g[1] else 0
                table[i].points += p0
                table[j].points += p1


def calcRank(table, k):
    rank = table[k].points * 100000 + table[k].diffGoals * 1000 + table[k].goals * 10
    return rank

#def calcDirektCompare(k1,k2):

def calcPlaceGER(table, norecursive = False):

    i = sorted(range(len(table)), key=lambda k: calcRank(table, k), reverse=True)
    pos = i.index(0)

    equallist = []
    for j in range(1,len(table)):
        if calcRank(table,0) == calcRank(table, j):
            equallist.append((j, i.index(j)))

    if len(equallist) == 0:
        return pos

    if norecursive:
        print("Fair play needed!")
        return pos

    equallist.insert(0,(0, pos))

    team = [i for i,pos in equallist]
    minitable = [teamStatus(eqip[i]) for i in team]
    calcTable(minitable)
    # print table
    print("minitable:")
    for e in minitable:
        print(e.toString())
    pos = calcPlaceGER(minitable, True) + min([e[1] for e in equallist])
    print("more eqal", equallist, "pl." , min([e[1] for e in equallist]), "ger:", pos)






    return pos




result = np.empty([14,14])

for i0 in range(7):
    for j0 in range(7):
        for i1 in range(7):
            for j1 in range(7):
                status[0][3] = (i0,j0)  ## GER -- KOR
                status[1][2] = (i1,j1)  ## SWE -- MEX
                table = [teamStatus(eqip[ii]) for ii in range(4)]
                calcTable(table)

                # print table
                for ii in range(4):
                    print(table[ii].toString())

                placeGER = calcPlaceGER(table)
                print("GER--KOR dif:", i0-j0, "SWE--MEX diff:", i1-j1, "is GER: ", placeGER + 1)
                x = i0-j0+6
                y = i1-j1+6
                result[x, y] = max(placeGER, result[x, y])

dz = []
x = []
y = []
color = []
for i in range(4,11):
    for j in range (4,11):

        dz.append(result[i, j]+1)
        c = '#00ceaa' if result[i, j] <= 1 else '#ceaa00'
        color.append(c)
        x.append(i-6)
        y.append(j-6)

# setup the figure and axes
fig = plt.figure(figsize=(8, 6))
ax1 = fig.gca(projection='3d')
dx = np.ones(len(x)) / 2
dy = np.ones(len(x)) / 2
z = np.zeros(len(x))

ax1.bar3d(x, y, z, dx, dy, dz, color, shade=True)
#ax1.view_init(ax1.elev, ax1.azim + 90)
ax1.set_xlabel("GER--KOR")
ax1.set_ylabel("SWE--MEX")
ax1.set_zticks([1,2,3,4])
plt.show()
