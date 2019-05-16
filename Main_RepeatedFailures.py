#!/usr/bin/env python2
import argparse
import RepeatedFailures

DEBUG = False

# Time units, in seconds
MINUTE = 60
HOUR = 60 * MINUTE
DAY = 24 * HOUR
WEEK = 7 * DAY

def runRepeatedFailuresExperiment(numNodes, numIntervals, numTrials):
   scatterWidths = [10, 50, 100, 500]
   # Failures every: 1 hour, 1 day, 1 week (in seconds)
   failureIntervals = [1 * MINUTE, 15 * MINUTE, 30 * MINUTE, 45 * MINUTE,
                       1 * HOUR, 1 * DAY]
   replicationFactor = 3
   # set node parameters (1 Gb/s, 1 TB per node), in Mb's, assuming
   # each peer can only dedicate 30% of capacity to node recovery
   nodeBandwidth = 1000
   nodeCapacity = 8 * 1000000
   recoveryUtil = 0.3

   intervalData = []
   for failureInterval in failureIntervals:
      print 'Failure Interval: %d' % failureInterval
      scatterWidthData = []
      for scatterWidth in scatterWidths:
         runner = RepeatedFailures.Runner(
            numNodes, scatterWidth, failureInterval, numIntervals, numTrials,
            replicationFactor, nodeBandwidth, nodeCapacity, recoveryUtil)
         probsOfDataLoss = runner.run()
         print 'Scatter Width: %d, Probs of Data Loss:\n%s' % (scatterWidth,
                                                               probsOfDataLoss)
         scatterWidthData.append((scatterWidth, probsOfDataLoss))
      print ''
      intervalData.append((failureInterval, scatterWidthData))

   # output the figures
   # TODO

if __name__ == '__main__':
   parser = argparse.ArgumentParser()
   parser.add_argument('-d', '--debug', action='store_true',
                       help='enable debugging output')
   parser.add_argument('-n', '--numNodes', default='5000',
                       help='number of nodes in cluster')
   parser.add_argument('-i', '--intervals', default='5',
                       help='number of repeated failures to graph')
   parser.add_argument('-t', '--trials', default='100',
                       help='number of trials for each datapoint')
   args = parser.parse_args()

   DEBUG = args.debug

   runRepeatedFailuresExperiment(int(args.numNodes), int(args.intervals),
                                 int(args.trials))
