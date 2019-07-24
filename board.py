#!/usr/bin/env python2
import numpy
import random
import math
import sys

class Board:
    """A class for representing the red-black chip game.

    The board is an nxn grid.  Each grid cell has some number
    of chips stacked on it.  Chips may be black (False) or
    red (True).
    """
    def __init__(self,n,k,p,kind=0):
        """Initializes board object."""
        self.n = n
        self.k = k
        self.p = p
        self.B = map(lambda y: map(lambda x: [],range(0,n)),range(0,n))
        self.A = numpy.zeros((n,n))
        self.numred = 0
        if kind == 0:
            self.init_0()
        else:
            self.init_winnable(kind)

    def init_0(self):
        for i in range(0,self.k):
            r = random.randint(0,self.n-1)
            c = random.randint(0,self.n-1)
            cr = random.random() < self.p
            self.B[r][c].append(cr)
            self.A[r,c] = (math.fabs(self.A[r,c]) + 1) * (-1.0 if cr else 1.0)
            if cr:
                self.numred += 1

    def init_winnable(self,kind=1):
        self.p = (0 if kind == 1 else self.getProb())
        self.not_important_bottoms = []
        count = self.k
        while count > 0:
            r = random.randint(0,self.n-1)
            c = random.randint(0,self.n-1)
            count -= self.add(r,c)

        removed = random.sample(self.not_important_bottoms,count*-1)
        for (x,y) in removed:
            self.B[x][y].pop(0)
            self.A[x,y] += (1.0 if self.A[x,y] < 0 else -1.0)

    def getProb(self):
        n = self.n*1.0
        self.p = -(3*n**2+3n-540*self.p +2)/(12*n**2-3*n-2)

    def checkProb(self):
        return self.p

    def add(self,r,c):
        count = 0
        self.B[r][c].append(True)
        self.A[r,c] = (math.fabs(self.A[r,c]) + 1)*-1
        self.numred += 1
        count += 1
        for x,y in [(r-1,c),(r+1,c),(r,c-1),(r,c+1)]:
            if self.valid(x,y):
                if self.height(x,y) == 0:
                    self.not_important_bottoms.append((x,y))
                cr = random.random() < self.p
                self.B[x][y].append(cr)
                self.A[x,y] = (math.fabs(self.A[x,y]) + 1) * (-1.0 if cr else 1.0)
                count += 1
                if cr:
                    self.numred += 1
        return count

    def getNumred(self):
        return self.numred

    def clone(self):
        """Creates a deep copy of the Board object."""
        C = Board(0,0,0)
        C.n = self.n
        C.k = self.k
        C.p = self.p
        C.B = map( lambda X: map(lambda a: a[:], X), self.B )
        C.A = self.A.copy()
        return C

    def getBoard(self):
        """Returns the board represented as a numpy array. """
        return self.A

    def color(self,r,c):
        """Returns True if there is a red chip at r,c, False otherwise."""
        return self.A[r,c] < 0 if self.valid(r,c) else False

    def height(self,r,c):
        """Returns the height of the stack at r,c, or 0 if r,c invalid."""
        return math.fabs(self.A[r,c]) if self.valid(r,c) else 0

    def valid(self,r,c):
        """Returns True if and only if r,c is a valid board position."""
        return 0 <= r and r < self.n and 0 <= c and c < self.n

    def pop(self,r,c):
        """If r,c is valid and non-empty, pops chip."""
        if self.valid(r,c) and self.A[r,c] != 0:
            self.B[r][c].pop()
            lasti = len(self.B[r][c])-1
            x = False if lasti < 0 else self.B[r][c][lasti]
            self.A[r,c] = (self.height(r,c) - 1)*(-1.0 if x else 1.0)

    def choose(self,r,c):
        """Carries out action of removing chip at r,c."""
        self.pop(r-1,c)
        self.pop(r+1,c)
        self.pop(r,c)
        self.pop(r,c-1)
        self.pop(r,c+1)
        return self

    def score(self):
        """Computes the score of the current board."""
        s = 0
        countRed = 0
        for r in self.A:
            for x in r:
                s += math.fabs(x)
                countRed += (1 if x < 0 else 0)
        return s if countRed == 0 else -1

    def getMoves(self):
        """Returns array of (r,c) positions of valid moves in lex order."""
        M = []
        for i in range(0,self.n):
            for j in range(0,self.n):
                if self.color(i,j):
                    M.append((i,j))
        return M


class LFPlay:
    """A class defining ChipBoard game play based on local features.

    The feature vector concept used here is that a (r,c) position
    defining a valid play is turned into an 18-component feature
    vector where the nine-cell box centered on (r,c) is represented
    from top-left to bottom-right.  Each cell gets two components in
    the feature vector - the stack height and color (-1=red, +1=black).
    The two moves to be compared are represented as a 36-component
    vector that is first move followed by second.
    """

    def getPosFeatureVector(self,B,r,c):
        """Returns feature vector for r,c."""
        V = []
        for dr in range(-1,2):
            for dc in range(-1,2):
                V.append(B.height(r+dr,c+dc))
                V.append(-1 if B.color(r+dr,c+dc) else 1)
        return V

    def getMovesWithValues(self,B,f):
        """Returns array of ((r,c),val) for each valid move, where val is playout with f."""
        M = B.getMoves()
        return map(lambda m: (m,self.playout(B.clone().choose(m[0],m[1]),f)), M)

    def makeMove(self,B,f):
        """Makes one move following choice function f as a policy."""
        M = B.getMoves()
        best = M[0]
        for m in M:
            if m != best:
                x = f(numpy.concatenate( (self.getPosFeatureVector(B,best[0],best[1]),
                                          self.getPosFeatureVector(B,m[0],m[1]))))
                if x > 0:
                    best = m
        B.choose(best[0],best[1])
        return B.score()

    def playout(self,B,f):
        """Playout with choice function f as a policy, returning resulting score."""
        s = B.score()
        while s < 0:
            s = self.makeMove(B,f)
        return s

    def play(B,f,N):
        """Plays N moves using f as policy."""
        s,m = B.score(),N
        while s < 0 and m > 0:
            s = self.makeMove(B,f)
            m = m-1
        return s

    def countRed(self,V,off):
        """Returns number of red chips that will be removed by a move.

        V : feature vector representing the two moves to be compared.
        off: 0 to count first move, 9 to count second move
        """
        c = 0
        for k in [1,3,4,5,7]:
            c += (1 if V[2*(k+off)+1] < 0 else 0)
        return c

    def countRemoved(self,V,off):
        """Returns total number of chips that will be removed by a move.

        V : feature vector representing the two moves to be compared.
        off: 0 to count first move, 9 to count second move
        """
        c = 0
        for k in [1,3,4,5,7]:
            c += (1 if V[2*(k+off)] > 0 else 0)
        return c

    def greedy(self,V):
        """Greedy choice function."""
        s1 = self.countRemoved(V,0) - self.countRed(V,0)
        s2 = self.countRemoved(V,9) - self.countRed(V,9)
        return s2 - s1

    def antigreedy(self,V):
        """Anti-greedy choice function ... i.e. do the opposite!"""
        return -1*self.greedy(V)
