
package fileSupport;

import java.io.*;
import java.util.*;

public class CSVtoList {

    // Method to load content into two-dimentional list
    public static List<List<String>> getCsvContent(String fileName) {

        // Create file
        File f = new File(fileName);
        //System.out.println(f.getAbsolutePath()); // Debug

        // Create list
        List<List<String>> lines = new ArrayList<>();

        // Open file
        try (BufferedReader br = new BufferedReader(new FileReader(f))) {
            
            // Put content in lines
            String line;
            while ((line = br.readLine()) != null) {
            
                String[] parts = line.split(",");
                lines.add(Arrays.asList(parts));
 
            }

        } catch (IOException e) {
             e.printStackTrace();
        } 

        // Return list
        return lines;

    }

    // Method to print two-dimentional list to console
    public static void printCsvContent(List<List<String>> content, int maxLine) {
    
        for(int l = 0;l < maxLine; l++)
        {
            System.out.println(content.get(l));
        }

    } 

} 

