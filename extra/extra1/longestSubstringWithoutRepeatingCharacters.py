def lengthOfLongestSubstring(s):
    max_length = 0
    seen = set() # Using set function to store only unique value
    left = 0

    for i in range(len(s)):
        if s[i] not in seen:
            seen.add(s[i]) # If not in set then add to set
            max_length = max(max_length, i - left+1)
        else:
            while s[i] in seen:
                seen.remove(s[left]) # If in set then remove and move the left pointer one place ahead
                left +=1
            seen.add(s[i])
    return max_length