#!/usr/bin/env python2
import argparse
import Facebook
import Hdfs
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import Ramcloud

DEBUG = False
GROUP_SIZE = 300

def runFigure6Experiment(rf=3, maxNodes=10000):
   # can't have less than replication factor number of nodes
   minNodes = rf

   # gather the data from the replication schemes
   replicationKwargs = {'debug': DEBUG, 'replicationFactor': 3}
   replicationSchemes = [
      Hdfs.HdfsRandomScheme(**replicationKwargs),
      Ramcloud.RamcloudRandomScheme(**replicationKwargs),
      Facebook.FacebookRandomScheme(**replicationKwargs),
      Hdfs.HdfsCopysetScheme(**replicationKwargs),
      Facebook.FacebookCopysetScheme(**replicationKwargs),
      Ramcloud.RamcloudCopysetScheme(**replicationKwargs),
   ]
   data = {}
   for scheme in replicationSchemes:
      results = []
      for numNodes in range(minNodes):
         # add initial (0, 0) datapoints below minimum number of nodes
         results.append((0, 0))
      for numNodes in range(minNodes, maxNodes + 1):
         results.append((numNodes, scheme.probabilityOfDataLoss(numNodes)))
      data[type(scheme).__name__] = results

   # generate the figure
   schemePlotInfos = [(type(scheme).__name__, scheme.plotInfo())
                       for scheme in replicationSchemes]

   generateDiagram(schemePlotInfos, data)
   generateFigure6(schemePlotInfos, data)

def generateDiagram(schemePlotInfos, data, groupSize=None):
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
   for key, schemePlotInfo in schemePlotInfos:
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

def generateFigure6(schemePlotInfos, data):
   # set dimensions and title
   fig = plt.figure(figsize=(8, 5))
   fig.suptitle('Probability of data loss when 1% of the nodes fail concurrently')

   # add data
   for key, schemePlotInfo in schemePlotInfos:
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
   plt.savefig('Figure6.png')

if __name__ == '__main__':
   parser = argparse.ArgumentParser()
   parser.add_argument('-d', '--debug', action='store_true',
                       help='enable debugging output')
   parser.add_argument('-g', '--groupSize', default='500',
                       help='size of debug summary groups')
   args = parser.parse_args()

   DEBUG = args.debug
   GROUP_SIZE = int(args.groupSize)

   runFigure6Experiment()
