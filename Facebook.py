import Replication

class FacebookRandomScheme(Replication.ReplicationScheme):
   def probabilityOfDataLoss(self, numNodes):
      # TODO
      return 0

   def name(self):
      return 'Facebook, Random Replication'

class FacebookCopysetScheme(Replication.ReplicationScheme):
   def probabilityOfDataLoss(self, numNodes):
      # TODO
      return 0

   def name(self):
      return 'Facebook, Copyset Replication'
