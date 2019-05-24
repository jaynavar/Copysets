#!/usr/bin/env python2
import argparse
import Facebook
from ExperimentTrack import ExperimentTrack
import Hdfs
import matplotlib
import numpy as np
import os
import Ramcloud

DEBUG = False
GROUP_SIZE = 300
RENDER_LOCAL = False

REPLICATION_SCHEMES = [
   Hdfs.HdfsRandomScheme,
   Ramcloud.RamcloudRandomScheme,
   Facebook.FacebookRandomScheme,
   Hdfs.HdfsCopysetScheme,
   Facebook.FacebookCopysetScheme,
   Ramcloud.RamcloudCopysetScheme,
]
SCHEME_PLOT_INFOS = [(scheme.__name__, scheme.plotInfo())
                     for scheme in REPLICATION_SCHEMES]

def runFigure6Experiment(rf=3, maxNodes=10000, simulation=False, trials=100):
   # can't have less than replication factor number of nodes
   minNodes = rf

   # gather the data from the replication schemes
   replicationKwargs = {'debug': DEBUG, 'simulation': simulation,
                        'trials': trials, 'replicationFactor': 3}
   replicationSchemes = [scheme(**replicationKwargs)
                         for scheme in REPLICATION_SCHEMES]
   data = {}
   for scheme in replicationSchemes:
      results = []
      for numNodes in range(minNodes):
         # add initial (0, 0) datapoints below minimum number of nodes
         results.append((0, 0))
      for numNodes in range(minNodes, maxNodes + 1):
         results.append((numNodes, scheme.probabilityOfDataLoss(numNodes)))
      data[type(scheme).__name__] = results
   generateDiagram(data)
   return data

def generateDiagram(data, groupSize=None):
   if groupSize is None:
      groupSize = GROUP_SIZE
   def outputDataPoints(dataPoints):
      # output stats for the group
      firstN = dataPoints[0][0]
      lastN = dataPoints[-1][0]
      npDataPoints = np.array([dp[1] for dp in dataPoints])
      avg = npDataPoints.mean()
      std = npDataPoints.std()
      print ('N=(%d,%d), AVG_PR=%0.3f, STD_PR=%0.3f' %
             (firstN, lastN, avg, std))

   # print average probabilities for groups of data points
   for key, schemePlotInfo in SCHEME_PLOT_INFOS:
      schemeName = schemePlotInfo.label
      print 'Scheme: %s' % schemeName
      dataPoints = []
      for numNodes, prob in data[key]:
         dataPoints.append((numNodes, prob))
         if len(dataPoints) == groupSize:
            outputDataPoints(dataPoints)
            # reset state
            dataPoints = []
      if dataPoints:
         outputDataPoints(dataPoints)
      print ''

def generateFigure6(data, et, simulation=False):
   # set dimensions and title
   fig = plt.figure(figsize=(8, 5))
   fig.suptitle('Probability of data loss when 1% of the nodes fail concurrently')

   # add data
   for key, schemePlotInfo in SCHEME_PLOT_INFOS:
      spi = schemePlotInfo
      x, y = zip(*data[key])
      plt.plot(x, y, label=spi.label, linestyle=spi.linestyle,
               linewidth=spi.linewidth, marker=spi.marker,
               markevery=spi.markevery, markersize=spi.markersize,
               markeredgewidth=spi.markeredgewidth,
               color=spi.color, clip_on=spi.clip_on)

   # add legend
   plt.legend(numpoints=1, handlelength=0.5, borderaxespad=1.0)

   # set x-axis
   plt.xlabel('Number of nodes')

   # set y-axis
   plt.ylabel('Probability of data loss')
   yticksRange = np.arange(0.0, 1.0 + 0.1, 0.2)
   plt.yticks(yticksRange)
   ax = plt.gca()
   ax.set_yticklabels(['{:,.0%}'.format(tick) for tick in yticksRange])

   # save figure
   if RENDER_LOCAL:
      plt.show()
   else:
      if et.save:
         if simulation:
            filename = 'Figure6_simulation.png'
         else:
            filename = 'Figure6_computation.png'
         plt.savefig(os.path.join(et.getDirName(), filename))

if __name__ == '__main__':
   parser = argparse.ArgumentParser()
   parser.add_argument('-d', '--debug', action='store_true',
                       help='enable debugging output')
   parser.add_argument('-s', '--save', action='store_true',
                       help='location to save data to')
   parser.add_argument('-l', '--load',
                       help='location to load data from')
   parser.add_argument('-g', '--groupSize', default='500',
                       help='size of debug summary groups')
   parser.add_argument('--simulation', action='store_true',
                       help='use simulation instead of computation')
   parser.add_argument('-t', '--trials', default='100',
                       help='number of simulation trials to run per datapoint')
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
   GROUP_SIZE = int(args.groupSize)

   trialInfo = [
      'Trials: %s' % args.trials,
      'Simulation: %r' % args.simulation,
   ]
   et = ExperimentTrack('data_Figure6', trialInfo, args.save)

   if args.load:
      data = et.loadData(args.load)
   else:
      data = runFigure6Experiment(simulation=args.simulation,
                                  trials=int(args.trials))

   et.dumpData(data)

   if not args.no_figures:
      generateFigure6(data, et, simulation=args.simulation)

   et.setCleanExit()
