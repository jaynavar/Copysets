#!/usr/bin/env python2
import atexit
from datetime import datetime, timedelta
import json
import os
import shutil
import time

class ExperimentTrack(object):
   def __init__(self, dataBaseDir, trialInfo, save):
      timestamp = datetime.today().strftime('%Y_%m_%d_%H_%M_%S')
      self.dataDir = os.path.join(dataBaseDir, timestamp)
      self.save = save
      self.starttime = int(time.time())

      if self.save and not os.path.exists(self.dataDir):
         print "Saving experiment data in: %s\n" % self.dataDir

         # create directory
         os.makedirs(self.dataDir)

         # save trial info
         with open(os.path.join(self.dataDir, 'TRIAL_INFO.txt'), 'w') as f:
            f.write('\n'.join(trialInfo) + '\n')

         self.cleanExit = False

         def exitFunc():
            # cleanup directory on failure exit
            if not self.cleanExit:
               shutil.rmtree(self.dataDir)
               return

            # add runtime to the trial info
            runtime = int(time.time()) - self.starttime
            t = timedelta(seconds=runtime)
            d = datetime(1,1,1) + t
            timeString = ("%02d:%02d:%02d:%02d" %
                          (d.day-1, d.hour, d.minute, d.second))
            with open(os.path.join(self.dataDir, 'TRIAL_INFO.txt'), 'a') as f:
               f.write('\nRuntime (DD:HH:MM:SS): %s\n' % timeString)

         atexit.register(exitFunc)

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
