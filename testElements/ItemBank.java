
package testElements;

import java.util.*;
import fileSupport.*;

public class ItemBank {

    // Create list of Items
    List<Item> items; 

    public ItemBank(String fileName) {
    
        // Load file content
        List<List<String>> content = CSVtoList.getContent(fileName);

        // Debug - Print content
        //CSVtoList.printContent(content, 10);

        // Initialize list
        items = new ArrayList<>();

        // Add items to list
        List<String> header = content.get(0);
        for(int i = 1; i < content.size(); i++) {
            List<String> line = content.get(i);
            items.add(new Item(header, line));
        }
     
        // Debug - Print itembank
        //this.printItemBank(10); 
    }
  
    // Method to print itembank
    public void printItemBank(int maxNr) {
        items.stream().limit(maxNr).forEach(System.out::println);
    }

    // Method to select and return random item
    public Item randomItem() {
        int itemNr = (int) (Math.random() * items.size());
        return items.get(itemNr);
    }

} 
