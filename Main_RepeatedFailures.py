#!/usr/bin/env python2
RENDER_LOCAL = False
import argparse
import copy
import datetime
import json
import matplotlib
if not RENDER_LOCAL:
   matplotlib.use('Agg')
from matplotlib.dates import DateFormatter
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
   failureIntervals = [1 * MINUTE, 25 * MINUTE, 50 * MINUTE]
   replicationFactor = 3
   # set node parameters (1 Gb/s, 100 GB per node), in Mb's, assuming
   # each peer can only dedicate 10% of capacity to node recovery
   nodeBandwidth = 1000
   nodeCapacity = 8 * 100000
   recoveryUtil = 0.05

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

   return intervalData

def outputFigures(intervalData):
   for suffix in ['iso', 'comp']:
      for failureInterval, scatterWidthData in intervalData:
         failureIntervalMinutes = int(failureInterval / 60)
         # TODO update title to include correct interval
         fig = plt.figure()
         fig.suptitle('Probability of data loss when 1%% of '
                      'the nodes fail every %d minutes' % failureIntervalMinutes )

         # add data
         for scatterWidth, probsOfDataLoss in scatterWidthData:
            x, y = zip(*probsOfDataLoss)
            y = [iso if suffix == 'iso' else comp for (iso, comp) in y]
            date = datetime.datetime(2019, 1, 1, 0, 0)
            x = [date + datetime.timedelta(seconds=v) for v in x]
            plt.plot(x, y, label='S=%d' % scatterWidth, linestyle='--',
                     marker='o', markersize=8, markeredgewidth=0.0,
                     clip_on=False)

         # add legend
         plt.legend(numpoints=1, handlelength=0.5, borderaxespad=1.0)

         # set x-axis
         plt.xlabel('Time')
         ax = plt.gca()
         ax.xaxis.set_major_formatter(DateFormatter("%H:%M"))
         plt.gcf().autofmt_xdate()

         # set y-axis
         plt.ylabel('Probability of data loss')
         yticksRange = np.arange(0.0, 1.0 + 0.1, 0.2)
         plt.yticks(yticksRange)
         ax.set_yticklabels(['{:,.0%}'.format(tick) for tick in yticksRange])

         if RENDER_LOCAL:
            plt.show()
         else:
            plt.savefig('figures/Figure_RepFails_Intv_%03d_mins_%s.png' %
                        (failureIntervalMinutes, suffix))

if __name__ == '__main__':
   parser = argparse.ArgumentParser()
   parser.add_argument('-d', '--debug', action='store_true',
                       help='enable debugging output')
   parser.add_argument('-n', '--numNodes', default='5000',
                       help='number of nodes in cluster')
   parser.add_argument('-i', '--intervals', default='10',
                       help='number of repeated failures to graph')
   parser.add_argument('-t', '--trials', default='100',
                       help='number of trials for each datapoint')
   parser.add_argument('-s', '--save',
                       help='location to save data to')
   parser.add_argument('-l', '--load',
                       help='location to load data from')
   parser.add_argument('--no-figures', action='store_true',
                       help='do not generate figures')
   args = parser.parse_args()

   DEBUG = args.debug

   if args.load:
      with open(args.load) as infile:
         intervalData = json.load(infile)
   else:
      intervalData = runRepeatedFailuresExperiment(
         int(args.numNodes), int(args.intervals), int(args.trials))

   if args.save:
      with open(args.save, 'w') as outfile:
         json.dump(intervalData, outfile, indent=2)

   if not args.no_figures:
      outputFigures(intervalData)
