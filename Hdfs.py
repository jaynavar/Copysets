import Replication

class HdfsScheme(Replication.ReplicationScheme):
   def __init__(self, *args, **kwargs):
      super(HdfsScheme, self).__init__(*args, **kwargs)

      self.chunksPerNode = 10000
      self.scatterWidth = 200

class HdfsRandomScheme(HdfsScheme):
   def probabilityOfDataLoss(self, numNodes):
      return self.randomReplicationDataLoss(
         numNodes, self.chunksPerNode, self.replicationFactor)

   def plotInfo(self):
      return Replication.PlotInfo('HDFS, Random Replication',
                                  linestyle='-', marker='D', color='red')

class HdfsCopysetScheme(HdfsScheme):
   def probabilityOfDataLoss(self, numNodes):
      return self.copysetReplicationDataLoss(
         numNodes, self.chunksPerNode, self.replicationFactor, self.scatterWidth)

   def plotInfo(self):
      return Replication.PlotInfo('HDFS, Copyset Replication',
                                  linestyle='-', marker='D', color='aqua')
