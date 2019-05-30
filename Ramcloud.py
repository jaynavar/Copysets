import Replication
import scipy.misc

class RamcloudScheme(Replication.ReplicationScheme):
   def __init__(self, *args, **kwargs):
      super(RamcloudScheme, self).__init__(*args, **kwargs)

      self.chunksPerNode = 8000
      # comes from S = P (R - 1)
      #  S: scatter width
      #  P: number of permutations (fixed at 1)
      #  R: replication factor
      self.scatterWidth = self.replicationFactor - 1

class RamcloudRandomScheme(RamcloudScheme):
   def probabilityOfDataLossSimulation(self, numNodes):
      return self.simulationRandomDataLoss(
         self.trials, numNodes, self.chunksPerNode, self.replicationFactor,
         self.scatterWidth)

   def probabilityOfDataLossComputation(self, numNodes):
      return self.randomReplicationDataLoss(
         numNodes, self.chunksPerNode, self.replicationFactor)

   @staticmethod
   def plotInfo():
      return Replication.PlotInfo('RAMCloud, Random Replication',
                                  linestyle='--', marker='s', color='blue')

class RamcloudCopysetScheme(RamcloudScheme):
   def probabilityOfDataLossSimulation(self, numNodes):
      return self.simulationCopysetDataLoss(
         self.trials, numNodes, self.chunksPerNode, self.replicationFactor,
         self.scatterWidth)

   def probabilityOfDataLossComputation(self, numNodes):
      return self.copysetReplicationDataLoss(
         numNodes, self.chunksPerNode, self.replicationFactor, self.scatterWidth)

   @staticmethod
   def plotInfo():
      return Replication.PlotInfo('RAMCloud, Copyset Replication',
                                  linestyle='--', marker='o', markersize=10,
                                  color='maroon')
