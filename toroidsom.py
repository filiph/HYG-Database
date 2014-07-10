import numpy as np
from mvpa2.suite import SimpleSOMMapper, accepts_dataset_as_samples

if __debug__:
    from mvpa2.base import debug


class ToroidSOMMapper(SimpleSOMMapper):

    def unfold_influence_kernel(self, bmu, distances_quadrant):
        infl = np.vstack((
            np.hstack((
                # upper left
                distances_quadrant[bmu[0]:0:-1, bmu[1]:0:-1],
                # upper right
                distances_quadrant[bmu[0]:0:-1, :self.kshape[1] - bmu[1]])),
            np.hstack((
                # lower left
                distances_quadrant[:self.kshape[0] - bmu[0], bmu[1]:0:-1],
                # lower right
                distances_quadrant[:self.kshape[0] - bmu[0], :self.kshape[1] - bmu[1]]))
        ))
        # create same thing, but for "wrapped around" distance of the toroid
        # diagonal wrap
        wrapped_diagonal_infl = np.vstack((
            np.hstack((
                # upper left
                distances_quadrant[self.kshape[0] - bmu[0]:, self.kshape[1] - bmu[1]:],
                # cross top
                np.zeros((bmu[0], 1)),
                # upper right
                distances_quadrant[self.kshape[0] - bmu[0]:, :bmu[1]:-1])),
            # cross horizontal
            np.zeros((1, self.kshape[1])),
            np.hstack((
                # lower left
                distances_quadrant[self.kshape[0]:bmu[0]:-1, self.kshape[1]-bmu[1]:],
                # cross bottom
                np.zeros((self.kshape[0] - bmu[0] - 1, 1)),
                # lower right
                distances_quadrant[self.kshape[0]:bmu[0]:-1, :bmu[1]:-1]))
        ))
        np.maximum(infl, wrapped_diagonal_infl, out=infl)
        # coming from top and bottom
        top_bottom_infl = np.vstack((
            np.hstack((
                # upper left
                distances_quadrant[self.kshape[0] - bmu[0]:, bmu[1]:0:-1],
                # upper right
                distances_quadrant[self.kshape[0] - bmu[0]:, :self.kshape[1] - bmu[1]])),
            np.zeros((1, self.kshape[1])),
            np.hstack((
                # lower left
                distances_quadrant[:bmu[0]:-1, bmu[1]:0:-1],
                # lower right
                distances_quadrant[:bmu[0]:-1, :self.kshape[1] - bmu[1]]
            ))
        ))
        np.maximum(infl, top_bottom_infl, out=infl)
        # coming from left and right
        left_right_infl = np.vstack((
            np.hstack((
                # upper left
                distances_quadrant[bmu[0]:0:-1, self.kshape[1] - bmu[1]:],
                # cross top
                np.zeros((bmu[0], 1)),
                # upper right
                distances_quadrant[bmu[0]:0:-1, :bmu[1]:-1]
            )),
            np.hstack((
                # lower left
                distances_quadrant[:self.kshape[0] - bmu[0], self.kshape[1] - bmu[1]:],
                # cross bottom
                np.zeros((self.kshape[0] - bmu[0], 1)),
                # lower right
                distances_quadrant[:self.kshape[0] - bmu[0], :bmu[1]:-1]
            ))
        ))
        np.maximum(infl, left_right_infl, out=infl)
        return infl

    @accepts_dataset_as_samples
    def _train(self, samples):
        """Perform network training.

        Parameters
        ----------
        samples : array-like
            Used for unsupervised training of the SOM.

        Notes
        -----
        It is assumed that prior to calling this method the _pretrain method
        was called with the same argument.
        """

        # ensure that dqd was set properly
        dqd = self._dqd
        if dqd is None:
            raise ValueError("This should not happen - was _pretrain called?")

        # units weight vector deltas for batch training
        # (height x width x #features)
        unit_deltas = np.zeros(self._K.shape, dtype='float')

        # for all iterations
        for it in xrange(1, self.niter + 1):
            # compute the neighborhood impact kernel for this iteration
            # has to be recomputed since kernel shrinks over time
            k = self._compute_influence_kernel(it, dqd)

            # for all training vectors
            for s in samples:
                # determine closest unit (as element coordinate)
                b = self._get_bmu(s)
                # train all units at once by unfolding the kernel (from the
                # single quadrant that is precomputed), cutting it to the
                # right shape and simply multiply it to the difference of target
                # and all unit weights....
                infl = self.unfold_influence_kernel(b, k)

                unit_deltas += infl[:, :, np.newaxis] * (s - self._K)

            # apply cumulative unit deltas
            self._K += unit_deltas

            if __debug__:
                debug("SOM", "Iteration %d/%d done: ||unit_deltas||=%g  ||radius||=%g" %
                      (it, self.niter, np.sqrt(np.sum(unit_deltas ** 2)),
                      self.radius * np.exp(-1.0 * it / self.iter_scale)))

            # reset unit deltas
            unit_deltas.fill(0.)


    # Returns a matrix of distances from a given point on a 2D toroidal map to each position.
    @staticmethod
    def _get_toroid_distance_kernel(shape, from_point):
        width, height = shape
        from_x, from_y = from_point
        result = np.zeros((width, height), dtype='float')
        for y in xrange(0, height):
            for x in xrange(0, width):
                dx = min(abs(x - from_x), width - abs(x - from_x))
                dy = min(abs(y - from_y), height - abs(y - from_y))
                result[x, y] = (dx ** 2 + dy ** 2) ** 0.5
        return result

    @staticmethod
    def get_toroid_distance(x1, y1, x2, y2, width, height):
        dx = min(abs(x1 - x2), width - abs(x1 - x2))
        dy = min(abs(y1 - y2), height - abs(y1 - y2))
        return (dx ** 2 + dy ** 2) ** 0.5


if __name__ == "__main__":
    width = 60
    height = 40
    iters = 20
    mapper = ToroidSOMMapper((width, height), iters)
    distance_metric = lambda x, y: (x ** 2 + y ** 2) ** 0.5
    dqd = np.fromfunction(distance_metric,
                          mapper.kshape, dtype='float')
    k = np.exp((-1.0 * dqd))
    print(mapper.unfold_influence_kernel((5, 3), k))
