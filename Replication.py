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
         return self.probabilityOfDataLossSimulation(numNodes)
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
      probOfDataLoss = (1.0 - (1.0 - probOfLosingChunk) **
                        (numNodes * chunksPerNode / replicationFactor))

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
   def simulationCopysetDataLoss(trials, numNodes, chunksPerNode, replicationFactor,
                                 scatterWidth):
      # setup implicit parameters
      numFailedNodes = int(0.01 * numNodes)
      permutations = int(scatterWidth / float(replicationFactor - 1))

      shuffledNodes = range(numNodes)
      results = []
      for _ in range(trials):
         lostData = False
         for p in xrange(permutations):
            # permute the nodes
            random.shuffle(shuffledNodes)
            # separate them into copysets, check if any of the copysets
            # contain all failed nodes
            for i in xrange(0, numNodes, replicationFactor):
               if len([node for node in shuffledNodes[i : i + replicationFactor]
                       if node < numFailedNodes]) == replicationFactor:
                  # assume failed nodes are [0, #_failed_nodes)
                  lostData = True
                  break
            if lostData:
               break

         results.append(1.0 if lostData else 0.0)

      # return average of the results, which is probability of data loss
      return np.array(results).mean()

   @staticmethod
   def simulationRandomDataLoss(trials, numNodes, chunksPerNode, replicationFactor,
                                scatterWidth):
      numFailedNodes = int(0.01 * numNodes)
      numTotalChunks = numNodes * chunksPerNode / replicationFactor

      if numFailedNodes < replicationFactor:
         # can't lose data if not enough nodes failed
         return 0.0

      results = []
      for _ in range(trials):
         lostData = False
         for _ in range(numTotalChunks):
            # assume failed nodes are [0, #_failed_nodes)
            if (len([n for n in random.sample(xrange(numNodes), replicationFactor)
                     if n < numFailedNodes])
                == replicationFactor):
               lostData = True
               break

         results.append(1.0 if lostData else 0.0)

      # return average of the results, which is probability of data loss
      return np.array(results).mean()

   @staticmethod
   def simulationFacebookRandomDataLoss(trials, numNodes, chunksPerNode,
                                        replicationFactor, scatterWidth):
      numFailedNodes = int(0.01 * numNodes)

      if numFailedNodes < replicationFactor:
         # can't lose data if not enough nodes failed
         return 0.0

      results = []
      nodesWrap = range(numNodes) + range(numNodes)
      for _ in range(trials):
         lostData = False
         failedNodes = sorted(random.sample(xrange(numNodes), numFailedNodes))

         # check if Facebook strawman replication scheme could have generated
         # any of the subsets
         #
         # NOTE: Facebook's scheme works by selecting the next "S" neighbors for
         # each node as its buddies
         failedNodesWrap = failedNodes + failedNodes
         for i, failedNode in enumerate(failedNodes):
            # if the next "RF - 1" nodes are within the "S" range, it means
            # this could have been a copyset data was replicated to (which we
            # assume means data *was* replicated to it)
            failedNodesInReach = failedNodesWrap[i + 1 :
                                                 i + (replicationFactor - 1) + 1]
            buddies = nodesWrap[failedNode + 1 :
                                failedNode + (scatterWidth + 1) + 1]
            if set(failedNodesInReach).issubset(set(buddies)):
               lostData = True
               break

         results.append(1.0 if lostData else 0.0)

      # return average of the results, which is probability of data loss
      return np.array(results).mean()

   @staticmethod
   def perChunkSimulationDataLoss(trials, numNodes, chunksPerNode,
                                  replicationFactor, generateReplicationFunc):
      results = []
      for _ in range(trials):
         # setup other parameters, we only have cluster at 80% load to avoid
         # failed replication due to insufficient space on nodes' buddies
         totalChunks = int(0.8 * chunksPerNode * numNodes / replicationFactor)
         nodes = range(numNodes)

         # replicate chunks across the cluster, generating a copyset for each chunk
         chunkReplicationFunc = generateReplicationFunc()
         copysets = set([tuple(sorted(chunkReplicationFunc()))
                         for _ in range(totalChunks)])

         # compute 1% of nodes that will fail
         failedNodes = sorted(random.sample(nodes, int(0.01 * numNodes)))

         # determine if failed nodes form a copyset that is replicated to
         lostData = not copysets.isdisjoint(
            it.combinations(failedNodes, replicationFactor))

         results.append(1.0 if lostData else 0.0)

      # return average of the results, which is probabilty of data loss
      return np.array(results).mean()

   @staticmethod
   def generateRandomReplicationFunc(numNodes, chunksPerNode, replicationFactor,
                                     scatterWidth):
      def generateReplicationFunc():
         nodes = set(range(numNodes))
         # node capacities map
         capacities = {nodeId: chunksPerNode for nodeId in nodes}
         # generate buddy groups for each node
         buddies = {nodeId: random.sample(nodes - {nodeId}, scatterWidth)
                    for nodeId in nodes}

         def decrementCapacities(nodes):
            for node in nodes:
               capacities[node] -= 1
               if capacities[node] == 0:
                  # remove the node if it is out of room
                  del capacities[node]

         def chunkReplicationFunc():
            while True:
               # choose primary replica from nodes with capacity
               primary = random.choice(capacities.keys())

               # choose secondary replicas from the buddy group
               buddiesWithRoom = [buddy for buddy in buddies[primary]
                                  if buddy in capacities]
               if len(buddiesWithRoom) < replicationFactor - 1:
                  # no eligible buddies for this primary
                  continue
               copyset = ([primary] +
                          random.sample(buddiesWithRoom, replicationFactor - 1))

               # decrement the capacities for each replica
               decrementCapacities(copyset)

               return copyset

         def simpleChunkReplicationFunc():
            copyset = random.sample(capacities.keys(), replicationFactor)
            # decrement the capacities for each replica
            decrementCapacities(copyset)
            return copyset

         if scatterWidth < numNodes - 1:
            return chunkReplicationFunc
         else:
            return simpleChunkReplicationFunc

      return generateReplicationFunc

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
