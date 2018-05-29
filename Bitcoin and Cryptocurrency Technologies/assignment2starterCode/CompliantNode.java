import java.util.ArrayList;
import java.util.Set;
import java.util.HashSet;

/* CompliantNode refers to a node that follows the rules (not malicious)*/
public class CompliantNode implements Node {
	private Set<Integer> neighbors = new HashSet<Integer>();
	private Set<Transaction> txs = new HashSet<Transaction>();
    public CompliantNode(double p_graph, double p_malicious, double p_txDistribution, int numRounds) {
        // IMPLEMENT THIS
    }

    public void setFollowees(boolean[] followees) {
        // IMPLEMENT THIS
    	neighbors.clear();
    	for (int i = 0; i < followees.length; ++i) {
    		if (followees[i]) {
    			neighbors.add(i);
    		}
    	}
    }

    public void setPendingTransaction(Set<Transaction> pendingTransactions) {
        // IMPLEMENT THIS
    	this.txs = pendingTransactions;
    }

    public Set<Transaction> sendToFollowers() {
        // IMPLEMENT THIS
    	return this.txs;
    }

    public void receiveFromFollowees(Set<Candidate> candidates) {
        // IMPLEMENT THIS
    	for (Candidate cd : candidates) {
    		if (neighbors.contains(cd.sender)) {
    			txs.add(cd.tx);
    		}
    	}
    }
}
