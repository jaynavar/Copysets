import Replication

class FacebookScheme(Replication.ReplicationScheme):
   def __init__(self, *args, **kwargs):
      super(FacebookScheme, self).__init__(*args, **kwargs)

      self.chunksPerNode = 10000
      self.scatterWidth = 10

class FacebookRandomScheme(FacebookScheme):
   def probabilityOfDataLoss(self, numNodes):
      # TODO
      return 0

   def name(self):
      return 'Facebook, Random Replication'

class FacebookCopysetScheme(FacebookScheme):
   def probabilityOfDataLoss(self, numNodes):
      # TODO
      return 0

   def name(self):
      return 'Facebook, Copyset Replication'
