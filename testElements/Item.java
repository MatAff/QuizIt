
package testElements;

import java.util.*;

public class Item {

    // Members
    String book;
    Integer chapter;
    Integer chapterItemNr;
    String fullRef;
    Integer pageQuestion;
    Integer pageAnswer;

    // Default constructor
    public Item() {

    } 

    // Constructor
    public Item(List<String> header, List<String> content) {
        for(int i = 0; i < content.size(); i++) {
            this.setValue(header.get(i),content.get(i));
        }
    }

    // Set something
    public boolean setValue(String type, String value) {
    
         switch(type.toLowerCase()) {
             case "book":
                 this.book = value;
                 return true;
             case "chapter":
                 this.chapter = Integer.valueOf(value);
                 return true;
             case "chapteritemnr":
                 this.chapterItemNr = Integer.valueOf(value);
                 return true;
             case "fullref":
                 this.fullRef = value;
                 return true;
         }
         return false;
 
    }

    // Override toString method
    @Override
    public String toString() {
        String s = "";
        if (book!=null) { s = s + book + "; "; }
        if (chapter!=null) { s = s + chapter + "; "; }
        if (chapterItemNr!=null) { s = s + chapterItemNr + "; "; }
        if (fullRef!=null) { s = s + fullRef + "; "; }
        return s;
    }

} 
