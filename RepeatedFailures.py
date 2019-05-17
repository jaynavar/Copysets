import collections
import itertools as it
import numpy as np
import random

class Runner(object):
   def __init__(self, numNodes, scatterWidth, failureInterval, numIntervals,
                numTrials, replicationFactor, nodeBandwidth, nodeCapacity,
                recoveryUtil):
      self.numNodes = numNodes
      self.scatterWidth = scatterWidth
      self.failureInterval = failureInterval
      self.numIntervals = numIntervals
      self.numTrials = numTrials
      self.replicationFactor = replicationFactor
      self.nodeBandwidth = nodeBandwidth
      self.nodeCapacity = nodeCapacity
      self.recoveryUtil = recoveryUtil

      # computed params
      self.permutations = int(self.scatterWidth / float(self.replicationFactor - 1))

      # simulated cluster state
      self.copysets = None
      self.buddies = None
      self.liveNodes = None
      self.failedNodes = None
      self.lostData = None

   def run(self):
      probs = [[] for _ in range(self.numIntervals)]
      for _ in range(self.numTrials):
         # setup the cluster
         self.setup()
         for interval in range(self.numIntervals):
            # cause repeated failure, and compute probability of data loss
            probs[interval].append(self.failureProbOfDataLoss())
            # simulate recovery of the cluster over given interval
            # before next failure
            self.recover()

      # average the results from the trials
      data = []
      for interval in range(self.numIntervals):
         data.append((interval * self.failureInterval,
                      np.array(probs[interval]).mean()))
      return data

   def setup(self):
      # simulated cluster state
      self.copysets = set()
      self.buddies = collections.defaultdict(set)
      self.liveNodes = set(range(self.numNodes))
      self.failedNodes = set()
      self.lostData = False

      # generate copysets using Copyset Replication scheme
      shuffledNodes = range(self.numNodes)
      for p in xrange(self.permutations):
         # permute the nodes
         random.shuffle(shuffledNodes)
         # separate them into copysets, add to set of all copysets
         for i in xrange(0, len(shuffledNodes), self.replicationFactor):
            copyset = tuple(
               sorted(shuffledNodes[i : i + self.replicationFactor]))
            if len(copyset) == 3:
               self.copysets.add(copyset)

      # create mapping from node to the other nodes it shares
      # copysets with, used to determine recovery time
      for copyset in self.copysets:
         for node in copyset:
            self.buddies[node].update(copyset)
      for node in range(self.numNodes):
         self.buddies[node].remove(node)

   def failureProbOfDataLoss(self):
      # if lost data in previous failure, we are considered as having
      # lost data in this failure as well
      if self.lostData:
         return 1.0

      # fail 1% of the nodes (remove from live, add to failed)
      newFailedNodes = set(
         random.sample(self.liveNodes, int(0.01 * len(self.liveNodes))))
      self.liveNodes.difference_update(newFailedNodes)
      self.failedNodes.update(newFailedNodes)

      # determine if failed nodes form one of the generated copysets
      self.lostData = not self.copysets.isdisjoint(
         it.combinations(sorted(self.failedNodes), self.replicationFactor))

      if self.lostData:
         return 1.0
      else:
         return 0.0

   def recover(self):
      originalFailedNodes = self.failedNodes.copy()

      failedBuddies = collections.defaultdict(set)
      for failedNode in originalFailedNodes:
         # create mapping from alive nodes to nodes
         # they are helping recover
         aliveBuddies = [buddy for buddy in self.buddies[failedNode]
                         if buddy not in originalFailedNodes]
         for aliveBuddy in aliveBuddies:
            failedBuddies[aliveBuddy].add(failedNode)

      for failedNode in originalFailedNodes:
         aliveBuddies = [buddy for buddy in self.buddies[failedNode]
                         if buddy not in originalFailedNodes]

         # determine recovery time, based on network bandwidth
         # of each peer they can dedicate to recovery,
         # and amount of data being recovered
         totalBandwidth = sum(
            [self.recoveryUtil * self.nodeBandwidth / len(failedBuddies[aliveBuddy])
             for aliveBuddy in aliveBuddies])
         recoveryTime = self.nodeCapacity / float(totalBandwidth)

         # check if recovered before next failure
         if recoveryTime < self.failureInterval:
            # remove from failed set, add to live set
            self.failedNodes.remove(failedNode)
            self.liveNodes.add(failedNode)
