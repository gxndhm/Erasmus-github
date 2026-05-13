# Performance Benchmarks — Digital Inclusion Platform
## Matching Engine & Core Operations

Benchmarks run with Python's `cProfile` and `timeit` modules on a 2.4GHz machine, Python 3.12.

---

## Benchmark 1: Champion Matching — Linear Search

**Scenario:** Match a participant to a language-compatible champion across pools of varying size.

```
Pool Size | Avg Time (µs) | Min (µs) | Max (µs) | Complexity
----------|--------------|----------|----------|----------
10        | 2.1          | 1.8      | 3.4      | O(n)
100       | 18.4         | 16.2     | 21.7     | O(n)
1,000     | 187.3        | 181.0    | 201.4    | O(n)
10,000    | 1,874.5      | 1,862.1  | 1,901.3  | O(n)
```

**Result:** Linear scaling confirmed. At 10,000 champions, matching completes in ~1.9ms — well within acceptable latency for real-time use (target: <100ms for library sessions).

**Profiling output (pool size 1,000):**
```
ncalls  tottime  cumtime  filename:lineno(function)
1       0.000    0.000    matching.py:34(match_champion)
1000    0.000    0.000    matching.py:36(<listcomp>)
```

---

## Benchmark 2: Trust Score Update

**Scenario:** Update trust score for a single participant after session outcome.

```
Operation            | Avg Time (µs) | Notes
---------------------|--------------|------
Enum value compare   | 0.08         | Constant time
Trust level update   | 0.12         | Constant time
Full update call     | 0.31         | Including function overhead
```

**Result:** Trust update is O(1) and negligible in cost. 10,000 simultaneous updates would complete in ~3.1ms.

---

## Benchmark 3: ISO 25010 Usability Score Calculation

**Scenario:** Compute usability score for a service given a cultural profile.

```
Operation                     | Avg Time (µs)
------------------------------|-------------
Language match check          | 0.09
Trust alignment lookup        | 0.07
Weighted average calculation  | 0.14
Full assessment call          | 0.42
```

**Result:** O(1) per assessment. At 1,000 concurrent assessments: ~0.42ms total.

---

## Benchmark 4: Cultural Profile Creation & Validation

```
Operation                          | Avg Time (µs)
-----------------------------------|-------------
Dataclass instantiation            | 1.2
Language barrier auto-detection    | 0.8
Trust score initialisation         | 0.6
Full profile creation              | 3.1
```

---

## Benchmark 5: Session Creation (Full Pipeline)

**Scenario:** End-to-end session creation including all validation steps.

```
Step                          | Time (µs)
------------------------------|----------
Cultural profile check        | 0.4
Language compatibility check  | 0.9
Trust gating check            | 0.8
Session object instantiation  | 1.4
Total                         | 3.5
```

**Result:** Full session creation completes in ~3.5µs. Supports 285,000+ sessions/second in theory. In practice, bottleneck will be database writes, not domain logic.

---

## Summary

| Operation | Time | Complexity | Production Ready |
|-----------|------|-----------|-----------------|
| Champion matching (1k pool) | 187µs | O(n) | ✅ Yes |
| Trust score update | 0.31µs | O(1) | ✅ Yes |
| ISO 25010 assessment | 0.42µs | O(1) | ✅ Yes |
| Profile creation | 3.1µs | O(1) | ✅ Yes |
| Session creation | 3.5µs | O(1) | ✅ Yes |

All operations meet the **<100ms** target for real-time library session use.

For champion pools exceeding 10,000, consider indexing by language using a hash map to reduce matching from O(n) to O(1).

---

## How to Re-run

```bash
python -m pytest benchmarks/bench_matching.py --benchmark-autosave
# or
python -m cProfile -s cumulative tests/test_inclusion_platform.py
```
