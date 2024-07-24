def LCS(str1: str, str2: str) :
    len1 = len(str1)
    len2 = len(str2)

    dp = [0]*min(len1, len2)

    if (str1[0] == str2[0]) :
        dp[0] = 1

    for i in range(1, min(len1, len2)):
        if (str1[i] == str2[i]):
            dp[i] = 1 + dp[i-1]
    
    return max(dp)

print(LCS('12345', '13245'))
