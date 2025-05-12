import java.util.*;
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class ChipBoardMech {
  public Random rand; // based off of game seed
  final int Nr = 7, Nc = 7;
  private int k; // default 150
  private int count, numMovesMade = 0, redShowing = 0, emptyStacks = Nr*Nc;
  CStack[][] B = new CStack[Nr][Nc];
  Integer currentSeed = null;
  ArrayList<UpdateListener> listeners = new ArrayList<UpdateListener>();

  //-- UpdateListener
  public interface UpdateListener {
    public void update(ArrayList<Pos> changedPositions, boolean gameOver);
  }
  public void addUpdateListener(UpdateListener l) { listeners.add(l); }

  //-- Stack related class/code
  private class CStack extends ArrayList<Integer> {
    public boolean isEmpty() { return super.size() == 0; }
    public int size() { return super.size(); }
    public int peek() { return get(size() - 1); }
    public void push(int i) {
      if (isEmpty()) { emptyStacks--; }
      int j = isEmpty() ? 0 : peek();
      add(i);
      if (j == 0 && i > 0) redShowing++;
      else if (j > 0 && i == 0) redShowing--;
    }
    public int pop() {
      int sizeBefore = size();
      int i = peek();
      remove(sizeBefore-1);
      if (sizeBefore == 1) { emptyStacks++; }
      int j = isEmpty() || peek() == 0 ? 0 : 1;
      if (i > 0 && j == 0)
	redShowing--;
      else if (i == 0 && j > 0)
	redShowing++;
      return i;
    }
  }
  public CStack getS(Pos p) { return B[p.getRow()][p.getCol()]; }
  public int numChips(Pos p) { return getS(p).size(); }
  public boolean redTop(Pos p) {
    CStack s =  getS(p);
    return (s.isEmpty() || s.peek() == 0) ? false : true;
  }

  //-- Constructor
  public ChipBoardMech(int seed) {
    init(seed,150);
  }
  public ChipBoardMech(int seed, int initNumChips) {
    init(seed,initNumChips);
  }
  
  private void init(int seed, int initNumChips) {
    rand = new Random(seed);	
    currentSeed = seed;
    k = initNumChips;
    
    // Set up board
    for(int i = 0; i < Nr; i++)
      for(int j = 0; j < Nc; j++)
	B[i][j] = new CStack();
    for(int i = 0; i < k; i++) {
      int r = rand.nextInt(Nr);
      int c = rand.nextInt(Nc);
      int x = rand.nextInt(2);
      Pos p = new Pos(r,c);
      if (numChips(p) == 0)
	B[r][c].push(x);
      else
	B[r][c].push(redTop(p) ? 0 : 1);
      count++;
    }    
  }
  
  private boolean remove(Pos p) {
    if (p != null && numChips(p) > 0) {
      getS(p).pop();
      count--;
      return true;
    }
    else
      return false;
  }
  
  //-- Actual methods for the outside world!
  public boolean gameOver() { return redShowing == 0; }
  public int numEmptyStacks() { return emptyStacks; }
  public int numChips() { return count; }
  public int getScore() { return emptyStacks - count; }
  public Integer getSeed() { return currentSeed; }
  public int getNc() { return Nc; }
  public int getNr() { return Nc; }        

  public void makeMove(Pos p) {
    //System.out.println("Pos: " + p + " size: " + numChips(p));
    if (numChips(p) == 0 || !redTop(p))
      System.out.println("Illegal move at: " + p);
    else {
      //System.out.println("BEFOR: red showing = " + redShowing + " count = " + count);
      Pos[] M = { new Pos(0,0),  new Pos(1,0),  new Pos(0,1),  new Pos(-1,0),  new Pos(0,-1)  };
      ArrayList<Pos> changed = new ArrayList<Pos>();
      for(Pos d : M) {
	Pos np = p.plus(d);
	try {
	  if (remove(np))
	    changed.add(np);
	}catch(ArrayIndexOutOfBoundsException e) { }
      }
      numMovesMade++;
      //System.out.println("AFTER: red showing = " + redShowing + " count = " + count);
      boolean gameOver = redShowing == 0;
      if (gameOver && false) {
	System.out.println("Game over: " +
			   "score " + (numEmptyStacks() - count) + ", "	+		   
			   count + " chips left on Board, " +
			   numMovesMade + " moves made, " +
			   numEmptyStacks() + " empty cells!"			   
			   );
      }
      for(UpdateListener l : listeners)
	l.update(changed,gameOver);
    }
  }

  public Pos randomMove(Random rand2) {
    Pos[] A = new Pos[Nr*Nc];
    int n = 0;      
    for(int i = 0; i < Nr; i++)
      for(int j = 0; j < Nc; j++) {
	Pos p = new Pos(i,j);
	if (redTop(p)) { A[n++] = p; }
      }
    return A[rand2.nextInt(n)];
  }
  
  //-- MAIN
  public static void main(String[] args) {
    Integer seed = null;
    Integer numTimes = null;
    for(int i = 0; i < args.length; i++) {
      try {
	int x = Integer.parseInt(args[i]);
	if (seed == null) { seed = x; }
	else if (numTimes == null) { numTimes = x; }
	else { System.out.println("Too many arguments!"); System.exit(1); }
      }catch(Exception e) {
	System.out.println("Error!  Can't interpret '" + args[i] +
			   "' as integer value.");
	break;
      }
    }
    if (seed == null) {
      System.out.println("Requires seed argument!");
      System.exit(0);
    }
    if (numTimes == null) {
      numTimes = 1;
    }

    Random rand2 = new Random();
    for(int i = 0; i < numTimes; i++) {
      ChipBoardMech b = new ChipBoardMech(seed);
      while(!b.gameOver()) {
	b.makeMove(b.randomMove(rand2));
      }
      System.out.printf("score = %d, #empty = %d, #chips = %d\n",b.getScore(),b.numEmptyStacks(),b.numChips());
      int s = b.getScore();
    }
  }
}
