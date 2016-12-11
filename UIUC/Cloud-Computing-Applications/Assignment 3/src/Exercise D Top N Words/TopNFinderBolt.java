import backtype.storm.topology.BasicOutputCollector;
import backtype.storm.topology.OutputFieldsDeclarer;
import backtype.storm.topology.base.BaseBasicBolt;
import backtype.storm.tuple.Fields;
import backtype.storm.tuple.Tuple;
import backtype.storm.tuple.Values;

import java.util.HashMap;
import java.util.*;

/**
 * a bolt that finds the top n words.
 */
public class TopNFinderBolt extends BaseBasicBolt {
  private HashMap<String, Integer> currentTopWords = new HashMap<String, Integer>();
  private HashMap<String, Integer> wholeMap = new HashMap<String, Integer>();
  private TreeMap<Integer, List<String>> treeMap = new TreeMap<Integer, List<String>>(Collections.reverseOrder());
  private int N;

  private long intervalToReport = 20;
  private long lastReportTime = System.currentTimeMillis();

  public TopNFinderBolt(int N) {
    this.N = N;
  }

  @Override
  public void execute(Tuple tuple, BasicOutputCollector collector) {
 /*
    ----------------------TODO-----------------------
    Task: keep track of the top N words


    ------------------------------------------------- */
	String word = tuple.getString(0);
	Integer cound = tuple.getInteger(1);
	if (wholeMap.containsKey(word)) {
		wholeMap.put(word, wholeMap.get(word) + 1);
	} else {
		wholeMap.put(word, 1);
	}


    //reports the top N words periodically
    if (System.currentTimeMillis() - lastReportTime >= intervalToReport) {
    	
      treeMap.clear();
      currentTopWords.clear();
      for (Map.Entry<String, Integer> entry : wholeMap.entrySet()) {
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
    	int apparence = entry.getKey();
      	List<String> words = entry.getValue();
      	Collections.sort(words);
      	for (String token : words) {
      		if (index < this.N) {
      			currentTopWords.put(token, apparence);
      		}
      	}
      }
      
      collector.emit(new Values(printMap()));
      lastReportTime = System.currentTimeMillis();
    }
  }

  @Override
  public void declareOutputFields(OutputFieldsDeclarer declarer) {

     declarer.declare(new Fields("top-N"));

  }

  public String printMap() {
    StringBuilder stringBuilder = new StringBuilder();
    stringBuilder.append("top-words = [ ");
    for (String word : currentTopWords.keySet()) {
      stringBuilder.append("(" + word + " , " + currentTopWords.get(word) + ") , ");
    }
    int lastCommaIndex = stringBuilder.lastIndexOf(",");
    stringBuilder.deleteCharAt(lastCommaIndex + 1);
    stringBuilder.deleteCharAt(lastCommaIndex);
    stringBuilder.append("]");
    return stringBuilder.toString();

  }
}
