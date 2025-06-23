from hybrid_generator import generate_hybrid_numbers
from smart_generator import generate_weighted_numbers
from simulator import simulate_random_sets

# 하이브리드 추천 5게임
hybrid_results = generate_hybrid_numbers(5)
print("💡 하이브리드 추천:")
for line in hybrid_results:
    print(line)

# 스마트 추천 5게임
smart_results = generate_weighted_numbers(5)
print("\n💡 스마트 추천:")
for line in smart_results:
    print(line)

# 시뮬레이션 1000세트 생성
simulated = simulate_random_sets(1000)
print(f"\n✅ 시뮬레이션 1000세트 생성 완료. 샘플 3세트:")
for s in simulated[:3]:
    print(s)
