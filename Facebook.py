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

   def plotInfo(self):
      return Replication.PlotInfo('Facebook, Random Replication',
                                  linestyle='-.', marker='o', markersize=10,
                                  color='lime')

class FacebookCopysetScheme(FacebookScheme):
   def probabilityOfDataLoss(self, numNodes):
      # TODO
      return 0

   def plotInfo(self):
      return Replication.PlotInfo('Facebook, Copyset Replication',
                                  linestyle='-.', marker='s', color='fuchsia')
