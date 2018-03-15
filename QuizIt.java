
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
        rb.print(10);
        //rb.print();

        // Get random item
        Item i = ib.randomItem();
        System.out.println(i);

        // Get item based on chapter number
        List<Integer> chapters = Arrays.asList(1,2,3);
        Item j = ib.chapterItem(chapters);
        System.out.println(j);

        // Compute proportion correct
        System.out.println(rb.propCorrect(5));
        System.out.println(rb.propCorrect(10));
        System.out.println(rb.propCorrectChapter(10,20));

    } 

} 

