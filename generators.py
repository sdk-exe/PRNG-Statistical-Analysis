# generators.py
# Contains the Python implementations of all seven PRNGs used in the study.

import os
import struct
import hashlib
import numpy as np

# --- 1. Classic LCG (32-bit) ---
def lcg32(n, seed, a=1664525, c=1013904223, m=2**32, burn_in=1000):
    """Generates a sequence using a Linear Congruential Generator."""
    x = seed & 0xFFFFFFFF
    out = np.empty(n + burn_in, dtype=np.uint32)
    for i in range(n + burn_in):
        x = (a * x + c) % m
        out[i] = x
    return out[burn_in:]

# --- 2. XOR-Shift (Marsaglia-style) ---
def xorshift32(n, seed, burn_in=1000):
    """Generates a sequence using a 32-bit XOR-Shift algorithm."""
    x = seed & 0xFFFFFFFF
    out = np.empty(n + burn_in, dtype=np.uint32)
    for i in range(n + burn_in):
        x ^= (x << 13) & 0xFFFFFFFF
        x ^= (x >> 17)
        x ^= (x << 5) & 0xFFFFFFFF
        out[i] = x & 0xFFFFFFFF
    return out[burn_in:]

# --- 3. Hybrid: LCG XOR-rot(xorshift) ---
def hybrid32(n, seed, burn_in=1000):
    """
    Generates a sequence using a custom hybrid of LCG and XOR-Shift.
    Note: Uses the same seed for both for simplicity in the harness.
    """
    l = lcg32(n + burn_in, seed, burn_in=0)
    x = xorshift32(n + burn_in, seed, burn_in=0)
    def rotl(v, r):
        return ((v << r) | (v >> (32 - r))) & 0xFFFFFFFF
    
    # Apply rotation to each element of x before XORing with l
    x_rotated = np.array([rotl(int(v), 13) for v in x], dtype=np.uint32)
    out = (l ^ x_rotated)[burn_in:]
    return out

# --- 4. Mersenne Twister (MT19937) via numpy ---
def mt19937(n, seed):
    """Generates a sequence using numpy's MT19937 implementation."""
    rg = np.random.Generator(np.random.MT19937(seed))
    return rg.integers(0, 2**32, size=n, dtype=np.uint32)

# --- 5. PCG64 (numpy) ---
def pcg64(n, seed):
    """Generates a sequence using numpy's PCG64 implementation."""
    rg = np.random.Generator(np.random.PCG64(seed))
    return rg.integers(0, 2**32, size=n, dtype=np.uint32)

# --- 6. OS-backed CSPRNG (os.urandom) ---
def csprng_os(n, seed=None): # Seed is ignored, kept for harness compatibility
    """Generates a sequence using the operating system's entropy source."""
    data = os.urandom(4 * n)
    return np.frombuffer(data, dtype=np.uint32)

# --- 7. Quantum-inspired: SHA-256(counter || pool) whitening ---
def q_inspired_sha256(n, seed=None): # Seed is ignored, kept for harness compatibility
    """
    Generates a sequence by whitening a system entropy pool with SHA-256.
    Returns the sequence only, for harness compatibility.
    """
    pool = os.urandom(32)
    counter = 0
    out = np.empty(n, dtype=np.uint32)
    i = 0
    while i < n:
        h = hashlib.sha256(counter.to_bytes(8, 'little') + pool).digest()
        words = struct.unpack('<8I', h)  # 8 uint32 per block
        take = min(8, n - i)
        out[i:i+take] = words[:take]
        i += take
        counter += 1
    return out