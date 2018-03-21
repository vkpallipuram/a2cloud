"""Typical counters available to perf.
All of these are verified available on the University of Pacific SOECS Cluster.
"""


class FPCounters():
    """Floating point hardware counters.
    """
    fp_comp_ops_exe__sse_x87 = "fp_comp_ops_exe.x87"
    fp_comp_ops_exe__sse_packed_double = "fp_comp_ops_exe.sse_packed_double"
    fp_comp_ops_exe__sse_packed_single = "fp_comp_ops_exe.sse_packed_single"
    fp_comp_ops_exe__sse_scalar_double = "fp_comp_ops_exe.sse_scalar_double"
    fp_comp_ops_exe__sse_scalar_single = "fp_comp_ops_exe.sse_scalar_single"
    simd_fp_256__packed_double = "simd_fp_256.packed_double"
    simd_fp_256__packed_single = "simd_fp_256.packed_single"


class MemCounters():
    """Memory related counters (kernel event based)
    """
    cpu_mem_loads = "cpu/mem-loads/"
    cpu_mem_stores = "cpu/mem-stores/"
    uncore_imc_0__cas_count_read  = "uncore_imc_0/cas_count_read/"
    uncore_imc_0__cas_count_write = "uncore_imc_0/cas_count_write/"
    uncore_imc_1__cas_count_read  = "uncore_imc_1/cas_count_read/"
    uncore_imc_1__cas_count_write = "uncore_imc_1/cas_count_write/"
    uncore_imc_2__cas_count_read  = "uncore_imc_2/cas_count_read/"
    uncore_imc_2__cas_count_write = "uncore_imc_2/cas_count_write/"
    uncore_imc_3__cas_count_read  = "uncore_imc_3/cas_count_read/"
    uncore_imc_3__cas_count_write = "uncore_imc_3/cas_count_write/"
    uncore_imc_4__cas_count_read  = "uncore_imc_4/cas_count_read/"
    uncore_imc_4__cas_count_write = "uncore_imc_4/cas_count_write/"
    uncore_imc_5__cas_count_read  = "uncore_imc_5/cas_count_read/"
    uncore_imc_5__cas_count_write = "uncore_imc_5/cas_count_write/"
    uncore_imc_6__cas_count_read  = "uncore_imc_6/cas_count_read/"
    uncore_imc_6__cas_count_write = "uncore_imc_6/cas_count_write/"
    uncore_imc_7__cas_count_read  = "uncore_imc_7/cas_count_read/"
    uncore_imc_7__cas_count_write = "uncore_imc_7/cas_count_write/"


class CacheCounters():
    """Cache related counters
    """
    cache_references = "cache-references"
    cache_misses = "cache-misses"
    llc_loads = "LLC-loads"
    llc_stores = "LLC-stores"
    llc_load_misses = "LLC-load-misses"
    llc_store_misses = "LLC-store-misses"