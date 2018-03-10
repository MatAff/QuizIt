
package testElements;

import java.util.*;
import fileSupport.*;

public class ItemLoader {

    public static List<Item> load(String fileName) {
    
        // Load file content
        List<List<String>> content = CSVtoList.getCsvContent(fileName);

        // Debug - Print content
        CSVtoList.printCsvContent(content, 10);

        // Create list of Items
        List<Item> items = new ArrayList<>();

        // Add items to list
        for(int i = 1; i < content.size(); i++) {
            List<String> line;
            
        }
 
        // Return 
        return items;

    }

} 
