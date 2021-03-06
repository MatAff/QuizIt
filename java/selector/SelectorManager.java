
package selector;

import java.util.*;

public class SelectorManager {

    public static Selector get(String loc, ResourceBundle settings) {
    
        String method = settings.getString("method");

        Selector s = null;

        if (method.equals("chapter")) { s = new ChapterSelector(loc, settings); }
        if (method.equals("item")) { s = new ItemSelector(loc, settings); }

        return s;
    }

} 
