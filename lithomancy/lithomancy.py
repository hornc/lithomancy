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
        self.start = (x1, y1)
        self.end = (x2, y2)

    @property
    def change(self):
        """
        Returns target, (delta x, delta y)
        """
        return (self.end[0] - self.start[0], self.end[1] - self.start[1])
        #return self.material, (self.end[0] - self.start[0], self.end[1] - self.start[1])


def touching(stones) -> bool:
    # Returns true if any stones are touching
    for _, s in stones.items():
        for _, other in stones.items():
            if s == other:
                continue
            if s.pos == other.pos:
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
        print(f'{s.material} : {s.start} - {s.end}')
    return sticks
