from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from lotto_data import insert_winning_number
import re

def crawl_latest_winning():
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')  # 창이 뜨도록 headless OFF
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        url = "https://www.dhlottery.co.kr/gameResult.do?method=byWin"
        driver.get(url)

        # 번호 요소 로드 대기 (최대 20초)
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.num.win span"))
        )

        round_text = driver.find_element(By.CSS_SELECTOR, "div.win_result h4 strong").text
        round_num = int(re.search(r'\d+', round_text).group())

        # ✅ 1등 번호 (6개)
        num_tags = driver.find_elements(By.CSS_SELECTOR, "div.num.win span")
        main_numbers = [int(tag.text.strip()) for tag in num_tags if tag.text.strip().isdigit()]

        # ✅ 보너스 번호 따로
        bonus_tag = driver.find_element(By.CSS_SELECTOR, "div.num.bonus span")
        bonus = int(bonus_tag.text.strip())

        # 디버깅 로그
        print(f"📋 1등 번호 개수: {len(main_numbers)}")
        print(f"🎯 1등 번호: {main_numbers}")
        print(f"🎯 보너스 번호: {bonus}")

        if len(main_numbers) != 6:
            print("❌ 번호 크롤링 실패: 1등 번호가 6개가 아닙니다.")
            return

        # 추첨일
        date_text = driver.find_element(By.CSS_SELECTOR, "div.win_result p.desc").text
        date = date_text.split('(')[0].strip()

        # 총당첨금/인원/1인당
        tds = driver.find_elements(By.CSS_SELECTOR, "table.tbl_data tbody tr td")
        total_prize = int(tds[1].text.replace(',', '').replace('원', '').strip())
        winner_count = int(tds[2].text.replace(',', '').replace('명', '').strip())
        per_person = int(tds[3].text.replace(',', '').replace('원', '').strip())

        # ✅ DB 저장
        insert_winning_number(
            round_num,
            date,
            ','.join(map(str, main_numbers)),
            bonus,
            total_prize,
            winner_count,
            per_person
        )

        print(f"✅ {round_num}회 당첨번호 DB 입력 완료!")

    except Exception as e:
        print(f"❌ 크롤링 중 에러 발생: {e}")

    finally:
        driver.quit()

if __name__ == '__main__':
    crawl_latest_winning()






