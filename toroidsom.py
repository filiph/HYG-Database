
from mvpa2.suite import SimpleSOMMapper, np, accepts_dataset_as_samples

if __debug__:
    from mvpa2.base import debug

class ToroidSOMMapper(SimpleSOMMapper):
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

        # units weight vector deltas for batch training
        # (height x width x #features)
        unit_deltas = np.zeros(self._K.shape, dtype='float')

        # a dictionary to store distance matrices for each (row, column) tuple
        distance_kernels = {}

        # for all iterations
        for it in xrange(1, self.niter + 1):
            # for all training vectors
            for s in samples:
                # determine closest unit (as element coordinate)
                b = self._get_bmu(s)

                # get or create distance kernel
                if b not in distance_kernels:
                    distance_kernels[b] = ToroidSOMMapper._get_toroid_distance_kernel(
                        self.kshape,
                        b
                    )
                dinstance_k = distance_kernels[b]

                # compute the neighborhood impact kernel for this iteration and bmu
                # has to be recomputed since kernel shrinks over time
                infl = self._compute_influence_kernel(it, dinstance_k)

                # train all units by  simply multiplying it to the difference of target
                # and all unit weights....
                unit_deltas += infl[:, :, np.newaxis] * (s - self._K)

            # apply cumulative unit deltas
            self._K += unit_deltas

            if __debug__:
                debug("SOM", "Iteration %d/%d done: ||unit_deltas||=%g" %
                      (it, self.niter, np.sqrt(np.sum(unit_deltas ** 2))))

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


if __name__ == "__main__":
    print(ToroidSOMMapper._get_toroid_distance_kernel((10, 5), (5, 0)))
