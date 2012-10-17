"""
Log-likelihood for Cauchy Distribution
--------------------------------------

This plot shows the Likelihood as a function of the mean :math:`\mu` and the
error :math:`\gamma` when the posterior is assumed to be a Cauchy distribution.
"""
# Author: Jake VanderPlas <vanderplas@astro.washington.edu>
# License: BSD
#   The figure produced by this code is published in the textbook
#   "Statistics, Data Mining, and Machine Learning for Astronomy" (2013)
#   For more information, see http://astroML.github.com
import numpy as np
import pylab as pl
from scipy.stats import cauchy
from astroML.plotting.likelihood import convert_to_stdev
from astroML.stats import median_sigmaG


def cauchy_logL(xi, gamma, mu):
    """Equation 5.74: cauchy likelihood"""
    xi = np.asarray(xi)
    n = xi.size
    shape = np.broadcast(gamma, mu).shape

    xi = xi.reshape(xi.shape + tuple([1 for s in shape]))

    return ((n - 1) * np.log(gamma)
            - np.sum(np.log(gamma ** 2 + (xi - mu) ** 2), 0))


#------------------------------------------------------------
# Define the grid and compute logL
gamma = np.linspace(0.1, 5, 70)
mu = np.linspace(-5, 5, 70)

np.random.seed(44)
mu0 = 0
gamma0 = 2
xi = cauchy(mu0, gamma0).rvs(10)

logL = cauchy_logL(xi, gamma[:, np.newaxis], mu)
logL -= logL.max()

#------------------------------------------------------------
# Find the max and print some information
i, j = np.where(logL >= np.max(logL))

print "mu from likelihood:", mu[j]
print "gamma from likelihood:", gamma[i]
print

med, sigG = median_sigmaG(xi)
print "mu from median", med
print "gamma from quartiles:", sigG / 1.483  # Equation 3.54

#------------------------------------------------------------
# Plot the results
pl.imshow(logL, origin='lower', cmap=pl.cm.binary,
          extent=(mu[0], mu[-1], gamma[0], gamma[-1]),
          aspect='auto')
pl.colorbar()
pl.clim(-5, 0)

pl.contour(mu, gamma, convert_to_stdev(logL),
           levels=(0.683, 0.955, 0.997),
           colors='k', linewidths=2)

pl.text(0.5, 0.9,
        r'$L(\mu,\gamma)\ \mathrm{for\ \bar{x}=0,\ \gamma=2,\ n=10}$',
        fontsize=18, bbox=dict(ec='k', fc='w', alpha=0.9),
        ha='center', va='center', transform=pl.gca().transAxes)

pl.xlabel(r'$\mu$')
pl.ylabel(r'$\gamma$')

pl.show()
