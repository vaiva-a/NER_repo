def min_flips_strategy(scores, k):
    n = len(scores)
    flips = []
    i = 0
    
    while i < n:
        if scores[i] < 0:
            if i + 1 < n and scores[i + 1] < 0:
                # Flip at i
                flips.append(i + 1)
                i += 2
            elif i + 2 < n and scores[i + 1] > 0 and scores[i + 2] < 0:
                # Flip at i and i+2
                flips.append(i + 1)
                flips.append(i + 2)
                i += 3
            else:
                return [-1]  # Not fixable
        else:
            i += 1

    if len(flips) <= k:
        return flips
    else:
        return [-1]
print(min_flips_strategy([1,-1,3,-1],5))