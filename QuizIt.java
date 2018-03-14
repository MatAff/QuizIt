
import testElements.*;
import java.util.*;

public class QuizIt {

    public static void main(String[] args) {

        // Set file name
        String fileName = "items.csv";

        // Load itembank
        ItemBank itemBank = new ItemBank(fileName);

        // Get random item
        Item i = itemBank.randomItem();
        System.out.println(i);

    } 

} 

