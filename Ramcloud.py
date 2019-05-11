import Replication
import scipy.misc

class RamcloudScheme(Replication.ReplicationScheme):
   def __init__(self, *args, **kwargs):
      super(RamcloudScheme, self).__init__(*args, **kwargs)

      self.chunksPerNode = 8000

class RamcloudRandomScheme(RamcloudScheme):
   def probabilityOfDataLoss(self, numNodes):
      return self.randomReplicationDataLoss(
         numNodes, self.chunksPerNode, self.replicationFactor)

   def name(self):
      return 'RAMCloud, Random Replication'

class RamcloudCopysetScheme(RamcloudScheme):
   def probabilityOfDataLoss(self, numNodes):
      # comes from S = P (R - 1)
      #  S: scatter width
      #  P: number of permutations (fixed at 1)
      #  R: replication factor
      scatterWidth = self.replicationFactor - 1

      return self.copysetReplicationDataLoss(
         numNodes, self.chunksPerNode, self.replicationFactor, scatterWidth)

   def name(self):
      return 'RAMCloud, Copyset Replication'
