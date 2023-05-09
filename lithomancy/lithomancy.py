import re


class Stone:
    AMETHYST = 'a'
    BERYL = 'b'
    CHALCEDONY = 'c'

    def __init__(self, id_, pos=(0.0, 0.0)):
        self.pos = pos  # x, y
        self.id = id_

    @property
    def name(self) -> str:
        return {
            'a': 'Amethyst',
            'b': 'Beryl',
            'c': 'Chalcedony'
        }[self.id]

    def move(self, delta:tuple):
        self.pos = (self.pos[0] + delta[0], self.pos[1] + delta[1])


class Stick:
    ASH = 'a'
    BIRCH = 'b'
    CEDAR = 'c'
    # OTHER = 'g'

    def __init__(self, material: str, x1: float, y1: float, x2: float, y2: float):
        self.material = material
        self.a = (x1, y1)
        self.b = (x2, y2)
        self.orientation = 1

    def enter(self, previous):
        """
        Sets the entry point of the current stick
        to determine the direction it is being traversed.
        """
        p = previous.end
        if self.a == p:
            self.orientation = 1
        elif self.b == p:
            self.orientation = -1
        else:
            print(self.a, self.b, p, previous.a, previous.b)
            raise Exception("Stick not touching an end of previous stick!")

    @property
    def end(self):
        """
        Returns the end point, given the current orientation.
        """
        return (None, self.b, self.a)[self.orientation]

    @property
    def change(self):
        """
        Returns target, (delta x, delta y)
        """
        return (self.orientation * (self.b[0] - self.a[0]), self.orientation * (self.b[1] - self.a[1]))


def touching(stones) -> bool:
    distance = lambda a,b: abs(((b[0] - a[0])**2 + (b[1] - a[1])**2)**0.5)
    rtouching = lambda a,b: 1 >= distance(a.pos, b.pos)
    # Returns true if any stones are touching
    for _, s in stones.items():
        for _, other in stones.items():
            if s == other:
                continue
            if rtouching(s, other):
                return True
    return False


def load_sticks(source_file_name: str) -> list[Stick]:
    FORK = '├'
    ENDFORK = '┤'
    raw = []
    with open(source_file_name, 'r') as f:
        for line in f:

            if line.startswith('#'):  # ignore comments
                continue
            vectors = line.split()
            for v in vectors:
                x, s, y = re.match(r'([\-0-9\.]*)([abcg├┤])([\-0-9\.]*)', v).groups()
                raw.append((s, (float(x or 0), float(y or 0))))
    pos = (0.0, 0.0)
    sticks = []
    stack = []
    for s in raw:
        if s[0] == FORK:
            stack.append(pos)
            continue
        if s[0] == ENDFORK:
            pos = stack.pop()
            continue
        x = pos[0] + s[1][0]
        y = pos[1] + s[1][1]
        sticks.append(Stick(s[0], *pos, x, y))
        pos = [x, y]

    for s in sticks:
        print(f'{s.material} : {s.a} - {s.b}')
    return sticks
