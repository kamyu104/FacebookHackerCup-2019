# Copyright (c) 2019 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2019 Final Round - Scoreboard
# https://www.facebook.com/hackercup/problem/690405368129547/
#
# Time:  O(N^2 * M)
# Space: O(1)
#

def scoreboard():
    N, M = map(int, raw_input().strip().split())
    S = []
    for _ in xrange(N):
        S.append(raw_input().strip())
    super_count = 0
    for i in xrange(1, N):
        for j in xrange(M):
            if S[0][j] == 'Y' and S[i][j] == 'N':
                break
        else:
            super_count += 1
    if super_count > 0:
        return "Y" if super_count == 1 else "N"

    is_found = False
    for p in xrange(1, N):
        candidates = []
        for i in xrange(1, N):
            if i == p:
                continue
            for j in xrange(M):
                if S[0][j] == 'Y' and S[p][j] == 'Y' and S[i][j] == 'N':
                    break
            else:
                # participants who have all common problems solved by you and participant p
                candidates.append(i)
        for j in xrange(M):
            if S[0][j] == 'N' and S[p][j] == 'Y':
                for i in candidates:
                    if S[i][j] == 'Y':
                        break  # candidate also outscores you
                else:
                    break  # no candidate outscores you
        else:
            continue  # not found
        is_found = True
        break
    return "Y" if is_found else "N"

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, scoreboard())
