import random
from lotto_data import get_recent_winning_numbers

def get_number_frequencies():
    """최근 10주 당첨번호 등장 횟수 계산"""
    recent_numbers = get_recent_winning_numbers(10)  # 최근 10주 번호
    freq = {}
    for nums in recent_numbers:
        for n in nums:
            freq[n] = freq.get(n, 0) + 1
    return freq

def generate_weighted_numbers(game_count):
    freq = get_number_frequencies()

    # 가중치 풀 생성
    weighted_pool = []
    for n in range(1, 46):
        count = freq.get(n, 1)  # 최소 1로 보장 (안 나온 번호도 선택 가능)
        weighted_pool.extend([n] * count)

    results = []
    for _ in range(game_count):
        selected = set()
        while len(selected) < 6:
            picked = random.choice(weighted_pool)
            selected.add(picked)
        results.append(sorted(selected))
    return results

