
import testElements.*;
import java.util.*;
import java.io.Console;

// TODO list
// * Read answer
// * Add answer to responses
// * Track performance over time
// * Use/test is
// * Make fileName an argument to start the program
// * Try to read Spanish items
// * Add further adaptability

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
        //List<Integer> chapters = Arrays.asList(12,13,14,15,16,17,18,19,20,21,22);
        List<Integer> chapters = Arrays.asList(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22);

        // Initialize console
        Console console = System.console(); // Created using singleton pattern
        String userInput = null;
  
        // Loop
        for(int i = 0; i < 5; i++) {
            
            // Compute overview
            Map<Integer, Double> propMap = pm.getChapPerform(rb);
            System.out.println("Overall: " + pm.avgChapters(chapters));
            List<Integer> probChaps = pm.getChapBelow(0.80, chapters, true); // true > prints
            System.out.println("");

            // Select item
            Item item = ib.chapterItem(probChaps);
            System.out.println(item);
            System.out.println("Page number " + ib.interpolatePageQuestion(item));
            System.out.println("Page number answer " + ib.interpolatePageAnswer(item));

            // Read something
            if (console != null) { userInput = console.readLine(); }
            System.out.println(userInput);

            // Process response
            Boolean correct = userInput.equals("1");
            rb.add(item, correct);
            
        }

        // Save responses
        rb.save();
        
    } 

} 
