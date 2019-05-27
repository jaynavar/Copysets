import Replication

class HdfsScheme(Replication.ReplicationScheme):
   def __init__(self, *args, **kwargs):
      super(HdfsScheme, self).__init__(*args, **kwargs)

      self.chunksPerNode = 10000
      self.scatterWidth = 200

class HdfsRandomScheme(HdfsScheme):
   def probabilityOfDataLossSimulation(self, numNodes):
      # TODO
      return 0

   def probabilityOfDataLossComputation(self, numNodes):
      return self.randomReplicationDataLoss(
         numNodes, self.chunksPerNode, self.replicationFactor)

   @staticmethod
   def plotInfo():
      return Replication.PlotInfo('HDFS, Random Replication',
                                  linestyle='-', marker='D', color='red')

class HdfsCopysetScheme(HdfsScheme):
   def probabilityOfDataLossSimulation(self, numNodes):
      return self.simulationCopysetDataLoss(
         self.trials, numNodes, self.chunksPerNode, self.replicationFactor,
         self.scatterWidth)

   def probabilityOfDataLossComputation(self, numNodes):
      return self.copysetReplicationDataLoss(
         numNodes, self.chunksPerNode, self.replicationFactor, self.scatterWidth)

   @staticmethod
   def plotInfo():
      return Replication.PlotInfo('HDFS, Copyset Replication',
                                  linestyle='-', marker='D', color='aqua')
