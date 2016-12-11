import java.io.File;
import java.lang.reflect.Array;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.*;
import java.io.*;

public class MP1 {
    Random generator;
    String userName;
    String inputFileName;
    String delimiters = " \t,;.?!-:@[](){}_*/";
    String[] stopWordsArray = {"i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours",
            "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its",
            "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that",
            "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having",
            "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while",
            "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before",
            "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again",
            "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each",
            "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than",
            "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"};

    void initialRandomGenerator(String seed) throws NoSuchAlgorithmException {
        MessageDigest messageDigest = MessageDigest.getInstance("SHA");
        messageDigest.update(seed.toLowerCase().trim().getBytes());
        byte[] seedMD5 = messageDigest.digest();

        long longSeed = 0;
        for (int i = 0; i < seedMD5.length; i++) {
            longSeed += ((long) seedMD5[i] & 0xffL) << (8 * i);
        }

        this.generator = new Random(longSeed);
    }

    Integer[] getIndexes() throws NoSuchAlgorithmException {
        Integer n = 10000;
        Integer number_of_lines = 50000;
        Integer[] ret = new Integer[n];
        this.initialRandomGenerator(this.userName);
        for (int i = 0; i < n; i++) {
            ret[i] = generator.nextInt(number_of_lines);
        }
        return ret;
    }

    public MP1(String userName, String inputFileName) {
        this.userName = userName;
        this.inputFileName = inputFileName;
    }

    public String[] process() throws Exception {
        String[] ret = new String[20];
        
        Integer[] indexes = getIndexes();
        /* convert String array to ArrayList */
        List<String> stopWords = Arrays.asList(stopWordsArray);
        
        /* read file into memory */
        List<String> lines = new ArrayList<String>();
        BufferedReader br = new BufferedReader(new FileReader(this.inputFileName));
        String read = null;
        while ((read = br.readLine()) != null) {
        	lines.add(read);
        }
        br.close();
        
        /* split tokens */
        List<String> tokens = new ArrayList<String>();
        for (int i : indexes) {
        	String line = lines.get(i);
        	StringTokenizer st = new StringTokenizer(line, delimiters);
    		while (st.hasMoreTokens()) {
    			String token = st.nextToken().toLowerCase().trim();
    			if (!stopWords.contains(token)) {
    				tokens.add(token);
    			}
    		}
        }
        
        /* Mapping string -> apparence */
        Map<String, Integer> rst = new HashMap<String, Integer>();
        for (String token : tokens) {
        	if (rst.containsKey(token)) {
        		rst.put(token, rst.get(token) + 1);
        	} else {
        		rst.put(token, 1);
        	}
        }
        
        /* create inverted index */
        TreeMap<Integer, List<String>> treeMap = new TreeMap<Integer, List<String>>(Collections.reverseOrder());
        for (Map.Entry<String, Integer> entry : rst.entrySet()) {
        	String token = entry.getKey();
        	int apparence = entry.getValue();
        	if (treeMap.containsKey(apparence)) {
        		if (treeMap.get(apparence).contains(token)) {
        			continue;
        		}
        	} else {
        		treeMap.put(apparence, new ArrayList<String>());
        	}
        	treeMap.get(apparence).add(token);
        }
        
        int index = 0;
        for (Map.Entry<Integer, List<String>> entry : treeMap.entrySet()) {
        	List<String> words = entry.getValue();
        	Collections.sort(words);
        	for (String word : words) {
        		if (index < ret.length) {
        			ret[index++] = word;
        		}
        	}
        }

        return ret;
    }

    public static void main(String[] args) throws Exception {
        if (args.length < 1){
            System.out.println("MP1 <User ID>");
        }
        else {
            String userName = args[0];
            String inputFileName = "./input.txt";
            MP1 mp = new MP1(userName, inputFileName);
            String[] topItems = mp.process();
            for (String item: topItems){
               System.out.println(item);
            }
        }
    }
}
