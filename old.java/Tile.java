import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.awt.geom.*;
import java.util.*;

public class Tile extends JPanel implements MouseListener
{
  private boolean activated = false, matched = false;
  private Pos pos;
  private int colorId = -1;
  private ArrayList<TileListener> listeners = new ArrayList<TileListener>();
  private ChipBoard board;
  
  public Tile() { init(); }
  public Tile(Pos p) { init(); pos = p; }
  public Tile(int i, int j, ChipBoard b) { pos = new Pos(i,j); board = b; init(); }
  
  public String toString() { return pos.toString(); }

  private void init()
  {
    setBackground(Color.WHITE);
    setBorder(BorderFactory.createLineBorder(Color.black));
    setPreferredSize(new Dimension(72,72));
    addMouseListener(this);
    addTileListener(board);
  }

  public Pos getPos() { return pos; }
  
  public boolean match(Tile t) {
    boolean tst = !t.matched && !this.matched && t.colorId == this.colorId;
    System.out.println("Tile " + pos + " and Tile " + t.pos + " colors " + (tst ? "match" : "don't match"));
    return tst;
  }
  
  //public void setColor(int colorId) { this.colorId = colorId; setBackground(DrBrownUtil.idToColor(colorId)); }
  
  public void addTileListener(TileListener listener) {
    listeners.add(listener);
  }
  

  public void mouseClicked(MouseEvent e) { }
  public void mouseEntered(MouseEvent e) { }
  public void mouseExited(MouseEvent e)  { }
  public void mousePressed(MouseEvent e) {
    for(TileListener l : listeners)
      l.pressed(this);
  }
  public void mouseReleased(MouseEvent e) {
  }

  
  protected void paintComponent(Graphics g) {    
    super.paintComponent(g);
    Graphics2D g2 = (Graphics2D)g;
    Rectangle2D.Double r = new Rectangle2D.Double(0,0,100,100);
    g2.setColor(Color.WHITE);
    g2.fill(r);
    int n = board.numChips(pos);
    boolean red = board.redTop(pos);    
    g2.setColor(red ? Color.RED : Color.BLACK);    
    g2.setFont(new Font("Serif", Font.BOLD, 24));
    g2.drawString(""+n,30,42);
  }
  
}
