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
RENDER_LOCAL = False

RANDOM_REPLICATION_SCHEMES = [
   Hdfs.HdfsRandomScheme,
   Ramcloud.RamcloudRandomScheme,
   Facebook.FacebookRandomScheme,
]
COPYSET_REPLICATION_SCHEMES = [
   Hdfs.HdfsCopysetScheme,
   Facebook.FacebookCopysetScheme,
   Ramcloud.RamcloudCopysetScheme,
]
ALL_REPLICATION_SCHEMES = RANDOM_REPLICATION_SCHEMES + COPYSET_REPLICATION_SCHEMES
SCHEME_PLOT_INFOS = [(scheme.__name__, scheme.plotInfo())
                     for scheme in ALL_REPLICATION_SCHEMES]

def runFigure6Experiment(rf=3, maxNodes=10000, simulation=False, trials=100,
                         sampleGap=1):
   # can't have less than replication factor number of nodes
   minNodes = rf

   # gather the data from the replication schemes
   replicationKwargs = {'debug': DEBUG, 'simulation': simulation,
                        'trials': trials, 'replicationFactor': 3}
   # currently only support copyset replication for simulations
   validReplicationSchemes = (ALL_REPLICATION_SCHEMES if not simulation else
                              COPYSET_REPLICATION_SCHEMES)
   replicationSchemes = [scheme(**replicationKwargs)
                         for scheme in validReplicationSchemes]
   data = {}
   for scheme in replicationSchemes:
      print 'Collecting data for: %s\n' % type(scheme).__name__
      results = []
      for numNodes in range(0, maxNodes + 1, sampleGap):
         if numNodes < minNodes:
            # add initial (0, 0) datapoints below minimum number of nodes
            results.append((0, 0))
         else:
            results.append((numNodes, scheme.probabilityOfDataLoss(numNodes)))
      data[type(scheme).__name__] = results
   return data

def generateDiagram(data, groupSize=500):
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
      if key not in data:
         continue
      schemeName = schemePlotInfo.label
      print 'Scheme: %s' % schemeName
      dataPoints = []
      minNumNodes = None
      for numNodes, prob in data[key]:
         if minNumNodes == None:
            minNumNodes = numNodes
         if numNodes - minNumNodes >= groupSize:
            outputDataPoints(dataPoints)
            # reset state
            dataPoints = []
            minNumNodes = numNodes
         dataPoints.append((numNodes, prob))
      if dataPoints:
         outputDataPoints(dataPoints)
      print ''

def generateFigure6(data, et, simulation=False, sampleGap=1):
   # set dimensions and title
   fig = plt.figure(figsize=(8, 5))
   fig.suptitle('Probability of data loss when 1% of the nodes fail concurrently')

   # add data
   for key, schemePlotInfo in SCHEME_PLOT_INFOS:
      if key not in data:
         continue
      spi = schemePlotInfo
      x, y = zip(*data[key])
      # mark every 1,000 ticks, regardless of sample gap
      markevery = int(1000 / sampleGap)
      plt.plot(x, y, label=spi.label, linestyle=spi.linestyle,
               linewidth=spi.linewidth, marker=spi.marker,
               markevery=markevery, markersize=spi.markersize,
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
   parser.add_argument('--note', default='N/A',
                       help='add comment to trial info')
   parser.add_argument('-g', '--group-size', default='500',
                       help='size of debug summary groups')
   parser.add_argument('--sample-gap', default='1',
                       help='gap between sampled datapoints')
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

   trialInfo = [
      'Trial Note: %s' % args.note,
      '',
      'Trials: %s' % args.trials,
      'Simulation: %r' % args.simulation,
      'Sample gap: %s' % args.sample_gap,
   ]
   et = ExperimentTrack('data_Figure6', trialInfo, args.save)

   if args.load:
      data = et.loadData(args.load)
   else:
      data = runFigure6Experiment(simulation=args.simulation,
                                  trials=int(args.trials),
                                  sampleGap=int(args.sample_gap))

   generateDiagram(data, groupSize=int(args.group_size))
   et.dumpData(data)

   if not args.no_figures:
      generateFigure6(data, et, simulation=args.simulation,
                      sampleGap=int(args.sample_gap))

   et.setCleanExit()
