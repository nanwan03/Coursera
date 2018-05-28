import java.util.*;

public class TxHandler {

    /**
     * Creates a public ledger whose current UTXOPool (collection of unspent transaction outputs) is
     * {@code utxoPool}. This should make a copy of utxoPool by using the UTXOPool(UTXOPool uPool)
     * constructor.
     */
	private UTXOPool uPool;
    public TxHandler(UTXOPool utxoPool) {
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
    	Set<Transaction> sets = new HashSet<Transaction>();
    	for (Transaction tx : possibleTxs) {
    		if (isValidTx(tx)) {
    			sets.add(tx);
    			for (Transaction.Input input : tx.getInputs()) {
    				UTXO uo = new UTXO(input.prevTxHash, input.outputIndex);
    				uPool.removeUTXO(uo);
    			}
    			for (int i = 0; i < tx.numOutputs(); ++i) {
    				UTXO uo = new UTXO(tx.getHash(), i);
    				uPool.addUTXO(uo, tx.getOutput(i));
    			}
    		}
    	}
    	return sets.toArray(new Transaction[sets.size()]);
    }

}
