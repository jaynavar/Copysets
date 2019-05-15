import itertools as it
import numpy as np
import random
import scipy.misc

class ReplicationScheme(object):
   def __init__(self, debug=False, simulation=False, trials=100,
                replicationFactor=3):
      self.debug = debug
      self.simulation = simulation
      self.trials = trials
      self.replicationFactor = replicationFactor

   def probabilityOfDataLoss(self, numNodes):
      if self.simulation:
         results = np.array([self.probabilityOfDataLossSimulation(numNodes)
                             for _ in range(self.trials)])
         if self.debug:
            print 'Average for %d in %s: %f' % (numNodes, self.__class__,
                                                results.mean())
         return results.mean()
      else:
         return self.probabilityOfDataLossComputation(numNodes)

   def probabilityOfDataLossSimulation(self, numNodes):
      raise NotImplementedError

   def probabilityOfDataLossComputation(self, numNodes):
      raise NotImplementedError

   def plotInfo(self):
      raise NotImplementedError

   @staticmethod
   def randomReplicationDataLoss(numNodes, chunksPerNode, replicationFactor):
      # compute the probability
      numFailedNodes = 0.01 * numNodes
      failedCombos = scipy.misc.comb(numFailedNodes, replicationFactor)
      totalCombos = scipy.misc.comb(numNodes, replicationFactor)
      probOfLosingChunk = failedCombos / totalCombos
      probOfDataLoss = 1.0 - (1.0 - probOfLosingChunk) ** (numNodes * chunksPerNode)

      return probOfDataLoss

   @staticmethod
   def copysetReplicationDataLoss(numNodes, chunksPerNode, replicationFactor,
                                  scatterWidth):
      # compute the probability
      numFailedNodes = 0.01 * numNodes
      failedCombos = scipy.misc.comb(numFailedNodes, replicationFactor)
      totalCopysets = scipy.misc.comb(numNodes, replicationFactor)
      numCopysets = (((scatterWidth + 1) / (replicationFactor - 1)) * numNodes /
                     replicationFactor)
      probOfDataLoss = 1.0 - (1.0 - numCopysets / totalCopysets) ** failedCombos

      return probOfDataLoss

   @staticmethod
   def totalChunks(numNodes, chunksPerNode, replicationFactor):
      roughChunks = int(0.8 * chunksPerNode * numNodes / replicationFactor)
      # round to multiple of numNodes, makes dividing easier
      totalChunks = int(numNodes * round(float(roughChunks) / numNodes))
      return totalChunks

   @staticmethod
   def simulationDataLoss(numNodes, chunksPerNode, replicationFactor,
                          copysetsFunc):
      # setup other parameters, we only have cluster at 80% load to avoid
      # failed replication due to insufficient space on nodes' buddies
      totalChunks = ReplicationScheme.totalChunks(numNodes, chunksPerNode,
                                                  replicationFactor)
      nodes = range(numNodes)

      # get the copysets for the given replication scheme
      copysets = copysetsFunc()

      # compute 1% of nodes that will fail
      failedNodes = sorted(random.sample(nodes, int(0.01 * numNodes)))

      # determine if failed nodes form a copyset that is replicated to
      lostData = not copysets.isdisjoint(
         it.combinations(failedNodes, replicationFactor))

      if lostData:
         # we lost data, so return data loss probability of 1.0
         return 1.0
      else:
         # we did not lose data, so return data loss probability of 0.0
         return 0.0

   @staticmethod
   def generateRandomReplicationFunc(numNodes, chunksPerNode, replicationFactor,
                                     scatterWidth):
      totalChunks = ReplicationScheme.totalChunks(numNodes, chunksPerNode,
                                                  replicationFactor)
      nodes = set(range(numNodes))
      # generate buddy groups for each node
      buddies = {nodeId: random.sample(nodes - {nodeId}, scatterWidth)
                 for nodeId in nodes}
      # number of chunks that each node is primary for
      primarySize = int(totalChunks / numNodes)
      # create map of node to chunks it's primary for
      primaryChunks = {nodeId: xrange(nodeId * primarySize,
                                      (nodeId + 1) * primarySize)
                       for nodeId in nodes}

      def copysetsFunc():
         # for each node, map its primary chunks to buddy nodes,
         # each generating a copyset
         

      return copysetsFunc

class PlotInfo(object):
   def __init__(self, label, linestyle='-', linewidth=4, marker='o',
                markevery=1000, markersize=8, markeredgewidth=0.0,
                color='blue', clip_on=False):
      self.label = label
      self.linestyle = linestyle
      self.linewidth = linewidth
      self.marker = marker
      self.markevery = markevery
      self.markersize = markersize
      self.markeredgewidth = markeredgewidth
      self.color = color
      self.clip_on = clip_on
