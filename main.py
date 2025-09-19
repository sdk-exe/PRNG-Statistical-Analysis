# main.py
# The main script to run the full testing battery on all PRNGs.

import numpy as np
import generators as gen
import statistical_tests as tests

# --- CONTROL FLAG ---
# Set to True to print detailed results for every seed, False for summary only.
VERBOSE_MODE = True

def compute_metrics_for_uint32_array(x_uint32, K=256, lags=(1, 2, 3, 4, 5)):
    """Computes all metrics for a given array of uint32 numbers."""
    u = tests.to_unit_float(x_uint32)
    
    H, counts = tests.hist_entropy(u, K=K)
    Hnorm = H / np.log2(K) if K > 1 else 0.0
    
    chi, pchi = tests.chi_square_uniformity(counts)
    
    p_lags = []
    for k in lags:
        _, pk = tests.autocorr_lag(u, k)
        p_lags.append(pk)
        
    runs_results = tests.runs_test(u)
    
    rqs_dict = tests.rqs_from_stats(Hnorm, pchi, p_lags, runs_results['p'])
    
    # Add other detailed stats for verbose output
    if VERBOSE_MODE:
        rqs_dict['p_chi'] = pchi
        rqs_dict['p_runs'] = runs_results['p']
        
    return rqs_dict

def run_benchmark():
    """Runs the full benchmark and prints the results."""
    
    prng_generators = {
        "LCG": gen.lcg32,
        "XORShift": gen.xorshift32,
        "Hybrid": gen.hybrid32,
        "MT19937": gen.mt19937,
        "PCG64": gen.pcg64,
        "CSPRNG": gen.csprng_os,
        "QuantumInspired": gen.q_inspired_sha256
    }
    
    seeds = [42, 424242, 1337, 8675309, 1234567, 314159, 271828, 1618033, 4444, 9001]
    N_SAMPLES = 100000
    
    print("Running PRNG benchmark...")
    results = {}
    
    for name, gen_func in prng_generators.items():
        print(f"  Testing {name}...")
        all_run_metrics = []
        is_deterministic = gen_func.__code__.co_argcount >= 2

        for seed in seeds:
            x_uint32 = gen_func(N_SAMPLES, seed) if is_deterministic else gen_func(N_SAMPLES)
            metrics = compute_metrics_for_uint32_array(x_uint32)
            all_run_metrics.append(metrics)
            
        results[name] = {
            'RQS_mean': np.mean([m['RQS'] for m in all_run_metrics]),
            'RQS_std': np.std([m['RQS'] for m in all_run_metrics]),
            'per_run_metrics': all_run_metrics
        }
        
    if VERBOSE_MODE:
        print("\n--- Detailed Per-Seed Results ---")
        for name, data in results.items():
            print(f"\nGenerator: {name}")
            print(f"  {'Seed':<10} | {'RQS':<8} | {'p_chi':<8} | {'p_runs':<8}")
            print("  " + "-" * 40)
            for i, run_metrics in enumerate(data['per_run_metrics']):
                seed_val = seeds[i] if name not in ["CSPRNG", "QuantumInspired"] else f"Run {i+1}"
                print(f"  {str(seed_val):<10} | {run_metrics['RQS']:.4f}   | {run_metrics['p_chi']:.4f}   | {run_metrics['p_runs']:.4f}")
    
    print("\n--- Benchmark Summary (Table 1) ---")
    print(f"{'Generator':<25} | {'RQS Mean':<12} | {'RQS Std. Dev.':<15}")
    print("-" * 58)
    for name, data in results.items():
        print(f"{name:<25} | {data['RQS_mean']:<12.4f} | {data['RQS_std']:<15.4f}")
    print("-" * 58)

if __name__ == "__main__":
    run_benchmark()