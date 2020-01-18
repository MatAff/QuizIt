
package support;

import java.io.*;
import java.util.*;
import java.util.stream.*;

public class CSV {

    // Method to write content to file
    public static void writeContent(String fileName, List<List<String>> content) {
        try {
            FileWriter pw = new FileWriter(fileName);
            for(List<String> l : content) {
                String line = l.stream()
                    .collect(Collectors.joining(","));
                pw.append(line);
                pw.append("\n");
            }
            pw.flush();
            pw.close();
        } catch (IOException e) {

        }
    }

    // Method to load content into two-dimentional list
    public static List<List<String>> getContent(String fileName) {

        // Create file
        File f = new File(fileName);

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
    public static void printContent(List<List<String>> content, int maxLine) {
    
        for(int l = 0;l < maxLine; l++)
        {
            System.out.println(content.get(l));
        }

    } 

} 
