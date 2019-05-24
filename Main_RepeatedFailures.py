#!/usr/bin/env python2
import argparse
import copy
from ExperimentTrack import ExperimentTrack
import datetime
import matplotlib
from matplotlib.dates import DateFormatter
import numpy as np
import os
import RepeatedFailures

DEBUG = False

# Time units, in seconds
MINUTE = 60
HOUR = 60 * MINUTE
DAY = 24 * HOUR
WEEK = 7 * DAY

# cluster parameters
SCATTER_WIDTHS = [10, 20, 100, 200]
FAILURE_INTERVALS = [1 * MINUTE, 25 * MINUTE, 50 * MINUTE]
REPLICATION_FACTOR = 3
# set node parameters (10 Gb/s, 1 TB per node), in Mb's, assuming
# each peer can only dedicate 10% of capacity to node recovery
NODE_BANDWIDTH = 10000
NODE_CAPACITY = 8 * 1000000
RECOVERY_UTIL = 0.05

def runRepeatedFailuresExperiment(numNodes, numIntervals, numTrials):
   intervalData = []
   for failureInterval in FAILURE_INTERVALS:
      print 'Failure Interval: %d' % failureInterval
      scatterWidthData = []
      for scatterWidth in SCATTER_WIDTHS:
         runner = RepeatedFailures.Runner(
            numNodes, scatterWidth, failureInterval, numIntervals, numTrials,
            REPLICATION_FACTOR, NODE_BANDWIDTH, NODE_CAPACITY, RECOVERY_UTIL)
         probsOfDataLoss = runner.run()
         print 'Scatter Width: %d, Probs of Data Loss:\n%s' % (scatterWidth,
                                                               probsOfDataLoss)
         scatterWidthData.append((scatterWidth, probsOfDataLoss))
      print ''
      intervalData.append((failureInterval, scatterWidthData))

   return intervalData

def outputFigures(intervalData, et):
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
            if et.save:
               filename = ('Figure_RepFails_Intv_%03d_mins_%s.png' %
                           (failureIntervalMinutes, suffix))
               plt.savefig(os.path.join(et.getDirName(), filename))

if __name__ == '__main__':
   parser = argparse.ArgumentParser()
   parser.add_argument('-d', '--debug', action='store_true',
                       help='enable debugging output')
   parser.add_argument('-s', '--save', action='store_true',
                       help='location to save data to')
   parser.add_argument('-l', '--load',
                       help='location to load data from')
   parser.add_argument('--note', default='N/A',
                       help='add comment to trial info')
   parser.add_argument('-n', '--numNodes', default='5000',
                       help='number of nodes in cluster')
   parser.add_argument('-i', '--intervals', default='10',
                       help='number of repeated failures to graph')
   parser.add_argument('-t', '--trials', default='100',
                       help='number of trials for each datapoint')
   parser.add_argument('--no-figures', action='store_true',
                       help='do not generate figures')
   parser.add_argument('-r', '--render-local', action='store_true',
                       help='render figure locally using X11')
   args = parser.parse_args()

   RENDER_LOCAL = args.render_local
   if not RENDER_LOCAL:
      matplotlib.use('Agg')
   import matplotlib.pyplot as plt

   DEBUG = args.debug

   trialInfo = [
      'Trial Note: %s' % args.note,
      '',
      'Nodes: %s' % args.numNodes,
      'Intervals: %s' % args.intervals,
      'Trials: %s' % args.trials,
      'Scatter widths: %s' % SCATTER_WIDTHS,
      'Failure intervals: %s' % FAILURE_INTERVALS,
      'Replication factor: %d' % REPLICATION_FACTOR,
      'Node bandwidth (Mb/s): %d' % NODE_BANDWIDTH,
      'Node capacity (GB): %d' % (NODE_CAPACITY / (8 * 1000)),
      'Recovery utilization rate: %f' % RECOVERY_UTIL,
   ]
   et = ExperimentTrack('data_RepeatedFailures', trialInfo, args.save)

   if args.load:
      intervalData = et.loadData(args.load)
   else:
      intervalData = runRepeatedFailuresExperiment(
         int(args.numNodes), int(args.intervals), int(args.trials))

   et.dumpData(intervalData)

   if not args.no_figures:
      outputFigures(intervalData, et)

   et.setCleanExit()
