class ReplicationScheme(object):
   def __init__(self, debug=False):
      self.debug = debug

   def probabilityOfDataLoss(self, numNodes):
      raise NotImplementedError

   def name(self):
      raise NotImplementedError
