def boyer_moore_search(text: str, pattern: str) -> int:
    m, n = len(pattern), len(text)
    if m == 0:
        return 0
    last = {char: i for i, char in enumerate(pattern)}
    shift = 0
    while shift <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[shift + j]:
            j -= 1
        if j < 0:
            return shift
        shift += max(1, j - last.get(text[shift + j], -1))
    return -1


def compute_lps(pattern: str) -> list[int]:
    lps = [0] * len(pattern)
    k = 0
    for i in range(1, len(pattern)):
        while k and pattern[i] != pattern[k]:
            k = lps[k - 1]
        if pattern[i] == pattern[k]:
            k += 1
        lps[i] = k
    return lps


def kmp_search(text: str, pattern: str) -> int:
    m = len(pattern)
    if m == 0:
        return 0
    lps = compute_lps(pattern)
    k = 0
    for i, char in enumerate(text):
        while k and char != pattern[k]:
            k = lps[k - 1]
        if char == pattern[k]:
            k += 1
        if k == m:
            return i - m + 1
    return -1


def rabin_karp_search(
    text: str, pattern: str, base: int = 256, mod: int = 1_000_000_007
) -> int:
    m, n = len(pattern), len(text)
    if m == 0:
        return 0
    if m > n:
        return -1
    high = pow(base, m - 1, mod)  
    pattern_hash = window_hash = 0
    for i in range(m):
        pattern_hash = (pattern_hash * base + ord(pattern[i])) % mod
        window_hash = (window_hash * base + ord(text[i])) % mod
    for shift in range(n - m + 1):
        if pattern_hash == window_hash and text[shift : shift + m] == pattern:
            return shift
        if shift < n - m:
            window_hash = (
                (window_hash - ord(text[shift]) * high) * base + ord(text[shift + m])
            ) % mod
    return -1
