import sqlite3
import datetime
import os

# ✅ Render 서버에 영구 저장되는 경로
DB_NAME = '/mnt/data/lotto.db'

# ✅ DB 및 테이블 초기화 함수 (없으면 자동 생성)
def init_database():
    if not os.path.exists(DB_NAME):
        print("[⚙️] DB 파일이 존재하지 않음. 새로 생성합니다.")
    else:
        print("[✅] DB 파일 존재 확인:", DB_NAME)

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # recommendations 테이블 생성
    c.execute('''
        CREATE TABLE IF NOT EXISTS recommendations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            round INTEGER,
            date TEXT,
            numbers TEXT,
            grade TEXT
        )
    ''')

    # winning_numbers 테이블 생성
    c.execute('''
        CREATE TABLE IF NOT EXISTS winning_numbers (
            round INTEGER PRIMARY KEY,
            date TEXT,
            numbers TEXT,
            bonus_number INTEGER,
            total_prize TEXT,
            winner_count TEXT,
            per_person TEXT
        )
    ''')

    conn.commit()
    conn.close()
    print("[✔️] DB 및 테이블 초기화 완료")

# 앱 구동 시 초기화 시도
init_database()

def save_recommendation(numbers):
    print("[DEBUG] 저장 시도 - 추천 번호:", numbers)
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        next_round = get_latest_round() + 1
        c.execute('''
            INSERT INTO recommendations (round, date, numbers, grade)
            VALUES (?, ?, ?, ?)
        ''', (
            next_round,
            datetime.date.today().isoformat(),
            ','.join(map(str, numbers)),
            '미추첨'
        ))
        conn.commit()
        conn.close()
        print(f"[✅] 추천번호 저장 완료 (회차: {next_round})")
    except Exception as e:
        print("[❌] 추천번호 저장 실패:", e)

def get_recommendations():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT id, round, date, numbers, grade FROM recommendations ORDER BY id DESC')
    rows = c.fetchall()
    conn.close()

    latest = get_latest_winning_info()
    latest_round = latest['round'] if latest else 0
    winning_numbers = list(map(int, latest['numbers'].split(','))) if latest else []
    bonus_number = int(latest['bonus']) if latest else None

    updated_rows = []

    for row in rows:
        rec_id, round_num, date_str, numbers_str, _ = row
        rec_numbers = list(map(int, numbers_str.split(',')))

        if round_num > latest_round:
            grade = '미추첨'
        else:
            match_count = len(set(rec_numbers) & set(winning_numbers))
            has_bonus = bonus_number in rec_numbers
            if match_count == 6:
                grade = '1등'
            elif match_count == 5 and has_bonus:
                grade = '2등'
            elif match_count == 5:
                grade = '3등'
            elif match_count == 4:
                grade = '4등'
            elif match_count == 3:
                grade = '5등'
            else:
                grade = '낙첨'

        updated_rows.append({
            'id': rec_id,
            'round': round_num,
            'date': date_str,
            'numbers': numbers_str,
            'grade': grade
        })

    return updated_rows

def get_latest_winning_info():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM winning_numbers ORDER BY round DESC LIMIT 1')
    row = c.fetchone()
    conn.close()
    if row:
        return {
            'round': row[0],
            'date': row[1],
            'numbers': row[2],
            'bonus': row[3],
            'total_prize': row[4],
            'winner_count': row[5],
            'per_person': row[6]
        }
    return None

def get_latest_round():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT MAX(round) FROM winning_numbers')
    row = c.fetchone()
    conn.close()
    return row[0] if row[0] else 0

def reset_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('DELETE FROM recommendations')
    conn.commit()
    conn.close()
    print("[⚠️] 추천 기록 초기화 완료")

def insert_winning_number(round_num, date, numbers, bonus, total_prize, winner_count, per_person):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT OR REPLACE INTO winning_numbers
        (round, date, numbers, bonus_number, total_prize, winner_count, per_person)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (round_num, date, numbers, bonus, total_prize, winner_count, per_person))
    conn.commit()
    conn.close()

def get_number_frequencies(limit=10):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(f"SELECT numbers FROM winning_numbers ORDER BY round DESC LIMIT {limit}")
    rows = c.fetchall()
    freq = {}
    for row in rows:
        nums = row[0].split(',')
        for n in nums:
            n = int(n)
            freq[n] = freq.get(n, 0) + 1
    conn.close()
    return freq

def get_recent_numbers(limit=10):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(f"SELECT numbers FROM winning_numbers ORDER BY round DESC LIMIT {limit}")
    rows = c.fetchall()
    numbers = []
    for row in rows:
        nums = [int(n) for n in row[0].split(',')]
        numbers.extend(nums)
    conn.close()
    return numbers

def get_recent_winning_numbers(limit=10):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(f"SELECT numbers FROM winning_numbers ORDER BY round DESC LIMIT {limit}")
    rows = c.fetchall()
    conn.close()
    return [
        [int(n) for n in row[0].split(',')]
        for row in rows
    ]








