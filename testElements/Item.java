
package testElements;

import java.util.*;
import support.*;

public class Item {

    // Members
    Integer itemNr;
    String question;
    String answer;
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
             case "itemnr":
                 this.itemNr = Integer.valueOf(value);
                 break;
             case "question":
                 this.question = value;
                 break;
             case "answer":
                 this.answer = value;
                 break;
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
             case "pagequestion":
                 //this.pageQuestion = Integer.valueOf(value);
                 this.pageQuestion = NumberSupport.createInteger(value);
                 return true;
             case "pageanswer":
                 this.pageAnswer =  Integer.valueOf(value);
                 return true;
         }
         return false;
 
    }

    // Override toString method
    @Override
    public String toString() {
        String s = "";
        if (itemNr!=null) { s = s + itemNr + "; "; }
        if (question!=null) { s = s + question + "; "; }
        if (answer!=null) { s = s + answer + "; "; }
        if (book!=null) { s = s + book + "; "; }
        if (chapter!=null) { s = s + chapter + "; "; }
        if (chapterItemNr!=null) { s = s + chapterItemNr + "; "; }
        if (fullRef!=null) { s = s + fullRef + "; "; }
        if (pageQuestion!=null) { s = s + pageQuestion + "; "; }
        if (pageAnswer!=null) { s = s + pageAnswer + "; "; }
        return s;
    }

    // Get question
    public String getQuestion() {
        return question;
    }

    // Get answer
    public String getAnswer() {
        return answer.replace("NEWLINE","\n");
    }

} 
