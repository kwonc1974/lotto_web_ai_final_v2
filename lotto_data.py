import os
import sqlite3
import datetime
import requests
from bs4 import BeautifulSoup

# 🔧 절대 경로 설정 (Render 배포 호환용)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, 'lotto.db')

# ✅ DB가 없으면 자동 생성
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # 추천 기록 테이블
    c.execute('''
        CREATE TABLE IF NOT EXISTS recommendations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            round INTEGER,
            date TEXT,
            numbers TEXT,
            grade TEXT
        )
    ''')

    # 당첨 번호 테이블
    c.execute('''
        CREATE TABLE IF NOT EXISTS winning_numbers (
            round INTEGER PRIMARY KEY,
            date TEXT,
            numbers TEXT,
            bonus INTEGER,
            total_prize INTEGER,
            winner_count INTEGER,
            per_person INTEGER
        )
    ''')

    conn.commit()
    conn.close()

# ✅ 최신 당첨 정보 가져오기
def get_latest_winning_info():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT round, date, numbers, bonus FROM winning_numbers ORDER BY round DESC LIMIT 1')
    row = c.fetchone()
    conn.close()

    if row:
        return {
            'round': row[0],
            'date': row[1],
            'numbers': row[2],
            'bonus': row[3]
        }
    return None

# ✅ 추천 번호 저장
def save_recommendation(numbers):
    latest = get_latest_winning_info()
    round_num = latest['round'] + 1 if latest else 1
    date_str = datetime.date.today().isoformat()

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO recommendations (round, date, numbers, grade)
        VALUES (?, ?, ?, ?)
    ''', (round_num, date_str, ','.join(map(str, numbers)), '미추첨'))
    conn.commit()
    conn.close()

# ✅ 추천 기록 전체 조회
def get_recommendations():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT id, round, date, numbers, grade FROM recommendations ORDER BY id DESC')
    rows = c.fetchall()
    conn.close()

    result = []
    for row in rows:
        result.append({
            'id': row[0],
            'round': row[1],
            'date': row[2],
            'numbers': row[3],
            'grade': row[4]
        })
    return result

# ✅ 당첨 번호 저장
def save_winning_numbers(round_num, date_str, numbers, bonus):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT OR REPLACE INTO winning_numbers (round, date, numbers, bonus, total_prize, winner_count, per_person)
        VALUES (?, ?, ?, ?, NULL, NULL, NULL)
    ''', (round_num, date_str, ','.join(map(str, numbers)), bonus))
    conn.commit()
    conn.close()

# ✅ 웹에서 최신 당첨 번호 가져오기
def fetch_latest_winning_numbers():
    url = 'https://dhlottery.co.kr/gameResult.do?method=byWin'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    round_text = soup.select_one('.win_result h4 strong').text.strip().replace('회', '')
    round_num = int(round_text)

    date_str = soup.select_one('.win_result .desc').text.strip()
    date_str = date_str.replace('추첨일 : ', '').replace('.', '-').strip()

    win_numbers = [int(tag.text.strip()) for tag in soup.select('.num.win p span')]
    bonus = int(soup.select_one('.bonus + .num span').text.strip())

    return {
        'round': round_num,
        'date': date_str,
        'numbers': win_numbers,
        'bonus': bonus
    }

# ✅ DB 초기화 (reset용)
def reset_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('DELETE FROM recommendations')
    conn.commit()
    conn.close()







