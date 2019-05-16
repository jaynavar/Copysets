#!/usr/bin/env python2
import argparse
import RepeatedFailures

DEBUG = False

# Time units, in seconds
MINUTE = 60
HOUR = 60 * MINUTE
DAY = 24 * HOUR
WEEK = 7 * DAY

def runRepeatedFailuresExperiment(numNodes, intervals):
   scatterWidths = [10, 200, 1000]
   # Failures every: 1 hour, 1 day, 1 week (in seconds)
   failureIntervals = [1 * HOUR, 1 * DAY, 1 * WEEK]

   intervalData = []
   for failureInterval in failureIntervals:
      print 'Failure Interval: %d' % failureInterval
      scatterWidthData = []
      for scatterWidth in scatterWidths:
         runner = RepeatedFailures.Runner(numNodes, scatterWidth, failureInterval)
         # setup the simulated cluster
         runner.setup()
         probsOfDataLoss = []
         for interval in range(intervals):
            # cause repeated failure, and compute probability of data loss
            probOfDataLoss = runner.failureProbOfDataLoss()
            probsOfDataLoss.append((interval * failureInterval, probOfDataLoss))
            # simulate recovery of the cluster over given interval
            # before next failure
            runner.recover(failureInterval)
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
   args = parser.parse_args()

   DEBUG = args.debug

   runRepeatedFailuresExperiment(int(args.numNodes), int(args.intervals))
