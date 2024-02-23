def eraseOverlapIntervals(intervals):
    n =len(intervals)
    intervals.sort(key=lambda x: x[1]) #Sorting the intervals in terms of second element 
        
    temp = 0 # Index of the last processed interval
    cnt = 1 # Total num of non overlapping intervals # 1 because taking first interval as nonoverlapping

    for i in range(1,n): # Taking first element as non overlapping thats why iterating from 1 to n
        if intervals[i][0] >= intervals[temp][1]: # If the first element of the current element is greater than or equal to the second element of previous
            # Means the element does not overlap
            temp = i 
            cnt += 1
    return n-cnt # returning the overlapping value