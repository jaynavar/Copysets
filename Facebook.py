import Replication
import scipy.misc

class FacebookScheme(Replication.ReplicationScheme):
   def __init__(self, *args, **kwargs):
      super(FacebookScheme, self).__init__(*args, **kwargs)

      self.chunksPerNode = 10000
      self.scatterWidth = 10

class FacebookRandomScheme(FacebookScheme):
   def probabilityOfDataLoss(self, numNodes):
      # compute the probability
      numFailedNodes = 0.01 * numNodes
      failedCombos = scipy.misc.comb(numFailedNodes, self.replicationFactor)
      totalCopysets = scipy.misc.comb(numNodes, self.replicationFactor)
      numCopysets = (scipy.misc.comb(self.scatterWidth + 1,
                                     self.replicationFactor - 1)
                     * numNodes)
      probOfDataLoss = 1.0 - (1.0 - numCopysets / totalCopysets) ** failedCombos

      return probOfDataLoss

   def plotInfo(self):
      return Replication.PlotInfo('Facebook, Random Replication',
                                  linestyle='-.', marker='o', markersize=10,
                                  color='lime')

class FacebookCopysetScheme(FacebookScheme):
   def probabilityOfDataLoss(self, numNodes):
      return self.copysetReplicationDataLoss(
         numNodes, self.chunksPerNode, self.replicationFactor, self.scatterWidth)

   def plotInfo(self):
      return Replication.PlotInfo('Facebook, Copyset Replication',
                                  linestyle='-.', marker='s', color='fuchsia')
