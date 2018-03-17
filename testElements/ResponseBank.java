
package testElements;

import java.util.*;
import fileSupport.*;
import java.util.stream.*;

public class ResponseBank {

    String fileName;
    List<Response> responses;
    List<String> header;

    // Load responses from file
    public ResponseBank(String fileName) {
     
        this.fileName = fileName;

        // Initialize list
        responses = new ArrayList<>();

        // Load file
        List<List<String>> content = CSVtoList.getContent(fileName);

        // Add responses to list
        header = content.get(0);
        for(int i = 1; i < content.size(); i++) {
            List<String> line = content.get(i);
            responses.add(new Response(header, line));
        }
     
    }

    // Add response
    public void add(Item item, Boolean correct) {
        Response r = new Response(header, item, correct);
        responses.add(r);
    }

    // Save to CSV
    public void save() {

        // Convert response bank to list (for saving as csv)
        List<List<String>> l = this.toList();
        CSVtoList.writeContent(fileName, l);
    }

    // Method to print itembank
    public void print() {
        this.print(responses.size());
    }

    // Method to print itembank with limit
    public void print(int maxNr) {
        responses.stream().limit(maxNr).forEach(System.out::println);
    }

    // Compute proportion correct
    public double propCorrect(int nr) {
        long nrCorrect = responses.stream()
                         .skip(responses.size() - nr)
                         .filter(r -> r.correct)
                         .count();
        return nrCorrect / (double) nr;
    }

    // Compute proportion correct by chapter
    public double propCorrectChapter(int nr, int chapter) {
        List<Response> subRes = responses
            .stream()
            .filter(r -> r.chapter==chapter)
            .collect(Collectors.toList());
        Map<Boolean, List<Response>> p = subRes.stream()
            .skip(Math.max(subRes.size() - nr,0))
            .collect(Collectors.partitioningBy(r -> r.correct));
        return (double) p.get(true).size() / (p.get(false).size() + p.get(true).size());
    }
 
    // Get chapter list
    public List<Integer> getChapters() {
        List<Integer> chapters = responses.stream()
            .map(r -> r.chapter)
            .distinct()
            .sorted()
            .collect(Collectors.toList());
        return chapters;
    }

    // Method to convert response bank to list (for saving as csv)
    public List<List<String>> toList() {
        List<List<String>> l = new ArrayList<>();
        l.add(header);
        for(Response r : responses) {
            l.add(r.toList(header));
        }
        return l;
    }
 
} 

