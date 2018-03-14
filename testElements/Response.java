
package testElements;

import java.util.*;
import java.time.*;

public class Response {

    String fullRef;
    LocalDateTime dateTime;
    Boolean correct;

    // Constructor
    public Response(List<String> header, List<String> content) {
        for(int i = 0; i < content.size(); i++) {
            this.setValue(header.get(i),content.get(i));
        }
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
         }
         return false;
 
    }

    // Override toString method
    @Override
    public String toString() {
        String s = "";
        if (fullRef!=null) { s = s + fullRef + "; "; }
        if (correct!=null) { s = s + correct + "; "; }
        return s;
    }

} 

