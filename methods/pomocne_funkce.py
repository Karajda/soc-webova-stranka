from mpmath import mp

REAL_PI = mp.pi
REAL_E = mp.e
REAL_FI = mp.phi

def spravne_desetinne(approx, real):
    approx_s = str(approx)
    real_s = str(real)
    count = 0
    for a, b in zip(approx_s, real_s):
        if a != b:
            break
        count += 1
    return max(count - 2, 0)

def a(n):
    if n == 0:
        return 2
    if n % 3 == 2:
        return 2 * ((n + 1) // 3)
    return 1