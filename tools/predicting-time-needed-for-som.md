# Trying to predict the time it will take to organize all stars into a SOM.

organize(stars[:10], width=100, height=100, iters=100)  # 0.873s
organize(stars[:10], width=1000, height=1000, iters=100)  # 136.889s
organize(stars[:100], width=100, height=100, iters=100)  # 8.601s
organize(stars[:1000], width=100, height=100, iters=100)  # 83.864s
organize(stars[:1000], width=100, height=100, iters=10)  # 8.547s
organize(stars[:1000], width=200, height=100, iters=10)  # 16.839s

Looks like time increases lineary with number of stars.
It definitely increases lineary with number of iters.
It also increases lineary with number of nodes in the Kohounen layer.

P = O(nstars, niters, width, height)
- or -
P = O(nstars, niters, size^2)


Now, let's try the full star set:

len(stars) == 119617
organize(stars, width=100, height=100, iters=10)  # 1090.213s

8.547s for 1000 stars, 1090.213s for 119617 = yes, linear

Prediction:
1090s (experimentally found to be the execution time for organize(stars, width=100, height=100, iters=10))
*10 (width:  100 -> 1000)
*10 (height: 100 -> 1000)
*100(iters:  10  -> 1000)
=
10900000s
=
126 days
= 
4+ months


## Compromise

