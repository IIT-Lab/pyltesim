#!/usr/bin/env python

''' Performs the Kivanc RCG algorithm on the input map.

This function performs the algorithm described in Kivanc 2003,
Computationally efficient bandwidth allocation and power control for
ofdma called Rate Craving Greedy.
It allocates subcarriers between users via a nearest neighbor search if
the final number of subcarriers per user is previously known.
Input: 
       - costmap: A matrix of dimension (subcarriers, users) where the
       entry represents the cost value that is used to allocate
       subcarriers (higher is better)
       - targetUserAssignment: A vector of dimension (users, 1) that holds the
       number of subcarriers that each user should receive.
       sum(subcarrierCount) must equal the number of subcarriers.
Output: 
       - outMap: size = [N]. Each entry contains the user index to whom the resource is assigned.
       - initialMap: The allocation after the first step (for debugging) 

File: rcg.py
'''

__author__ = "Hauke Holtkamp"
__credits__ = "Hauke Holtkamp"
__license__ = "unknown"
__version__ = "unknown"
__maintainer__ = "Hauke Holtkamp"
__email__ = "h.holtkamp@gmail.com" 
__status__ = "Development" 

from numpy import *

def rcg(costmp, targetUserAssignment):
    """Rate craving greedy subcarrier allocation"""
    
    users = costmp.shape[1]
    subcarriers = costmp.shape[0]
    costmap = float32(real(costmp))

    # check input
    if len(targetUserAssignment) is not users:
        raise ValueError('rcg input mismatch')

    currentSubcarrierAssignment = empty([subcarriers]); currentSubcarrierAssignment[:] = nan
    currentUserAssignment = zeros([users]); #currentUserAssignment[:] = nan

    # an NaN array signifies a sleep mode slot
    if sum(isnan(targetUserAssignment)) == users:
        outMap = empty([subcarriers])
        outMap[:] = nan
        initialMap = nan
        return outMap, initialMap

    # initial subcarrier assignment by strength regardless of count
    for sc in range(subcarriers):
        maxindex = argmax(costmap[sc,:])
        currentSubcarrierAssignment[sc] = maxindex # save which user has the best value
        currentUserAssignment[maxindex] = currentUserAssignment[maxindex] + 1
        
    initialMap = currentUserAssignment.copy()
#    print initialMap

    # perform the RCG reassignment. Take from the overloaded and give to the dissatisfied.
    overloadedUsers = (targetUserAssignment-currentUserAssignment<0) # boolean array
    satisfiedUsers = (targetUserAssignment-currentUserAssignment<=0) # boolean array

    for olusrindex in arange(users):
        while overloadedUsers[olusrindex]:

            # find nearest neighbor
            subcarrierIndicesOfOlusr = (currentSubcarrierAssignment == olusrindex)
            subcarrierIndicesOfOtherUsers = (currentSubcarrierAssignment != olusrindex)
            
            diffmp = abs(diffmap(costmap.copy(), olusrindex)) # generate map of differences
            
            diffmp[:,where(satisfiedUsers==True)] = nan # clear out the satisfieds. We do not compare to them.
            minindx = nanargmin(diffmp[:,where(satisfiedUsers==False)],0) # subcarrier indices of useful values
            diffmp[subcarrierIndicesOfOtherUsers,:] = nan # clear out rest

            # trade subcarrier with nearest neighbor (nn)
            nnindex = unravel_index(nanargmin(diffmp), diffmp.shape)
            tradesc = nnindex[0]
            tousr   = nnindex[1]
            
            # trade the nearest neighbor
            currentSubcarrierAssignment[tradesc] = tousr
            currentUserAssignment[tousr] = currentUserAssignment[tousr] + 1
            currentUserAssignment[olusrindex] = currentUserAssignment[olusrindex] - 1
#            print targetUserAssignment
#            print currentUserAssignment

            # keep track
            overloadedUsers = (targetUserAssignment-currentUserAssignment<0) # boolean array
            satisfiedUsers = (targetUserAssignment-currentUserAssignment<=0) # boolean array

    outMap = currentSubcarrierAssignment
    return outMap, initialMap 

def diffmap(costmap, userindex):
    """For a reference user, this function returns the differences rather than absolute values."""
    uservalues = costmap[:,userindex].copy()
    uservalues.shape = (uservalues.size,1) # promote dimensions
    costmap[:,userindex] = nan # don't compare to self
    
    diffmap = -uservalues + costmap
    return diffmap

if __name__ == '__main__':
    users = 4
    subcarriers = 5
    costmap = random.random([subcarriers, users])
    subcarrierCount = array([1,2,2,0], dtype=float_)
#    subcarrierCount[:] = nan
    print rcg(costmap, subcarrierCount)

