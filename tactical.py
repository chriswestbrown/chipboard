from board import LFPlay, Board

class TacticalPlay(LFPlay):
    def tacticalGreedy(self,V):
        """Greedy choice function."""
        s1 = self.countRemoved(V,0)/self.countRed(V,0)
        s2 = self.countRemoved(V,9)/self.countRed(V,9)
        return s1 - s2
    def antitacticalgreedy(self,V):
        return -1*tacticalGreedy(V)

class Tester:
    def testStrats(self,N):
        g,ag,t,at = 0
        for i in range(N):
            b = Board(6,140,.4)
