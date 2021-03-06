
package testElements;

import support.*;
import java.util.*;
import java.util.stream.*;
import java.util.function.*;

public class ItemBank {

    // Create list of Items
    List<Item> items; 

    public ItemBank(String fileName) {
    
        // Load file content
        List<List<String>> content = CSV.getContent(fileName);

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
  
    public void printItemBank() {
        this.printItemBank(items.size());
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

    // Method to select random item from a list of itemNrs
    public Item randomItem(List<Integer> itemNrs) {
        int nr = (int) (Math.random() * itemNrs.size());
        Integer itemNr = itemNrs.get(nr);
        System.out.println(itemNr);
        return items.stream().filter(i -> i.itemNr.equals(itemNr)).findFirst().get();
    }

    // Get all item numbers
    public List<Integer> getAllItemNrs() {
        return items.stream().
               map(i -> i.itemNr).
               collect(Collectors.toList());
    }

    // Select from chapter
    public Item chapterItem(List<Integer> chapters) {
        List<Item> subItems = items.stream().
                              filter(i -> chapters.contains(i.chapter)).
                              collect(Collectors.toList());
        int itemNr = (int) (Math.random() * subItems.size());
        return subItems.get(itemNr);
    }

    // Interpolation of page question number
    public double interpolatePageQuestion(Item item) {

        // Using generic interpolation method
        double page = NumberSupport.interpolate(item, items, theItem -> theItem.pageQuestion);
        return (double) Math.round(page*100)/100;
    }

    // Interpolation of page answer number
    public double interpolatePageAnswer(Item item) {

        // Using generic interpolation method
        double page = NumberSupport.interpolate(item, items, theItem -> theItem.pageAnswer);
        return (double) Math.round(page*100)/100;
    }

} 
