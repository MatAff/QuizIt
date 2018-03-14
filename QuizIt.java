
import testElements.*;
import java.util.*;

public class QuizIt {

    public static void main(String[] args) {

        // Set file names
        String ibFileName = "items.csv";
        String rbFileName = "responses.csv";

        // Load itembank
        ItemBank ib = new ItemBank(ibFileName);

        // Load responsebank
        ResponseBank rb = new ResponseBank(rbFileName);
        //rb.print(10);

        // Get random item
        Item i = ib.randomItem();
        System.out.println(i);

    } 

} 

