# statistical_tests.py
# Contains the implementations of the statistical tests and the RQS metric.

import numpy as np
from scipy.stats import chi2, norm

# --- Helper Functions ---
def to_unit_float(x_uint32):
    """Normalizes uint32 array to floats in [0, 1)."""
    return x_uint32.astype(np.float64) / 2**32

def to_bitstream(u_float):
    """Converts floats in [0, 1) to a bitstream based on a 0.5 threshold."""
    return (u_float >= 0.5).astype(np.uint8)

# --- Metric Implementations ---
def hist_entropy(u, K=256):
    """Calculates Shannon entropy based on a histogram estimator."""
    counts, _ = np.histogram(u, bins=K, range=(0.0, 1.0))
    p = counts / counts.sum()
    p = p[p > 0]
    H = -(p * np.log2(p)).sum()
    return H, counts

def chi_square_uniformity(counts):
    """Performs a chi-square goodness-of-fit test for uniformity."""
    K = counts.size
    N = counts.sum()
    if K == 0 or N == 0:
        return 0.0, 1.0
    E = N / K
    chi_stat = ((counts - E)**2 / E).sum()
    p = 1 - chi2.cdf(chi_stat, df=K-1)
    return chi_stat, p

def autocorr_lag(u, k=1):
    """Calculates the lag-k autocorrelation and its p-value."""
    n = u.size
    if n <= k:
        return 0.0, 1.0
    u_c = u - u.mean()
    denom = (u_c * u_c).sum()
    if denom == 0:
        return 0.0, 1.0
    num = (u_c[:-k] * u_c[k:]).sum()
    rho = num / denom
    z = rho * np.sqrt(n)
    p = 2 * (1 - norm.cdf(abs(z)))
    return rho, p

def runs_test(u):
    """Performs the Wald-Wolfowitz runs test on a sequence."""
    b = (u >= 0.5).astype(np.int8)
    n = b.size
    n1 = int(b.sum())
    n0 = n - n1
    if n <= 1 or n0 == 0 or n1 == 0:
        return {'R':0, 'z':0, 'p':1.0}
    
    R = 1 + int((b[1:] != b[:-1]).sum())
    mu = (2 * n1 * n0) / n + 1
    var_num = 2 * n1 * n0 * (2 * n1 * n0 - n)
    var_den = (n**2 * (n - 1))
    
    if var_den == 0:
        return {'R': R, 'z': 0, 'p': 1.0}
        
    var = var_num / var_den
    z = (R - mu) / np.sqrt(var) if var > 0 else 0.0
    p = 2 * (1 - norm.cdf(abs(z)))
    return {'R':R, 'mu':mu, 'var':var, 'z':z, 'p':p}

def rqs_from_stats(Hnorm, pchi, p_lags, pruns):
    """Calculates the composite Randomness Quality Score (RQS)."""
    s_H = Hnorm
    s_chi = 1 - 2 * abs(pchi - 0.5)
    s_rho = np.mean([1 - 2 * abs(p - 0.5) for p in p_lags])
    s_runs = 1 - 2 * abs(pruns - 0.5)
    rqs = 0.25 * (s_H + s_chi + s_rho + s_runs)
    return {'s_H': s_H, 's_chi': s_chi, 's_rho': s_rho, 's_runs': s_runs, 'RQS': rqs}