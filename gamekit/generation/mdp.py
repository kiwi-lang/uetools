import math
import numpy as np
import random
from numba import njit


@njit
def baserand():
    return np.random.rand()
    return random.random()


@njit
def rand(spread = 1):
    return baserand() * spread * 2 - spread


@njit
def jitter(value, spread):
    return value + rand(spread)


@njit
def midpoint(a, b) -> int:
    """Index in the middle of two points"""
    return int((a + b) * 0.5)


@njit
def avg(a, b) -> float:
    """Average of values"""
    return (a + b) * 0.5


@njit
def avg_all(a, b, c, d) -> float:
    return (a + b + c + d) / float(4)


@njit
def displace_square(array, lx, rx, by, ty, spread):
    cx = midpoint(lx, rx) # Center, left, right
    cy = midpoint(by, ty) # Center, Bot, top

    bl = array[lx, by] # bottom left
    br = array[rx, by] # bottom right
    tl = array[lx, ty] # top left
    tr = array[rx, ty] # top right

    t = avg(tl, tr) # top
    l = avg(bl, tl) # left
    b = avg(bl, br) # bot
    r = avg(br, tr) # right

    array[cx, by] = jitter(b, spread) # bottom
    array[cx, ty] = jitter(t, spread) # top
    array[lx, cy] = jitter(l, spread) # left
    array[rx, cy] = jitter(r, spread) # right

    center = avg_all(t, l , b, r)
    array[cx, cy] = jitter(center, spread)


@njit
def mpd(resolution, exponent, array, spread=0.3, evol=0.5, seed=0):
    """Apply the midpoint displacement algorithm on a given array"""
    np.random.seed(seed)

    array[0, 0] = baserand()
    array[0, -1] = baserand()
    array[-1, 0] = baserand()
    array[-1, -1] = baserand()

    for i in range(exponent):
        chunks = int(math.pow(2, i))
        width = ((resolution - 1) / chunks)

        for x in range(chunks):
            for y in range(chunks):
                # corners of the chunks
                lx = int(width * x)
                rx = int(lx + width)
                by = int(width * y)
                ty = int(by + width)

                displace_square(array, lx, rx, by, ty, spread)

    min, max = array.min(), array.max()
    array = (array - min) / (max - min)


@njit
def displace_diamond_square(array, x, y, radius, spread):
    bl = array[x - radius, y - radius] # bottom left
    br = array[x - radius, y + radius] # bottom right
    tl = array[x + radius, y - radius] # top left
    tr = array[x + radius, y + radius] # top right

    array[x, y] = jitter(avg_all(bl, br, tl, tr), spread)


@njit
def displace_diamond_diamond(array, x, y, radius, spread):
    count = 0
    total = 0

    if x - radius > 0:
        total += array[x - radius, y] # bottom left
        count += 1

    if x + radius < array.shape[0]:
        total += array[x + radius, y] # bottom right
        count += 1

    if y - radius > 0:
        total += array[x, y - radius] # top left
        count += 1

    if y + radius < array.shape[1]:
        total += array[x, y + radius] # top right
        count += 1

    array[x, y] = jitter(total / count, spread)


@njit
def apply_square(array, radius, resolution, spread):
    for x in range(radius, resolution, radius * 2):
        for y in range(radius, resolution, radius * 2):
            displace_diamond_square(array, x, y, radius, spread)


@njit
def apply_diamond(array, radius, resolution, spread):
    for y in range(0, resolution, radius):
        shift = radius if y / radius % 2 == 0 else 0
        for x in range(shift, resolution, radius * 2):
            displace_diamond_diamond(array, x, y, radius, spread)


@njit
def mdp_diamond(array, resolution, spread, evol=0.5, seed=0):
    np.random.seed(seed)

    array[0, 0] = baserand()
    array[0, -1] = baserand()
    array[-1, 0] = baserand()
    array[-1, -1] = baserand()

    radius = int(resolution / 2)
    while radius >= 1:
        apply_square(array, radius, resolution, spread)
        apply_diamond(array, radius, resolution, spread)

        radius = int(radius / 2)
        spread = spread * evol

    min, max = array.min(), array.max()
    array = (array - min) / (max - min)


class HeightMap:
    def __init__(self, exponent):
        self.exponent = exponent
        self.resolution = int(math.pow(2, exponent) + 1)
        self.data = np.zeros((self.resolution, self.resolution))
        self.last = self.resolution - 1

    def apply(self, fun):
        for i in range(self.resolution):
            for j in range(self.resolution):
                self.data[i, j] = fun()
        return self

    def mpd(self, spread=0.3, evol=0.5):
        mpd(self.resolution, self.exponent, self.data, spread, evol)
        return self

    def mdp_diamond(self, spread=0.3, evol=0.5):
        mdp_diamond(self.data, self.resolution, spread, evol)
        return self

    def show(self):
        import matplotlib.pyplot as plt
        plt.imshow(self.data, cmap='Greys', interpolation='nearest')
        plt.show()


def generate_images():
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.image

    for a, i in enumerate(np.linspace(0.1, 2, 10)):
        for b, j in enumerate(np.linspace(0.1, 1, 10)):
            title = f'spread {i:.2f} evol {j:.2f}'
            data = HeightMap(12).mdp_diamond(i, j).data
            matplotlib.image.imsave(f'dump/{title}.png', data, cmap='Greys')
            print(title)


generate_images()
