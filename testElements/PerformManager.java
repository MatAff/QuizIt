
package testElements;

import java.util.*;
import java.util.stream.*;
import printSupport.*;

public class PerformManager {

    int minChap;
    int maxChap;
    Map<Integer, Double> propMap;
    List<Integer> problemChap;

    // Constructor
    public PerformManager() {}

    // Constructor 
    public PerformManager(ItemBank ib) {
        
    }

    // Get chapter overview
    public Map<Integer, Double> getChapPerform(ResponseBank rb) {

        // Initialize map
        propMap = new HashMap<>();

        // Get list of chapters present
        List<Integer> chapter = rb.getChapters();
        for(Integer c : chapter) {
            Double prop = rb.propCorrectChapter(20,c);
            prop = (double) Math.round(prop*1000)/1000;
            propMap.put(c, prop);
        }  
 
        // Return map
        return propMap;

    }
 
    // Get average across selected chapters
    public double avgChapters(List<Integer> chapters) {
        List<Double> vals = new ArrayList<>();
        for(Integer c : chapters) {
            vals.add(propMap.get(c));
        }
        return vals.stream().mapToDouble(d -> d).average().getAsDouble();
    }

    // Get chapter below thresshold
    public List<Integer> getChapBelow(double th, List<Integer> chapters, boolean print) {
        problemChap = new ArrayList<>();
        for(Integer c : chapters) {
            if (propMap.get(c) < th) {
                problemChap.add(c);
                PSupport.printColor(c + " " + propMap.get(c),"red");
            } else {
                PSupport.printColor(c + " " + propMap.get(c),"green");
            }
        }
        return problemChap;
    }
}

