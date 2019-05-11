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

   def name(self):
      return 'HDFS, Random Replication'

class HdfsCopysetScheme(HdfsScheme):
   def probabilityOfDataLoss(self, numNodes):
      return self.copysetReplicationDataLoss(
         numNodes, self.chunksPerNode, self.replicationFactor, self.scatterWidth)

   def name(self):
      return 'HDFS, Copyset Replication'
