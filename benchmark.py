import timeit
from pathlib import Path

from search import boyer_moore_search, kmp_search, rabin_karp_search

ALGORITHMS = {
    "Боєр-Мур": boyer_moore_search,
    "КМП": kmp_search,
    "Рабін-Карп": rabin_karp_search,
}

FAKE = "вигаданий підрядок, якого тут немає 12345"
ARTICLES = {
    "Стаття 1": ("article1.txt", "Жадібні алгоритми. Distance learning"),
    "Стаття 2": ("article2.txt", "Zero-suppressed BDDs and their applications"),
}

NUMBER = 20  # скільки разів викликаємо функцію за один замір
REPEAT = 5  # скільки замірів робимо, беремо найменший


def measure(func, text: str, pattern: str) -> float:
    best = min(timeit.repeat(lambda: func(text, pattern), number=NUMBER, repeat=REPEAT))
    return best / NUMBER * 1000


def main() -> None:
    here = Path(__file__).parent
    totals = dict.fromkeys(ALGORITHMS, 0.0)

    print("| Текст | Підрядок | " + " | ".join(ALGORITHMS) + " |")
    print("|---|---|" + "---:|" * len(ALGORITHMS))

    winners = {}
    for title, (filename, existing) in ARTICLES.items():
        text = (here / filename).read_text(encoding="utf-8")
        assert existing in text, f"{title}: 'існуючий' підрядок не знайдено"
        assert FAKE not in text, f"{title}: 'вигаданий' підрядок існує"

        article_totals = dict.fromkeys(ALGORITHMS, 0.0)
        for kind, pattern in (("існуючий", existing), ("вигаданий", FAKE)):
            times = {name: measure(f, text, pattern) for name, f in ALGORITHMS.items()}
            for name, t in times.items():
                article_totals[name] += t
                totals[name] += t
            print(f"| {title} | {kind} | " + " | ".join(f"{t:.4f}" for t in times.values()) + " |")
        winners[title] = min(article_totals, key=article_totals.get)

    print("\nЧас одного пошуку, мс (менше — краще).\n")
    for title, name in winners.items():
        print(f"- Найшвидший для «{title}»: **{name}**")
    print(f"- Найшвидший загалом: **{min(totals, key=totals.get)}**")
    print("\nСумарний час, мс: " + ", ".join(f"{n} — {t:.4f}" for n, t in totals.items()))


if __name__ == "__main__":
    main()
