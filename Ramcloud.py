import Replication

class RamcloudRandomScheme(Replication.ReplicationScheme):
   def probabilityOfDataLoss(self, numNodes):
      # TODO
      return 0

   def name(self):
      return 'RAMCloud, Random Replication'

class RamcloudCopysetScheme(Replication.ReplicationScheme):
   def probabilityOfDataLoss(self, numNodes):
      # TODO
      return 0

   def name(self):
      return 'RAMCloud, Copyset Replication'
