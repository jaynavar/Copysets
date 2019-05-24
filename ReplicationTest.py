#!/usr/bin/env python2
import random
import timeit

# number of nodes in cluster
N = 5000
# number of chunks per node
C = 8000
# replication factor
R = 3
# total number of chunks in the system
T = N * C / R
# number of failed nodes
F = int(0.01 * N)

print "N=%d, C=%d, R=%d, T=%d, F=%d\n" % (N, C, R, T, F)

def countLoop():
   count = 0
   for _ in range(T):
      count += 1

print "Count loop"
print timeit.timeit(countLoop, number=1)
print ""

def tupleSetAdd():
   tuples = set()
   for i in range(T):
      tuples.add((i, i+1, i+2))

print "Adding tuples to set"
print timeit.timeit(tupleSetAdd, number=1)
print ""

def probOfDataLossShortcut():
   nodes = range(N)
   for _ in range(T):
      if len([n for n in random.sample(nodes, R) if n < F]) == R:
         return True
   return False

print "Prob of data loss shortcut test"
print timeit.timeit(probOfDataLossShortcut, number=1)
print ""

def randomGeneration():
   for _ in range(T):
      copyset = []
      while len(copyset) < R:
         copyset = set([random.randint(0, N) for _ in range(R)])

print "Random generation"
print timeit.timeit(randomGeneration, number=1)
print ""

def randomSampling():
   nodes = range(N)
   for _ in range(T):
      random.sample(nodes, R)

print "Random sampling"
print timeit.timeit(randomSampling, number=1)
print ""

def generateCopysets():
   copysets = set()
   nodes = range(N)
   for _ in range(T):
      copysets.add(tuple(sorted(random.sample(nodes, R))))

print "Random copyset generation"
print timeit.timeit(generateCopysets, number=1)
print ""

def generateCopysetsWithCapacities():
   copysets = set()
   capacities = {nodeId: C for nodeId in range(N)}
   for _ in range(int(0.8 * T)):
      copyset = random.sample(capacities.keys(), R)
      copysets.add(tuple(sorted(copyset)))

      # decrement node capacities
      for node in copyset:
         capacities[node] -= 1
         if capacities[node] == 0:
            del capacities[node]

print "Random copyset generation with capacities"
print timeit.timeit(generateCopysetsWithCapacities, number=1)
print ""
