# [FacebookHackerCup-2019](https://www.facebook.com/hackercup/past_rounds/) ![Language](https://img.shields.io/badge/language-Python-orange.svg) [![License](https://img.shields.io/badge/license-CC%203.0-blue.svg)](https://creativecommons.org/licenses/by-nc/3.0/) ![Progress](https://img.shields.io/badge/progress-12%20%2F%2012-ff69b4.svg)

Python solutions of Facebook Hacker Cup 2019. Solution begins with `*` means it will get TLE in the largest data set (total computation amount > `10^8`, which is not friendly for Python to solve in 5 ~ 15 seconds).

* [Qualification Round](https://github.com/kamyu104/FacebookHackerCup-2019#qualification-round)
* [Round 1](https://github.com/kamyu104/FacebookHackerCup-2019#round-1)
* [Round 2](https://github.com/kamyu104/FacebookHackerCup-2019#round-2)

## Qualification Round
| # | Title | Solution | Time | Space | Difficulty | Tag | Note |
|---| ----- | -------- | ---- | ----- | ---------- | --- | ---- |
|1| [Leapfrog: Ch. 1](https://www.facebook.com/hackercup/problem/656203948152907/)| [Python](./Qualification%20Round/leapfrog1.py)| _O(N)_ | _O(1)_ | Easy | | Math |
|2| [Leapfrog: Ch. 2](https://www.facebook.com/hackercup/problem/2426282194266338/)| [Python](./Qualification%20Round/leapfrog2.py)| _O(N)_ | _O(1)_ | Easy | | Math |
|3| [Mr. X](https://www.facebook.com/hackercup/problem/589264531559040/)| [Python](./Qualification%20Round/mr_x.py) [Python](./Qualification%20Round/mr_x2.py) | _O(E)_ | _O(D)_ | Medium | | String |
|4| [Trees as a Service](https://www.facebook.com/hackercup/problem/330920680938986/)| [Python](./Qualification%20Round/trees_as_a_service.py)| _O(N^2 * (N + M))_ | _O(N)_ | Hard | | Recursion |

## Round 1
| # | Title | Solution | Time | Space | Difficulty | Tag | Note |
|---| ----- | -------- | ---- | ----- | ---------- | --- | ---- |
|1| [Graphs as a Service](https://www.facebook.com/hackercup/problem/862237970786911/)| [Python](./Round%201/graphs_as_a_service.py)| _O(N^3)_ | _O(N^2)_ | Easy | | Floyd-Warshall Algorithm |
|2| [Class Treasurer](https://www.facebook.com/hackercup/problem/2448144345414246/)| [Python](./Round%201/class_treasurer.py)| _O(N)_ | _O(N)_ | Easy | | Greedy |
|3| [Ladders and Snakes](https://www.facebook.com/hackercup/problem/448364075989193/)| [Python](./Round%201/ladders_and_snakes.py) | _O(N^4)_ | _O(N^2)_ | Hard | | Line Sweep, Dinic's Algorithm, Max-Flow Min-Cut Theorem |
|4| [Connect the Dots](https://www.facebook.com/hackercup/problem/2390352741015547/)| [Python](./Round%201/connect_the_dots.py)| _O(NlogN)_ | _O(N)_ | Hard | | Heap, Sort |

## Round 2
| # | Title | Solution | Time | Space | Difficulty | Tag | Note |
|---| ----- | -------- | ---- | ----- | ---------- | --- | ---- |
|1| [On the Run](https://www.facebook.com/hackercup/problem/432000547357525/)| [Python](./Round%202/on_the_run.py)| _O(N^3)_ | _O(N^2)_ | Easy | | Math |
|2| [Bitstrings as a Service](https://www.facebook.com/hackercup/problem/432000547357525/)| [Python](./Round%202/bitstrings_as_a_service.py)| _O((M + N) * N)_ | _O(N^2)_ | Medium | | Union Find, DP |
|3| [Grading](https://www.facebook.com/hackercup/problem/421194065345355/)| [PyPy](./Round%202/grading.py) | _O(S * H^2)_ | _O(H)_ | Hard | | DP, Binary Search |
|4| [Seafood](https://www.facebook.com/hackercup/problem/404425766835121/)| [Python](./Round%202/seafood.py)| _O(NlogN)_ | _O(N)_ | Hard | | Mono Stack, Binary Search, DP |
