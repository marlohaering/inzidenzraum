class Line:
    def __init__(self, p1, p2, q):
        self.p1 = p1
        self.p2 = p2
        self.points = set()

        for i in range(q):
            t = (p1 + i * (p2 - p1)) % q
            t = tuple(t)
            self.points.add(t)

        self.points = frozenset(self.points)

    def __eq__(self, other):
        if not isinstance(other, Line):
            return False
        return self.points == other.points

    def __hash__(self):
        return hash(self.points)

    def __str__(self):
        return str(self.points)

    def is_on_line(self, p):
        return p in self.points
