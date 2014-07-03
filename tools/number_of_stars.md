HYG database has close to 120,000 stars in it. But for the SOM to make sense, we need to cut of at some point, because some of those stars are far further then the rest.

For example, StarID 21006 is said to be 10,000,000 parsecs away (which is several orders of magnitude more than the most other stars in the database). But even more realistically sounding distances, like that of StarID 37481 (2,127 parsecs away), would skew the map.

For this reason, we are looking at all the stars that are less then 1,000 parsecs away from the Sun. This still gives us 108946 stars. The farthest star is StarID 117455, which is 990 parsecs away.

So, use `stars[:108947]` to get all the stars that interest us.