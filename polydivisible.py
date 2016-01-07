import itertools as it


class PolyCandidate:
    def __init__(self, digListList):
        self.digListList = digListList
        self.position = [None] * sum([len(digList) for digList in digListList])
        for i in range(len(digListList)):
            for j in range(len(digListList[i])):
                self.position[digListList[i][j] - 1] = [i, j]
        self.perms = [it.permutations(digList) for digList in digListList]
        self.currents = None

    def __iter__(self):
        return self

    def next(self):
        if self.currents is None:
            self.currents = [perm.next() for perm in self.perms]
            return [self.currents[pos[0]][pos[1]] for pos in self.position]
        for i in range(len(self.perms)):
            try:
                self.currents[i] = self.perms[i].next()
                break
            except StopIteration:
                if i == len(self.perms) - 1:
                    raise StopIteration
                else:
                    self.perms[i] = it.permutations(self.digListList[i])
                    self.currents[i] = self.perms[i].next()

        return [self.currents[pos[0]][pos[1]] for pos in self.position]


def factors(n):
    return sorted(set(reduce(list.__add__, ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0))))


def highbase(digits):
    """Convert a tuple of digits into a string representation."""
    if type(digits) is int:
        if digits < 10:
            return chr(ord("0") + digits)
        else:
            return chr(ord("A") + digits - 10)
    else:
        return "".join([highbase(digit) for digit in digits])


def polydivisible(b):
    """Print the polydivisible numbers for base b."""
    print "Base {0}:".format(b)
    if b % 2 == 1:
        return
    fs = factors(b)
    fs.pop()
    fs.reverse()

    dll = list()
    done = set()
    for f in fs:
        t = [f * i for i in range(1, b//f)]
        t = set(t) - done
        done = done | t
        dll.append(sorted(t))

    # trials = it.permutations(range(1, b), b-1)
    trials = PolyCandidate(dll)
    while True:
        try:
            trial = trials.next()
            partial = trial[0]
            for i in range(2, b):
                partial = b * partial + trial[i - 1]
                if not partial % i == 0:
                    break
            else:
                print "   ", highbase(trial)
        except StopIteration:
            return

for i in range(2, 25):
    polydivisible(i)

print "Done"
