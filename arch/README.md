ChipBoard                     Chris Brown, July 2019

ChipBoard is a toy game that allows us to explore
learning in a challenging situation --- one in which
traditional reinforcement learning isn't a very good
fit.  The game works like this:  We have a board like
chess (of whatever dimension).  It has chips stacked
in the squares.  Some are all black on top, some have
a red dot on the top.  You can move by chooseing a
red-dot chip on the top of a stack and picking it and
the chips on the top of the adjacent (non-diagonal!)
stacks.  The goal is to minimize the number of chips
left on the board when you get to the point that there
are no moves left.

1) Example using python code:

>>> from board import Board, LFPlay
>>> b = Board(6,140,0.4)
>>> p = LFPlay()
>>> p.playout(b.clone(),p.greedy)
35.0
>>> p.playout(b.clone(),p.antigreedy)
58.0
