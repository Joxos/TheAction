from fractions import Fraction


def calculate_distance(p1, p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** (1 / 2)


class Line:
    def __init__(self, p1, p2):
        self.k = Fraction(p1[1] - p2[1], p1[0] - p2[0])
        self.b = p1[1] - self.k * p1[0]

    def calculate_y(self, x):
        return self.k * x + self.b

    def calculate_x(self, y):
        return (y - self.b) / self.k


def sampling(p1, p2):
    if p1 == p2:
        return []
    elif p1[0] == p2[0]:
        return [(p1[0], i) for i in range(min(p1[1], p2[1]) + 1, max(p1[1], p2[1]))]
    elif p1[1] == p2[1]:
        return [(i, p1[1]) for i in range(min(p1[0], p2[0]) + 1, max(p1[0], p2[0]))]
    line = Line(p1, p2)
    points = []

    # x samples
    min_x = min(p1[0], p2[0])
    max_x = max(p1[0], p2[0])
    for x in range(min_x + 1, max_x):
        points.append((x, round(line.calculate_y(x))))

    # y samples
    min_y = min(p1[1], p2[1])
    max_y = max(p1[1], p2[1])
    for y in range(min_y + 1, max_y):
        points.append((round(line.calculate_x(y)), y))

    return points


if __name__ == "__main__":
    p1 = (0, 3)
    p2 = (3, 1)
    print(sampling(p1, p2))
    print(calculate_distance(p1, p2))
