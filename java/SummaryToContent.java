
import java.util.*;
import java.io.*;
import java.nio.file.*;
import java.util.stream.*;
import java.text.*;
import support.*;

public class SummaryToContent {

    // Function to check if line contains item and return number of answer lines
    private static int getAnswerNumber(String line) {
    
        // Return zero if line does not contain []
        if(!line.contains("[")) return 0;

        // Get number section
        int pos = line.indexOf("[");
        String subString = line.substring(pos + 1);
        //System.out.println(subString);

        // Parse to number
        int nrLines = 0;
        try {
            NumberFormat en = NumberFormat.getIntegerInstance();
            nrLines = Integer.parseInt(en.parse(subString).toString());
        } catch(ParseException e) {
            e.printStackTrace();
        }

        // Number
        return nrLines;
    }

    public static void main(String[] args) {

        // Filename
        String fileName = args[0] + "/summary.txt";

        // Create content list
        List<List<String>> content = new ArrayList<>();
        int itemNr = 0;
        List<String> header = Arrays.asList("ItemNr","Question","Answer");
        content.add(header);

        // File reader
        try {

            // Get content
            List<String> l = Files.readAllLines(Paths.get(fileName));

            // Print content
            for(int i = 0; i < l.size(); i++) {
                 
                 // Read content
                 String line = l.get(i);
                 int nrLines = getAnswerNumber(line);
                 if (nrLines > 0) {
     
                     // Answer
                     List<String> a = new ArrayList<>();
                     for(int aNr = 0; aNr < nrLines; aNr++) {
                         a.add(l.get(i + aNr + 1));
                     }
                     String answer = String.join("NEWLINE", a);
                     answer = answer.replace(",","");

                     // Create list and add
                     line = line.replace(",","");
                     List<String> itemContent = Arrays.asList(Integer.toString(++itemNr),line,answer);
                     content.add(itemContent);

                 }
            }

	} catch(IOException e) {
            e.printStackTrace();
        }

        // Print content
        //System.out.println(content);

        // Write to CSV
        CSV.writeContent(args[0] + "/items.csv",content);

    } 

}

