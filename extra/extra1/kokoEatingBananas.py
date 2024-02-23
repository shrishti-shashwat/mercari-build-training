from math import ceil

# Solving Using Binary search

class Solution:
    def findhours(self,piles,hours): # Function to calculate the total hrs needed
        totalHrs = 0
        n = len(piles)
        for i in range(n):
            totalHrs += ceil(piles[i]/hours)
        return totalHrs
    
    def minEatingSpeed(self, piles, h): # Function to calculate the speed of eating # h is the total hr
        low = 1
        high = max(piles)
        while (low<=high):
            mid = (low+(high-low)//2)
            totalHrs = self.findhours(piles,mid) # To find the total hrs by passing mid
            if totalHrs <= h:
                high = mid-1
            else:
                low = mid+1
        return low