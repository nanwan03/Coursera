import java.util.HashMap;
import java.util.Map;

// Block Chain should maintain only limited block nodes to satisfy the functions
// You should not have all the blocks added to the block chain in memory 
// as it would cause a memory overflow.

public class BlockChain {
	private static class BlockChainNode {
		private Block block;
		private UTXOPool uPool;
		private int height;
		public BlockChainNode(Block block, int parentHeight, UTXOPool uPool) {
			this.block = block;
			this.uPool = uPool;
			this.height = parentHeight + 1;
		}
		public int getHeight() {
			return this.height;
		}
		public Block getBlock() {
			return this.block;
		}
		public UTXOPool getuPool() {
			return this.uPool;
		}
	}
	private BlockChainNode maxHeightNode = null;
	private Map<ByteArrayWrapper, BlockChainNode> blockChainMap = new HashMap<ByteArrayWrapper, BlockChainNode>();
	private TransactionPool tPool = new TransactionPool();
    public static final int CUT_OFF_AGE = 10;

    /**
     * create an empty block chain with just a genesis block. Assume {@code genesisBlock} is a valid
     * block
     */
    public BlockChain(Block genesisBlock) {
        // IMPLEMENT THIS
    	UTXOPool uPool = new UTXOPool();
    	addCoinBasetoUPool(genesisBlock, uPool);
    	BlockChainNode bcNode = new BlockChainNode(genesisBlock, 0, uPool);
    	blockChainMap.put(new ByteArrayWrapper(genesisBlock.getHash()), bcNode);
    	maxHeightNode = bcNode;
    }

    /** Get the maximum height block */
    public Block getMaxHeightBlock() {
        // IMPLEMENT THIS
    	return this.maxHeightNode.getBlock();
    }

    /** Get the UTXOPool for mining a new block on top of max height block */
    public UTXOPool getMaxHeightUTXOPool() {
        // IMPLEMENT THIS
    	return this.maxHeightNode.getuPool();
    }

    /** Get the transaction pool to mine a new block */
    public TransactionPool getTransactionPool() {
        // IMPLEMENT THIS
    	return this.tPool;
    }

    /**
     * Add {@code block} to the block chain if it is valid. For validity, all transactions should be
     * valid and block should be at {@code height > (maxHeight - CUT_OFF_AGE)}.
     * 
     * <p>
     * For example, you can try creating a new block over the genesis block (block height 2) if the
     * block chain height is {@code <=
     * CUT_OFF_AGE + 1}. As soon as {@code height > CUT_OFF_AGE + 1}, you cannot create a new block
     * at height 2.
     * 
     * @return true if block is successfully added
     */
    public boolean addBlock(Block block) {
        // IMPLEMENT THIS
    	byte[] pHash = block.getPrevBlockHash();
    	if (pHash == null) {
    		return false;
    	}
    	BlockChainNode parentNode = blockChainMap.get(new ByteArrayWrapper(pHash));
    	if (parentNode == null) {
    		return false;
    	}
    	TxHandler txHandler = new TxHandler(new UTXOPool(parentNode.getuPool()));
    	Transaction[] blockTxs = block.getTransactions().toArray(new Transaction[0]);
    	Transaction[] tx = txHandler.handleTxs(blockTxs);
    	if (blockTxs.length != tx.length) {
    		return false;
    	}
    	int height = parentNode.getHeight() + 1;
    	if (height <= maxHeightNode.getHeight() - CUT_OFF_AGE) {
    		return false;
    	}
    	addCoinBasetoUPool(block, txHandler.getUTXOPool());
    	BlockChainNode bcNode = new BlockChainNode(block, parentNode.getHeight(), txHandler.getUTXOPool());
    	blockChainMap.put(new ByteArrayWrapper(block.getHash()), bcNode);
    	if (bcNode.getHeight() > maxHeightNode.getHeight()) {
    		maxHeightNode = bcNode;
    	}
    	return true;
    }

    /** Add a transaction to the transaction pool */
    public void addTransaction(Transaction tx) {
        // IMPLEMENT THIS
    	tPool.addTransaction(tx);
    }
    
    private void addCoinBasetoUPool(Block block, UTXOPool uPool) {
    	Transaction coinbase = block.getCoinbase();
    	for (int i = 0; i < coinbase.numOutputs(); ++i) {
    		Transaction.Output output = coinbase.getOutput(i);
    		UTXO uo = new UTXO(coinbase.getHash(), i);
    		uPool.addUTXO(uo, output);
    	}
    }
}