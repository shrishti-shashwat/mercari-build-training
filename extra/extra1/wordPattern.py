def wordPattern(pattern, s):
    sSpt = s.split(' ')  # Spliting the words of the string
    mapp = dict()        # Using hashing
    if len(sSpt) != len(pattern): # if len is note equal then return False
        return False
    if len(set(pattern)) != len(set(sSpt)): # set contains all unique so its len also must be equal, if not then return false
        return False
        
    for i in range(len(sSpt)):
        if sSpt[i] not in mapp: 
            mapp[sSpt[i]] = pattern[i]
        elif mapp[sSpt[i]] != pattern[i]:
            return False
    return True