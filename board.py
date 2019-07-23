#!/usr/bin/env python2
import numpy
import random
import math
import sys

class Board:
    """A class for representing the red-black chip game."""
    def __init__(self,n,k,p):
        self.n = n
        self.k = k
        self.p = p
        self.B = map(lambda y: map(lambda x: [],range(0,n)),range(0,n))
        self.A = numpy.zeros((n,n))
        for i in range(0,k):
            r = random.randint(0,n-1)
            c = random.randint(0,n-1)
            cr = random.random() < p
            self.B[r][c].append(cr)
            self.A[r,c] = (math.fabs(self.A[r,c]) + 1) * (-1.0 if cr else 1.0)

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
        assert(self.color(r,c), "row,col off board in choose")
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

    def getPosFeatureVector(self,r,c):
        """Returns feature vector for r,c."""
        V = []
        for dr in range(-1,2):
            for dc in range(-1,2):
                V.append(self.height(r+dr,c+dc))
                V.append(-1 if self.color(r+dr,c+dc) else 1)
        return V

    def getMoves(self):
        """Returns array of (r,c) positions of valid moves in lex order."""
        M = []
        for i in range(0,self.n):
            for j in range(0,self.n):
                if self.color(i,j):
                    M.append((i,j))
        return M
        
    def getMovesWithValues(self,f):
        """Returns array of ((r,c),val) for each valid move, where val is playout with f."""
        M = self.getMoves()
        return map(lambda m: (m,self.clone().choose(m[0],m[1]).playout(f)), M)
                    
    def makeMove(self,f):
        """Makes one move following choice function f as a policy."""
        M = self.getMoves()
        best = M[0]
        for m in M:
            if m != best:
                x = f(numpy.concatenate( (self.getPosFeatureVector(best[0],best[1]),self.getPosFeatureVector(m[0],m[1]))))
                if x > 0:
                    best = m
        self.choose(best[0],best[1])
        return self.score()

    def playout(self,f):
        """Playout with choice function f as a policy, returning resulting score."""
        s = self.score()
        while s < 0:
            s = self.makeMove(f)
        return s

    def play(self,f,N):
        """Plays N moves using f as policy."""
        s,m = self.score(),N
        while s < 0 and m > 0:
            s = self.makeMove(f)
            m = m-1
        return s
    
    
def countRed(V,off):
    """Returns number of TO BE CONTINUED  """
    c = 0
    for k in [1,3,4,5,7]:
        c += (1 if V[2*(k+off)+1] < 0 else 0)
    return c

def countRemoved(V,off):
    c = 0
    for k in [1,3,4,5,7]:
        c += (1 if V[2*(k+off)] > 0 else 0)
    return c

def greedy(V):
    s1 = countRemoved(V,0) - countRed(V,0)
    s2 = countRemoved(V,9) - countRed(V,9)
    return s2 - s1 

def antigreedy(V):
    return -1*greedy(V)

