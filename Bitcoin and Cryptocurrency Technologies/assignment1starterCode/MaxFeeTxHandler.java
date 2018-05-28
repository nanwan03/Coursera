import java.util.*;

public class MaxFeeTxHandler {
    /**
     * Creates a public ledger whose current UTXOPool (collection of unspent transaction outputs) is
     * {@code utxoPool}. This should make a copy of utxoPool by using the UTXOPool(UTXOPool uPool)
     * constructor.
     */
	private UTXOPool uPool;
    public MaxFeeTxHandler(UTXOPool utxoPool) {
        // IMPLEMENT THIS
    	uPool = new UTXOPool(utxoPool);
    }

    /**
     * @return true if:
     * (1) all outputs claimed by {@code tx} are in the current UTXO pool, 
     * (2) the signatures on each input of {@code tx} are valid, 
     * (3) no UTXO is claimed multiple times by {@code tx},
     * (4) all of {@code tx}s output values are non-negative, and
     * (5) the sum of {@code tx}s input values is greater than or equal to the sum of its output
     *     values; and false otherwise.
     */
    public boolean isValidTx(Transaction tx) {
        // IMPLEMENT THIS
    	UTXOPool tmp = new UTXOPool();
    	int size = tx.numInputs();
    	double inputValue = 0;
    	double outputValue = 0;
    	for (int i = 0; i < size; ++i) {
    		Transaction.Input input = tx.getInput(i);
    		UTXO uo = new UTXO(input.prevTxHash, input.outputIndex);
    		if (!uPool.contains(uo)) {
    			return false;
    		}
    		Transaction.Output output = uPool.getTxOutput(uo);
    		if (!Crypto.verifySignature(output.address, tx.getRawDataToSign(i), input.signature)) {
    			return false;
    		}
    		if (output.value < 0) {
    			return false;
    		}
    		if (tmp.contains(uo)) {
    			return false;
    		}
    		tmp.addUTXO(uo, output);
    		inputValue += output.value;
    	}
    	for (Transaction.Output output : tx.getOutputs()) {
    		if (output.value < 0) {
    			return false;
    		}
    		outputValue += output.value;
    	}
    	return inputValue >= outputValue;
    }
    
    /**
     * Handles each epoch by receiving an unordered array of proposed transactions, checking each
     * transaction for correctness, returning a mutually valid array of accepted transactions, and
     * updating the current UTXO pool as appropriate.
     */
    public Transaction[] handleTxs(Transaction[] possibleTxs) {
        // IMPLEMENT THIS
    	因为每次加入一个valid transaction都要update UTXOPool(remove inputs, add outputs)， 而UTXOPool决定了下一个transaction是不是valid的， 并且它还决定了一个transaction的fee
    	所以不能简单地将possibleTXs按照fee的大小排序。
    	根据每个transaction的inputs所对应的UTXO，将所有的transaction连接成graph (前一个transaction的output的UTXO是后一个transaction的input)，并且做拓扑排序，枚举每个拓扑排序的sum of fees，求最大值所对应的transaction set
	或者作DFS枚举每个可能的组合
    }

}
