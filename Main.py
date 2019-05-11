#!/usr/bin/env python2
import argparse
import Facebook
import Hdfs
import matplotlib
import numpy as np
import Ramcloud

DEBUG = False

def runFigure6Experiment(rf=3, maxNodes=10000):
   # can't have less than replication factor number of nodes
   minNodes = rf

   # gather the data from the replication schemes
   replicationSchemes = [
      Hdfs.HdfsRandomScheme(debug=DEBUG),
      Ramcloud.RamcloudRandomScheme(debug=DEBUG),
      Facebook.FacebookRandomScheme(debug=DEBUG),
      Hdfs.HdfsCopysetScheme(debug=DEBUG),
      Ramcloud.RamcloudCopysetScheme(debug=DEBUG),
      Facebook.FacebookCopysetScheme(debug=DEBUG),
   ]
   data = {}
   for scheme in replicationSchemes:
      results = []
      for numNodes in range(minNodes, maxNodes + 1):
         results.append((numNodes, scheme.probabilityOfDataLoss(numNodes)))
      data[type(scheme).__name__] = results

   # generate the figure
   schemeNames = [(type(scheme).__name__, scheme.name())
                  for scheme in replicationSchemes]
   if DEBUG:
      generateDiagram(schemeNames, data)
   generateFigure6(schemeNames, data)

def generateDiagram(schemeNames, data, groupSize=500):
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
   for key, schemeName in schemeNames:
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

def generateFigure6(schemeNames, data):
   # TODO: generate Figure 6 plot
   # TODO: use the scheme names to generate the figure key in correct order
   pass

if __name__ == '__main__':
   parser = argparse.ArgumentParser()
   parser.add_argument('-d', '--debug', action='store_true',
                       help='enable debugging output')
   args = parser.parse_args()

   DEBUG = args.debug

   runFigure6Experiment()
