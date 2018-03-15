
package testElements;

import java.util.*;
import java.time.*;

public class Response {

    String fullRef;
    LocalDateTime dateTime;
    Boolean correct;
    Integer chapter;

    // Constructor
    public Response(List<String> header, List<String> content) {
        for(int i = 0; i < content.size(); i++) {
            this.setValue(header.get(i),content.get(i));
        }
    }

    // To list method (for saving)
    public List<String> toList(List<String> header) {
        List<String> l = new ArrayList<>();
        for(String s : header) {
            switch(s.toLowerCase()) {
                case "fullref":
                    l.add(fullRef);
                    break;
                 case "datetime":
                     //this.dateTime = Integer.valueOf(value);
                     break;
                 case "correct":
                     l.add(correct ? "1" : "0");
                     break;
                 case "chapter":
                     l.add(chapter.toString());
                     break;
                 default:
                     l.add(null);
             }
         }
         return l;
    }

    // Set something
    public boolean setValue(String type, String value) {
         switch(type.toLowerCase()) {
             case "fullref":
                 this.fullRef = value;
                 return true;
             case "datetime":
                 //this.dateTime = Integer.valueOf(value);
                 return true;
             case "correct":
                 this.correct = value.equals("1");
                 return true;
             case "chapter":
                 this.chapter = Integer.valueOf(value);
                 return true;
         }
         return false;
 
    }

    // Override toString method
    @Override
    public String toString() {
        String s = "";
        if (fullRef!=null) { s = s + fullRef + "; "; }
        if (correct!=null) { s = s + correct + "; "; }
        if (chapter!=null) { s = s + chapter + "; "; }
        return s;
    }

} 

