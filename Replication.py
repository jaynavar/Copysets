import scipy.misc

class ReplicationScheme(object):
   def __init__(self, debug=False, replicationFactor=3):
      self.debug = debug
      self.replicationFactor = replicationFactor

   def probabilityOfDataLoss(self, numNodes):
      raise NotImplementedError

   def plotInfo(self):
      raise NotImplementedError

   @staticmethod
   def randomReplicationDataLoss(numNodes, chunksPerNode, replicationFactor):
      # compute the probability
      numFailedNodes = 0.01 * numNodes
      failedCombos = scipy.misc.comb(numFailedNodes, replicationFactor)
      totalCombos = scipy.misc.comb(numNodes, replicationFactor)
      probOfLosingChunk = failedCombos / totalCombos
      probOfDataLoss = 1.0 - (1.0 - probOfLosingChunk) ** (numNodes * chunksPerNode)

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

class PlotInfo(object):
   def __init__(self, label, linestyle='-', linewidth=4, marker='o',
                markevery=1000, markersize=8, markeredgewidth=0.0,
                color='blue', clip_on=False):
      self.label = label
      self.linestyle = linestyle
      self.linewidth = linewidth
      self.marker = marker
      self.markevery = markevery
      self.markersize = markersize
      self.markeredgewidth = markeredgewidth
      self.color = color
      self.clip_on = clip_on
