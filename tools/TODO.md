- "better" SOM algorithm
    - use toroidal map instead of 2D square
        - in other words, it's a Civ map or Snake map (going through any wall goes to the other
          side)
        - this means stars won't get crammed to sides but we can still use 2D
        - the only thing we need to do is provide distance_metric
            - `dx = min ( abs(x2 - x1) , size - abs(x2 - x1) )`
                from http://stackoverflow.com/a/23580331/1416886
        - putting Sol in the center is easy (just "scroll" the viewport)
    - use true hex coords
        - http://3dmdesign.com/development/hexmap-coordinates-the-easy-way
        - http://www.redblobgames.com/grids/hexagons/
    - use circular map instead of square
        - create custom SOMMapper, which:
            - maps the kshape into another array (not 2D - probably 1d hex spiral)
            - overrides the distance_metric to compute spatial relationship on the new kshape
              (instead of `lambda x, y: (x ** 2 + y ** 2) ** 0.5`)
                - use https://github.com/pfrolov/hexagonal-spiral
            - Actually, we don't need a custom SOMMapper, we can use SimpleSOMMapper and put
              onedimensional kshape and the custom distance_metric.
    - try to put Sol in the center
        - maybe do the initial kohonen layer by putting all stars into a spiral around the Sun?
          (instead of completely random)
    - accentuates spatial relationship between stars with proper names (Proxima Centauri should be
      very close to Sol, no matter what)