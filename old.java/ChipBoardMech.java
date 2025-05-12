import java.util.*;
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class ChipBoardMech {
  public Random rand;
  final int Nr = 7, Nc = 7, k = 150;
  private int count = k, numMovesMade = 0, redShowing = 0, emptyStacks = Nr*Nc;
  CStack[][] B = new CStack[Nr][Nc];
  Integer currentSeed = null;
  ArrayList<UpdateListener> listeners = new ArrayList<UpdateListener>();

  public interface UpdateListener {
    public void update(ArrayList<Pos> changedPositions, boolean gameOver);
  }
  
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

  public boolean gameOver() { return redShowing == 0; }

  
  public boolean remove(Pos p) {
    if (p != null && numChips(p) > 0) {
      //System.out.println("REMOVE: " + p);
      getS(p).pop();
      //System.out.println("      : red showing = " + redShowing );
      count--;
      return true;
    }
    else
      return false;
  }
      
  public void makeMove(Pos p) {
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
      if (gameOver) {
	System.out.println("Game over: " +
			   "score " + (numberOfEmpty() - count) + ", "	+		   
			   count + " chips left on Board, " +
			   numMovesMade + " moves made, " +
			   numberOfEmpty() + " empty cells!"			   
			   );
      }
      for(UpdateListener l : listeners)
	l.update(changed,gameOver);
    }
  }


  public int numberOfEmpty() {
    int n = 0;
    for(int i = 0; i < Nr; i++)
      for(int j = 0; j < Nc; j++) {
	Pos p = new Pos(i,j);
	n += (numChips(p) == 0 ? 1 : 0);
      }
    return n;
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
  
  public ChipBoardMech(int seed) {
    rand = new Random(seed);	
    currentSeed = seed;

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
    }    
  }
  
  public static void main(String[] args) {
    boolean help = false;
    Integer seed = null;
    int playType = 0; // 0 <- human, 1 <- random
    for(int i = 0; i < args.length; i++) {
      if (args[i].equals("-r"))
	playType = 1;
      else if (args[i].equals("-h"))
	help = true;
      else if (args[i].equals("--help"))
	help = true;
      else { try {
	  seed = Integer.parseInt(args[i]);
	}catch(Exception e) {
	  help = true;
	  System.out.println("Error!  Can't interpret '" + args[i] +
			     "' as integer seed value.");
	  break;
	}
      }
    }
    if (help || seed == null) {
      printHelp();
      System.exit(0);
    }
    
    // Seed 100, best so far: Game over: 10 chips left on Board, 43 moves made 43 empty cells!
    ChipBoardMech b = new ChipBoardMech(seed);
    Random rand2 = new Random();
    while(!b.gameOver()) {
      b.makeMove(b.randomMove(rand2));
    }

  }


  static String msgHTML =
      "<b>usage:</b> <code>chipboard [-r|-h|--help]&lt;seed&gt;</code><br>\n" +
      "ChipBoard v0.1<br>\n" +
      "<ul><li>Each square represents a stack of alternating red/back chips.</li>\n" +
      "<li>The number is the size of the stack, the color is the color of the top chip.</li>\n" +
      "<li>Click on a *red* number to remove the top chip on that square and those adjacent.</li>\n" +
      "<li>Play stops when there are no more red squares.</li>\n" +
      "<li>Score is calculated as: score = #emtpy_stacks - #number_chips_remaining.</li>\n" +
      "<li>Goal: get the highest score you can!</li></ol>";

  public void makeHelpFrame() {
    JFrame helpFrame = new JFrame();    
    JEditorPane ep = new JEditorPane();
    ep.setContentType("text/html");
    ep.setText(msgHTML);
    helpFrame.add(ep);
    helpFrame.setLocation(400,50);
    helpFrame.pack();
    helpFrame.setVisible(true);
  }
  
  public static void printHelp() {
    String msg =
      "usage: chipboard [-r|-h|--help] <seed>\n" +
      "ChipBoard v0.1\n" +
      "Each square represents a stack of alternating red/back chips.\n" +
      "The number is the size of the stack, the color is the color of the top chip.\n" +
      "Click on a *red* number to remove the top chip on that square and those adjacent.\n" +
      "Play stops when there are no more red squares.\n" +
      "Score is calculated as: score = #emtpy_stacks - #number_chips_remaining.\n" +
      "Goal: get the highest score you can!";
    System.out.println(msg);
  }

  
  
}
