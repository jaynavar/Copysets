#!/usr/bin/env python2
import argparse
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import RepeatedFailures

DEBUG = False

# Time units, in seconds
MINUTE = 60
HOUR = 60 * MINUTE
DAY = 24 * HOUR
WEEK = 7 * DAY

def runRepeatedFailuresExperiment(numNodes, numIntervals, numTrials):
   scatterWidths = [10, 200]
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

   outputFigures(intervalData)

def outputFigures(intervalData):
   for failureInterval, scatterWidthData in intervalData:
      # TODO update title to include correct interval
      fig = plt.figure()
      fig.suptitle('Probability of data loss when 1%% of '
                   'the nodes fail every %d' % failureInterval)

      # add data
      for scatterWidth, probsOfDataLoss in scatterWidthData:
         x, y = zip(*probsOfDataLoss)
         plt.plot(x, y, label='S=%d' % scatterWidth, linestyle='--',
                  marker='o', markersize=8, markeredgewidth=0.0,
                  clip_on=False)

      # add legend
      plt.legend(numpoints=1, handlelength=0.5, borderaxespad=1.0)

      # set x-axis
      plt.xlabel('Time')

      # set y-axis
      plt.ylabel('Probability of data loss')
      yticksRange = np.arange(0.0, 1.0 + 0.1, 0.2)
      plt.yticks(yticksRange)
      ax = plt.gca()
      ax.set_yticklabels(['{:,.0%}'.format(tick) for tick in yticksRange])

      # TODO remove below
      plt.show()

      # save figure
      # if simulation:
      #    plt.savefig('Figure6_simulation.png')
      # else:
      #    plt.savefig('Figure6_computation.png')

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
