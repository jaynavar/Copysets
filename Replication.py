import scipy.misc

class ReplicationScheme(object):
   def __init__(self, debug=False, replicationFactor=3):
      self.debug = debug
      self.replicationFactor = replicationFactor

   def probabilityOfDataLoss(self, numNodes):
      raise NotImplementedError

   def name(self):
      raise NotImplementedError

   @staticmethod
   def randomReplicationDataLoss(numNodes, chunksPerNode, replicationFactor):
      # compute the probability
      numFailedNodes = 0.01 * numNodes
      failedCombos = scipy.misc.comb(numFailedNodes, replicationFactor)
      totalCombos = scipy.misc.comb(numNodes, replicationFactor)
      probOfLosingChunk = failedCombos / totalCombos
      numChunks = numNodes * chunksPerNode
      probOfDataLoss = 1.0 - (1.0 - probOfLosingChunk) ** (numNodes * numChunks)

      return probOfDataLoss

   @staticmethod
   def copysetReplicationDataLoss(numNodes, chunksPerNode, replicationFactor,
                                  scatterWidth):
      # compute the probability
      numFailedNodes = 0.01 * numNodes
      failedCombos = scipy.misc.comb(numFailedNodes, replicationFactor)
      totalCopysets = scipy.misc.comb(numNodes, replicationFactor)
      numCopysets = ((scatterWidth / (replicationFactor - 1)) * numNodes /
                     replicationFactor)
      probOfDataLoss = 1.0 - (1.0 - numCopysets / totalCopysets) ** failedCombos

      return probOfDataLoss
