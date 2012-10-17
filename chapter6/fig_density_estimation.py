"""
Comparison of 1D Density Estimators
-----------------------------------
"""
# Author: Jake VanderPlas <vanderplas@astro.washington.edu>
# License: BSD
#   The figure produced by this code is published in the textbook
#   "Statistics, Data Mining, and Machine Learning for Astronomy" (2013)
#   For more information, see http://astroML.github.com
import numpy as np
import pylab as pl
from scipy import stats

from astroML.density_estimation import \
    KDE, KNeighborsDensity, histogram_bayesian_blocks

#------------------------------------------------------------
# Generate our data: a mix of several Cauchy distributions
#  this is the same data used in the Bayesian Blocks figure
np.random.seed(0)
N = 10000
mu_gamma_f = [(5, 1.0, 0.1),
              (7, 0.5, 0.5),
              (9, 0.1, 0.1),
              (12, 0.5, 0.2),
              (14, 1.0, 0.1)]
true_pdf = lambda x: sum([f * stats.cauchy(mu, gamma).pdf(x)
                          for (mu, gamma, f) in mu_gamma_f])
x = np.concatenate([stats.cauchy(mu, gamma).rvs(int(f * N))
                    for (mu, gamma, f) in mu_gamma_f])
np.random.shuffle(x)
x = x[x > -10]
x = x[x < 30]

#------------------------------------------------------------
# plot the results
fig = pl.figure(figsize=(8, 8))
fig.subplots_adjust()
N_values = (500, 5000)
subplots = (211, 212)
k_values = (10, 100)

for N, k, subplot in zip(N_values, k_values, subplots):
    ax = fig.add_subplot(subplot)
    xN = x[:N]
    t = np.linspace(-10, 30, 1000)

    # Compute bins via Bayesian Blocks
    counts, bins_B = histogram_bayesian_blocks(xN)

    # Compute density with KDE
    kde = KDE('gaussian', h=0.1).fit(xN[:, None])
    dens_kde = kde.eval(t[:, None]) / N

    # Compute density with Bayesian nearest neighbors
    nbrs = KNeighborsDensity('bayesian', n_neighbors=k).fit(xN[:, None])
    dens_nbrs = nbrs.eval(t[:, None]) / N

    # plot the results
    ax.plot(t, true_pdf(t), ':', color='black', zorder=3,
            label="Generating Distribution")
    ax.plot(xN, -0.005 * np.ones(len(xN)), '|k', lw=1.5)
    ax.hist(xN, bins_B, normed=True, zorder=1,
            histtype='stepfilled', lw=1.5, color='k', alpha=0.2,
            label="Bayesian Blocks")
    ax.plot(t, dens_nbrs, '-', lw=2, color='gray', zorder=2,
            label="Nearest Neighbors (k=%i)" % k)
    ax.plot(t, dens_kde, '-', color='black', zorder=3,
            label="Kernel Density (h=0.1)")

    # label the plot
    ax.text(0.02, 0.95, "%i points" % N, ha='left', va='top',
            transform=ax.transAxes)
    ax.set_ylabel('p(x)')
    ax.legend(loc='upper right', prop=dict(size=12))

    if subplot == 212:
        ax.set_xlabel('x')

    ax.set_xlim(0, 20)
    ax.set_ylim(-0.01, 0.4001)

pl.show()
