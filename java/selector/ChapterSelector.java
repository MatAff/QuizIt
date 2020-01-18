
package selector;

import testElements.*;
import java.util.*;
import java.util.stream.*;
import java.util.function.*;

public class ChapterSelector implements Selector {

    List<Integer> chapters;
    List<Integer> probChaps;
    Item item;
    ItemBank ib;
    ResponseBank rb;
    PerformManager pm;

    public ChapterSelector(String loc, ResourceBundle settings) {

        // Set file names
        String ibFileName = loc + "/items.csv";
        String rbFileName = loc + "/responses.csv";

        // Load itembank and responsebank
        ib = new ItemBank(ibFileName);
        rb = new ResponseBank(rbFileName);

        // Initialize PerformanceManager
        pm = new PerformManager();
 
        // Set chapters
        chapters = getChapters(settings.getString("chapters"));
    }

    private List<Integer> getChapters(String chapString) {
        List<Integer> chapters = Arrays.asList(chapString.split(",")).
                                 stream().
                                 map(e -> Integer.valueOf(e)).
                                 collect(Collectors.toList());
        return chapters;
    }

    // Pick item
    public void pickItem() {

        // Select item
        item = ib.chapterItem(probChaps);
        System.out.println(item);
        System.out.println("Page number " + ib.interpolatePageQuestion(item));
        System.out.println("Page number answer " + ib.interpolatePageAnswer(item));
 
    }

    // Check answer
    public void checkAnswer(String input) {
        
        Boolean correct = input.equals("1");
        rb.add(item, correct);
 
    }

    // Check performance
    public void checkPerformance() {
        
        // Compute overview
        Map<Integer, Double> propMap = pm.getChapPerform(rb);
        System.out.println("Overall: " + pm.avgChapters(chapters));
        probChaps = pm.getChapBelow(0.80, chapters, true); // true > prints
        System.out.println("");
 
    }

    // Save responses
    public void saveResponses() {

        // Save responses
        rb.save();

    }

} 
