import pytest

from search import boyer_moore_search, kmp_search, rabin_karp_search

ALGORITHMS = [boyer_moore_search, kmp_search, rabin_karp_search]

# (текст, підрядок), результат порівнюю з вбудованим str.find
CASES = [
    ("hello world", "hello"),  # збіг на початку
    ("hello world", "lo wo"),  # у середині
    ("hello world", "world"),  # у кінці
    ("hello world", "xyz"),  # немає
    ("abc", "abcdef"),  # підрядок довший за текст
    ("abc", "abc"),  # підрядок дорівнює тексту
    ("aaaaaaaab", "aaaaab"),  # повтори: таблиця префіксів КМП, зсуви БМ
    ("abababc", "ababc"),  # частковий збіг перед справжнім
    ("abcabcabc", "abc"),  # кілька входжень -> перше
    ("abcabcabc", "cab"),
    ("Двійковий пошук працює швидко", "пошук"),  # кирилиця
    ("Двійковий пошук працює швидко", "повільно"),
    ("hello", ""),  # порожній підрядок -> 0
    ("", "a"),  # порожній текст
    ("a", "a"),
    ("ab", "b"),
]


@pytest.mark.parametrize("search", ALGORITHMS, ids=lambda f: f.__name__)
@pytest.mark.parametrize("text, pattern", CASES)
def test_matches_str_find(search, text, pattern):
    assert search(text, pattern) == text.find(pattern)
