import random
from lotto_data import get_recent_numbers

def generate_hybrid_numbers(game_count):
    recent_numbers = get_recent_numbers()
    results = []

    for _ in range(game_count):
        selected = set()

        # 최근 번호에서 2~3개
        while len(selected) < 3:
            selected.add(random.choice(recent_numbers))

        # 구간별 번호 추가
        while len(selected) < 6:
            n = random.randint(1, 45)
            if n not in selected:
                selected.add(n)

        # 구간 균형 검사 (1~10, 11~20, ...)
        counts = [0] * 5
        for n in selected:
            if n <= 10:
                counts[0] += 1
            elif n <= 20:
                counts[1] += 1
            elif n <= 30:
                counts[2] += 1
            elif n <= 40:
                counts[3] += 1
            else:
                counts[4] += 1

        # 너무 한쪽 구간에 몰리면 재시도
        if max(counts) > 3:
            continue

        results.append(sorted(selected))

    return results





