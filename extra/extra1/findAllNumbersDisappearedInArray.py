# Time Complexity O(N^2) Space Complexity O(N)
def findDisappearedNumbers( nums):
    n = len(nums)
    ans = []
    for i in range(1,n+1):
        for num in nums:
            if i == num:
                break
        if i != num:
            ans.append(i)
    return ans


# Time Complexity O(N) Space Complexity O(N)
def findDisappearedNumbers( nums):
    sett = set(nums)
    ans = []

    for i in range(1,len(nums)+1):
        if i not in sett:
            ans.append(i)
    return ans

# Time Complexity O(N) Space Complexity O(1)
def findDisappearedNumbers( nums):
    result = []
    for num in nums:
        nums[abs(num)-1] = -abs(nums[abs(num)-1])
    for i in range(len(nums)):
        if nums[i] > 0:
            result.append(i+1)
    return result