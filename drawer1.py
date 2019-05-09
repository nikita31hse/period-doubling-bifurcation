import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Slider


class Point:
    X = 0
    Y = 0
    IsOnCurve = False

    def __init__(self, _x, _y, isoncurve=False):
        self.X = _x
        self.Y = _y
        self.IsOnCurve = isoncurve


def arange(start, finish, d):
    while start <= finish:
        yield start
        start += d


def F(x):
    global mu
    return 4 * mu * x * (1 - x)


DRAWING_POINT = 8
f_in = open("data.txt", "r")
start_x, mu = map(float, f_in.readline().split())

fig, ax = plt.subplots(figsize=(10, 6))
fig.subplots_adjust(left=0.05, right=0.8)
##ax.set_facecolor('#eafff5')
line, = ax.plot([], [], lw=2, color="#FF0000", label="line")
ax.set_ylim(0, 1)
ax.set_xlim(0, 1)
point_path = []
##ax.plot(xdata, ydata, color='#000000')
text = fig.text(0.82, 0.6, 'Try this values:\n  $\mu_1$=0.5\n  $\mu_2$=0.8\n  $\mu_3$=0.87\n  $\mu_4$=0.89\n  $\mu_5$=0.8915\n  $\mu_6$=0.95', size=14)
text = fig.text(0.25, 0.9, 'Period doubling bifurcation', size=20)


xarr = list(arange(0, 1.01, 0.01))
yarr = []
for num in xarr:
    yarr.append(4 * mu * num * (1 - num))
ax.plot(xarr, yarr, color='#000000')

path = [Point(start_x, F(start_x), True), Point(F(start_x), F(start_x))]
Length = 1000000
frame = 0

for i in range(Length):
    path.extend([Point(path[-1].X, F(path[-1].X), True), Point(F(path[-1].X), F(path[-1].X))])


def run(data):
    global frame, point_path

    point_path.append(path[frame])

    if len(point_path) > 2 * DRAWING_POINT:
        point_path = point_path[2:] ##/2

    if len(point_path) <= DRAWING_POINT:
        line.set_data(list(map(lambda P: P.X, point_path)), list(map(lambda P: P.Y, point_path)))
    else:
        line.set_data(list(map(lambda P: P.X, point_path))[len(point_path) - DRAWING_POINT:],
                      list(map(lambda P: P.Y, point_path))[len(point_path) - DRAWING_POINT:])

    for p_index in range(len(point_path)):
        p = point_path[p_index]
        if p.IsOnCurve:
            ax.scatter(p.X, p.Y, color="#FFFFFF", s=80)
            ax.scatter(p.X, p.Y, color="#0000FF", s=60, alpha=p_index / len(point_path))

    if len(ax.collections) >= 2 * DRAWING_POINT:
        ax.collections = ax.collections[len(ax.collections) - 2 * DRAWING_POINT:]

    frame += 1
    return line,


def update(val):
    global current_animation
    current_animation._stop()
    current_animation = animation.FuncAnimation(fig, run, range(1, Length), interval=val)

ax.plot([0, 1], [0, 1], color="#000000")

axfreq = plt.axes([0.25, 0.005, 0.65, 0.03])
sfreq = Slider(axfreq, '', 50, 2000, valinit=1000, valstep=50)
sfreq.on_changed(update)

current_animation = animation.FuncAnimation(fig, run, range(Length), interval=sfreq.val)
plt.show()
