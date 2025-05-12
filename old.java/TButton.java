import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.awt.geom.*;
import java.util.*;

public class TButton extends JPanel implements MouseListener {
  private final int h = 24, w = 24;
  private String lab;
  private ArrayList<ActionListener> listeners = new ArrayList<ActionListener>();
  public TButton(String lab) {
    this.lab  = lab;
    setPreferredSize(new Dimension(24,24));
    addMouseListener(this);
  }
  public void addActionListener(ActionListener l) { listeners.add(l); }

  
  public void mouseClicked(MouseEvent e) {
    for(ActionListener l : listeners)
      l.actionPerformed(new ActionEvent(this,0,""));
  }
  public void mouseEntered(MouseEvent e) { }
  public void mouseExited(MouseEvent e)  { }
  public void mousePressed(MouseEvent e) { }
  public void mouseReleased(MouseEvent e) { }
  
  protected void paintComponent(Graphics g) {    
    super.paintComponent(g);
    Graphics2D g2 = (Graphics2D)g;
    
    // This voodoo makes the output prettier
    g2.setRenderingHint(
        RenderingHints.KEY_ANTIALIASING, 
	RenderingHints.VALUE_ANTIALIAS_ON);
    g2.setRenderingHint(
        RenderingHints.KEY_RENDERING, 
	RenderingHints.VALUE_RENDER_QUALITY);

    g2.setFont(new Font("Serif", Font.BOLD, 20));
    g2.drawString(lab,2,h-4);
  }
}
