import random
from lotto_data import get_recent_numbers

def generate_hybrid_numbers(game_count):
    recent_numbers = get_recent_numbers()
    results = []

    attempts = 0
    while len(results) < game_count and attempts < 100:
        attempts += 1
        selected = set()

        # 최근 번호에서 2~3개 선택
        while len(selected) < 3:
            selected.add(random.choice(recent_numbers))

        # 나머지 번호 랜덤으로 채우기
        while len(selected) < 6:
            n = random.randint(1, 45)
            selected.add(n)

        # 구간별 균형 체크 (1~10, 11~20, ..., 41~45)
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

        if max(counts) > 4:
            continue  # 한쪽 구간에 너무 몰리면 다시 시도

        results.append(sorted(selected))

    return results






