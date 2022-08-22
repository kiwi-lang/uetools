from dataclasses import dataclass

from math import floor, sin

def fract(x: float):
    return x - int(x)


@dataclass
class Vec2:
    x: float
    y: float

    @property
    def xy(self) -> 'Vec2':
        return self

    def __mul__(self, obj):
        if isinstance(obj, float):
            return Vec2(self.x * obj, self.y * obj)

        return Vec2(self.x * obj.x, self.y * obj.y)

    def __add__(self, obj):
        return Vec2(self.x + obj.x, self.y + obj.y)

    def floor(self):
        return Vec2(floor(self.x), floor(self.y))

    def fract(self):
        return Vec2(fract(self.x), fract(self.y))


def sub(a, b):
    return Vec2(a - b.x, a - b.y)

def mult(a, obj):
    if isinstance(a, float) and isinstance(obj, Vec2):
        return mult(obj, a)

    if isinstance(a, float) and isinstance(obj, float):
        return a * obj

    if isinstance(obj, float):
        return Vec2(a.x * obj, a.y * obj)

    return Vec2(a.x * obj, a.y * obj)


def dot(a, b):
    return a.x * b.x + a.y * b.y


def mix(x, y, a):
    return mult(x, (1 - a)) + mult(y, a)


def random (st: Vec2) -> float:
    return fract(sin(dot(st.xy, Vec2(12.9898,78.233))) * 43758.5453123)

def noise(st: Vec2) -> float:
    i: Vec2 = st.floor()
    f: Vec2 = st.fract()

    # Four corners in 2D of a tile
    a = random(i);
    b = random(i + Vec2(1.0, 0.0))
    c = random(i + Vec2(0.0, 1.0))
    d = random(i + Vec2(1.0, 1.0))

    u: Vec2 = f * f * sub(3.0, f * 2.0)

    return (mix(a, b, u.x) +
            (c - a)* u.y * (1.0 - u.x) +
            (d - b) * u.x * u.y)


class FractionalBrownianmotion:
    def __init__(self):
        # Properties
        self.octaves: int = 4
        self.lacunarity: float = 1.0
        self.gain: float = 0.5
        # Initial values
        self.amplitude: float = 0.5
        self.frequency: float = 1

    def __call__(self, st) -> float:
        value: float = 0.0
        frequency = self.frequency
        amplitude = self.amplitude

        for _ in range(self.octaves):
            value += self.amplitude * noise(st)
            st = st * 2.0;
            # frequency *= self.lacunarity
            amplitude *= self.gain

        return value


if __name__ == '__main__':
    # %matplotlib inline
    import matplotlib.pyplot as plt
    import numpy as np

    n, m = (128, 128)
    generated = np.zeros((n, m))
    generated[0, 0] = 0

    # Hurst index
    # The Hurst exponent describes the raggedness of the resultant motion
    #  higher value leading to a smoother motion
    H = 0.5
    T = 32
    S = 1

    fbm = FractionalBrownianmotion()

    for row in range(n):
        for col in range(m):
            st = Vec2(row / n, col / m)

            generated[row, col] = fbm(st)

    plt.imshow(generated, cmap='hot', interpolation='nearest')
    plt.show()