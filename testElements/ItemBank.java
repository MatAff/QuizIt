
package testElements;

import java.util.*;
import fileSupport.*;
import java.util.stream.*;
import numberSupport.*;
import java.util.function.*;

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

        // Test generic interpolation method
        System.out.println(NSupport.interpolate(item, items, (theItem) -> theItem.pageQuestion));

        if (item.pageQuestion!=null) {
            return item.pageQuestion;
        } else {
 
            int startIndex = -999;
            int startPage = -999;
            int endIndex = -999;
            int endPage = -999;

            int ind = items.indexOf(item);

            Function<Item, Integer> func = theItem -> theItem.pageQuestion;
            for(int s = ind; s >= 0; s--) {
                Integer val = func.apply(items.get(s));
                //if(items.get(s).pageQuestion!=null) {
                if(val!=null) {
                    startIndex = s;
                    startPage = val; //items.get(s).pageQuestion;
                    break;
                }
            }
            for(int e = ind; e < items.size(); e++) {
                if(items.get(e).pageQuestion!=null) {
                    endIndex = e;
                    endPage = items.get(e).pageQuestion;
                    break;
                }
            }
            return NSupport.interpolate(ind, startIndex, startPage, endIndex, endPage);
        }
    }

} 
