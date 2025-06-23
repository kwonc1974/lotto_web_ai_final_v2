import requests
from lotto_data import insert_winning_number

def fetch_and_store_winning(round_num):
    url = f"https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={round_num}"
    res = requests.get(url)
    data = res.json()

    if data.get("returnValue") != "success":
        print(f"❌ 데이터 수신 실패 (회차: {round_num})")
        return

    main_numbers = [data[f"drwtNo{i}"] for i in range(1, 7)]
    bonus = data["bnusNo"]
    date = data["drwNoDate"]

    insert_winning_number(
        data["drwNo"],
        date,
        ','.join(map(str, main_numbers)),
        bonus,
        0,  # 총 당첨금 데이터는 API 미제공, 필요 시 크롤링 보완
        0,
        0
    )
    print(f"✅ {data['drwNo']}회 당첨번호 DB 입력 완료!")
