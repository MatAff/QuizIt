
import testElements.*;
import java.util.*;

public class QuizIt {

    public static void main(String[] args) {

        // Set file names
        String ibFileName = "items.csv";
        String rbFileName = "responses.csv";

        // Load itembank and responsebank
        ItemBank ib = new ItemBank(ibFileName);
        ResponseBank rb = new ResponseBank(rbFileName);

        // Initialize PerformanceManager
        PerformManager pm = new PerformManager();

        // Select chapter
        List<Integer> chapters = Arrays.asList(12,13,14,15,16,17,18,19,20,21,22);

        // Loop
        for(int i = 0; i < 5; i++) {
            
            // Compute overview
            Map<Integer, Double> propMap = pm.getChapPerform(rb);
            List<Integer> probChaps = pm.getChapBelow(0.75, chapters);
            Item j = ib.chapterItem(chapters);
            System.out.println(j);
            
        }

        // Save responses
        rb.save();
        
    } 

} 
