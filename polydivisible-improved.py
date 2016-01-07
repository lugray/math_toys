import itertools as it
import math
import sys
from operator import mul


class ProgressBar:
    def __init__(self, width=None, percent=0):
        if width is None:
            self.width = self.getTerminalSize()[0] - 8
        else:
            self.width = width
        sys.stdout.write("%s" % (" " * (self.width + 7)))
        self.updateProgress(percent)

    def getTerminalSize(self):
        import os
        env = os.environ

        def ioctl_GWINSZ(fd):
            try:
                import fcntl
                import termios
                import struct
                cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
            except:
                return
            return cr
        cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
        if not cr:
            try:
                fd = os.open(os.ctermid(), os.O_RDONLY)
                cr = ioctl_GWINSZ(fd)
                os.close(fd)
            except:
                pass
        if not cr:
            cr = (env.get('LINES', 25), env.get('COLUMNS', 80))
        return int(cr[1]), int(cr[0])

    def updateProgress(self, percent=None, done=False):
        if percent is not None:
            self.percent = min(100, percent)
        barLength = self.percent * self.width / 100
        sys.stdout.write("\b" * (self.width+7))
        sys.stdout.write("[%s" % ("*" * barLength))
        sys.stdout.write("%s] " % (" " * (self.width - barLength)))
        sys.stdout.write("%3d%%" % (self.percent))
        sys.stdout.flush()
        if done:
            print ""

    def print_line(self, text):
        sys.stdout.write("%s" % (" " * (self.width + 7)))
        sys.stdout.write("\b" * (self.width+7))
        print text
        sys.stdout.write("%s" % (" " * (self.width + 7)))
        sys.stdout.flush()
        self.updateProgress()

    def finish(self, remove=False):
        if remove:
            sys.stdout.write("%s" % (" " * (self.width + 7)))
            sys.stdout.write("\b" * (self.width+7))
        else:
            self.updateProgress(None, True)


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

    total = reduce(mul, [math.factorial(len(dl)) for dl in dll], 1)
    curr = 0
    lastp = 0
    bar = ProgressBar()

    trials = it.permutations(range(1, b), b-1)
    trials = PolyCandidate(dll)
    while True:
        curr = curr + 1
        currp = (curr * 100)//total
        if currp > lastp:
            # print "{0}%".format(currp)
            bar.updateProgress(currp)
            lastp = currp
        try:
            trial = trials.next()
            partial = trial[0]
            for i in range(2, b):
                partial = b * partial + trial[i - 1]
                if not partial % i == 0:
                    break
            else:
                bar.print_line("    " + highbase(trial))
        except StopIteration:
            bar.finish()
            return

for i in range(1, 35):
    polydivisible(i)

print "Done"
