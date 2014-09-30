import cmath


def omega(p, q):
    """
    """
    return cmath.exp((2.0 * cmath.pi * 1j * q) / p)


def fft(signal):
    """
    pulled from: http://jeremykun.com/2012/07/18/the-fast-fourier-transform/
    """
    n = len(signal)
    if n == 1:
        return signal
    else:
        Feven = fft([signal[i] for i in xrange(0, n, 2)])
        Fodd = fft([signal[i] for i in xrange(1, n, 2)])

        combined = [0] * n
        for m in xrange(n/2):
            combined[m] = Feven[m] + omega(n, -m) * Fodd[m]
            combined[m + n/2] = Feven[m] - omega(n, -m) * Fodd[m]

        return combined
