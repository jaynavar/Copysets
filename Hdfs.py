import Replication

class HdfsRandomScheme(Replication.ReplicationScheme):
   def probabilityOfDataLoss(self, numNodes):
      # TODO
      return 0

   def name(self):
      return 'HDFS, Random Replication'

class HdfsCopysetScheme(Replication.ReplicationScheme):
   def probabilityOfDataLoss(self, numNodes):
      # TODO
      return 0

   def name(self):
      return 'HDFS, Copyset Replication'
