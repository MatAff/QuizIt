
import testElements.*;
import selector.*;
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
 
        // Check argument has been entered
        // TODO

        // Get settings
        ResourceBundle settings = ResourceBundle.getBundle(args[0] + "/settings");
        System.out.println(settings.getString("method"));

        // Get Selector
        Selector s = SelectorManager.get(args[0], settings);

        // Initialize console
        Console console = System.console(); // Created using singleton pattern
        String userInput = null;
  
        // Loop
        for(int i = 0; i < 5; i++) {
            
            // Check performance and pick new item
            s.checkPerformance();
            s.pickItem();

            // Read answer
            if (console != null) { userInput = console.readLine(); }
            System.out.println(userInput);

            // Process response
            s.checkAnswer(userInput);

       }

       // Save responses
       s.saveResponses();
        
    } 

} 
