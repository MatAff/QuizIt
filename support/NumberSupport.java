
package support;

import java.util.function.*;
import java.util.*;

public class NumberSupport {

    // Create Integer from String exception returns null
    public static Integer createInteger(String s) {
    
        Integer i;

        try {
            i = Integer.valueOf(s);
        } catch (NumberFormatException e) {
            i = null;
        }

        return i;
    }
 
    // Interpolate 
    public static double interpolate(int currentIndex, int startIndex, double startVal,
                                      int endIndex, double endVal) {
        //System.out.println(currentIndex + " " + startIndex + " " + startVal + 
                           //" " + endIndex + " " +  endVal);
        return startVal + (endVal - startVal) * (currentIndex - startIndex) / (endIndex - startIndex);
    }

    // Generic static interpolation method
    public static <T, S> double interpolate(T t, List<T> list, Function<T,S> func) {
        
        S val = func.apply(t);
        if (val!=null) { 
            return Double.valueOf(val.toString());
        } else {
 
            int startIndex = -999;
            double startVal = -999;
            int endIndex = -999;
            double endVal = -999;

            int ind = list.indexOf(t);

            // Get start position
            for(int s = ind; s >= 0; s--) {
                S valS = func.apply(list.get(s));
                if(valS!=null) {
                    startIndex = s;
                    startVal = Double.valueOf(valS.toString());
                    break;
                }
            }

            // Get end position
            for(int e = ind; e < list.size(); e++) {
                S valE = func.apply(list.get(e));
                if(valE!=null) {
                    endIndex = e;
                    endVal = Double.valueOf(valE.toString());
                    break;
                }
            }

            // Interpolate and return
            return interpolate(ind, startIndex, startVal, endIndex, endVal); 
        }
    }

}

