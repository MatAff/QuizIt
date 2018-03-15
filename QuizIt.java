
import testElements.*;
import java.util.*;
import fileSupport.*; // Should be moved to ResponsesBank and not accessed from here

public class QuizIt {

    public static void main(String[] args) {

        // Set file names
        String ibFileName = "items.csv";
        String rbFileName = "responses.csv";

        // Load itembank
        ItemBank ib = new ItemBank(ibFileName);

        // Load responsebank
        ResponseBank rb = new ResponseBank(rbFileName);
        //rb.print(10);

        // Initialize PerformanceManager
        PerformManager pm = new PerformManager();

        // Select chapter
        List<Integer> chapters = Arrays.asList(12,13,14,15,16,17,18,19,20,21,22);

        // Get random item
        //Item i = ib.randomItem();
        //System.out.println(i);

        // Get item based on chapter number
        //List<Integer> chapters = Arrays.asList(1,2,3);
        //Item j = ib.chapterItem(chapters);
        //System.out.println(j);

        // Compute proportion correct
        //System.out.println(rb.propCorrect(5));
        //System.out.println(rb.propCorrect(10));
        //System.out.println(rb.propCorrectChapter(10,20));

        // Compute overview
        Map<Integer, Double> propMap = pm.getChapPerform(rb);
        System.out.println(pm.getChapBelow(0.75, chapters));
 
        // Convert response bank to list (for saving as csv)
        List<List<String>> l = rb.toList();
        CSVtoList.writeContent("test.csv", l);
        System.out.println(l);
        
    } 

} 

