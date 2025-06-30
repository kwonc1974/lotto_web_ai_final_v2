import schedule
import time
import subprocess
from datetime import datetime

def run_update():
    print(f"🔄 [{datetime.now()}] 당첨 결과 업데이트 실행 중...")
    subprocess.run(["python", "auto_update.py"], shell=True)

# 매주 토요일 밤 9시에 실행
schedule.every().saturday.at("21:00").do(run_update)

print("🕒 스케줄러 작동 시작... (CTRL+C로 종료)")

while True:
    schedule.run_pending()
    time.sleep(60)
