
package testElements;

import java.util.*;
import fileSupport.*;

public class ResponseBank {

    // List of responses
    List<Response> responses;

    // Load responses from file
    public ResponseBank(String fileName) {

        // Initialize list
        responses = new ArrayList<>();

        // Load file
        List<List<String>> content = CSVtoList.getContent(fileName);

        // Add responses to list
        List<String> header = content.get(0);
        for(int i = 1; i < content.size(); i++) {
            List<String> line = content.get(i);
            responses.add(new Response(header, line));
        }
     
    }

    // Method to print itembank
    public void print(int maxNr) {
        responses.stream().limit(maxNr).forEach(System.out::println);
    }

 
} 

