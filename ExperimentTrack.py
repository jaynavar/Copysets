#!/usr/bin/env python2
import atexit
from datetime import datetime
import os
import json
import shutil

class ExperimentTrack(object):
   def __init__(self, dataBaseDir, trialInfo, save):
      timestamp = datetime.today().strftime('%Y_%m_%d_%H_%M_%S')
      self.dataDir = os.path.join(dataBaseDir, timestamp)
      self.save = save

      if self.save and not os.path.exists(self.dataDir):
         print "Saving experiment data in: %s" % self.dataDir

         # create directory
         os.makedirs(self.dataDir)

         # save trial info
         with open(os.path.join(self.dataDir, 'TRIAL_INFO.txt'), 'w') as f:
            f.write('\n'.join(trialInfo) + '\n')

         # cleanup directory on failure exit
         self.cleanExit = False
         def cleanup():
            if not self.cleanExit:
               shutil.rmtree(self.dataDir)
         atexit.register(cleanup)

   def getDirName(self):
      return self.dataDir

   def setCleanExit(self):
      self.cleanExit = True

   def dumpData(self, data):
      if not self.save:
         return
      with open(os.path.join(self.dataDir, 'DATA.json'), 'w') as f:
         json.dump(data, f, indent=2)

   @staticmethod
   def loadData(filePath):
      with open(filePath) as f:
         return json.load(f)
