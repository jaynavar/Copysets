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

def countLoop():
   count = 0
   for _ in range(T):
      count += 1

def tupleSetAdd():
   tuples = set()
   for i in range(T):
      tuples.add((i, i+1, i+2))

def randomSampling():
   nodes = range(N)
   for _ in range(T):
      random.sample(nodes, R)

def generateCopysets():
   copysets = set()
   nodes = range(N)
   for _ in range(T):
      copysets.add(tuple(sorted(random.sample(nodes, R))))

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

print "N=%d, C=%d, R=%d, T=%d\n" % (N, C, R, T)

print "Count loop"
print timeit.timeit(countLoop, number=1)
print ""

print "Adding tuples to set"
print timeit.timeit(tupleSetAdd, number=1)
print ""

print "Random sampling"
print timeit.timeit(randomSampling, number=1)
print ""

print "Random copyset generation"
print timeit.timeit(generateCopysets, number=1)
print ""

print "Random copyset generation with capacities"
print timeit.timeit(generateCopysetsWithCapacities, number=1)
print ""
