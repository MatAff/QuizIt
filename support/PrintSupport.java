
package support;

public class PrintSupport {

    public static final String ANS4x_RESET = "\u001B[0m";
    public static final String ANSI_BLACK = "\u001B[30m";
    public static final String ANSI_RED = "\u001B[31m";
    public static final String ANSI_GREEN = "\u001B[32m";
    public static final String ANSI_YELLOW = "\u001B[33m";
    public static final String ANSI_BLUE = "\u001B[34m";
    public static final String ANSI_PURPLE = "\u001B[35m";
    public static final String ANSI_CYAN = "\u001B[36m";
    public static final String ANSI_WHITE = "\u001B[37m";
    
    public static void printColor(String text, String color) {

        String ansiTag = null;

        switch(color.toLowerCase()) {
             case "black":
                 ansiTag = ANSI_BLACK;
                 break;
             case "red":
                 ansiTag = ANSI_RED;
                 break;
             case "green":
                 ansiTag = ANSI_GREEN;
                 break;
             default:
                 ansiTag = ANSI_BLACK;
                 break;
        }

        // Print
        System.out.println(ansiTag + text + ANS4x_RESET);
    } 
}

