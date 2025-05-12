import javax.swing.*;
import java.awt.*;

/**
 * Provides JLabel with anti-aliasing and 14pt font.
 */
public class CBLabel extends JLabel {

  public CBLabel(String text) {
        super(text);
	setFont(new Font("Sans", Font.BOLD, 14));
    }

  protected void paintComponent(Graphics g) {
    Graphics2D g2 = (Graphics2D) g;
    g2.setRenderingHint(RenderingHints.KEY_TEXT_ANTIALIASING,
			RenderingHints.VALUE_TEXT_ANTIALIAS_ON);    
    super.paintComponent(g);
  }
}
