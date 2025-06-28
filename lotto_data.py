import sqlite3
import datetime

DB_NAME = 'lotto.db'

def save_recommendation(numbers):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO recommendations (round, date, numbers, grade)
        VALUES (?, ?, ?, ?)
    ''', (
        get_latest_round(),
        datetime.date.today().isoformat(),
        ','.join(map(str, numbers)),
        '낙첨'
    ))
    conn.commit()
    conn.close()

def get_recommendations():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT id, round, date, numbers, grade FROM recommendations ORDER BY id DESC')
    rows = c.fetchall()
    conn.close()
    return [
        {'id': row[0], 'round': row[1], 'date': row[2], 'numbers': row[3], 'grade': row[4]}
        for row in rows
    ]

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
    print("추천 기록 초기화 완료")

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
    """최근 limit 회차의 번호 출현 빈도"""
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
    """최근 limit 회차 번호들을 모두 모아서 리스트 반환"""
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
    """최근 limit 회차 당첨번호를 리스트 of 리스트 형태로 반환"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(f"SELECT numbers FROM winning_numbers ORDER BY round DESC LIMIT {limit}")
    rows = c.fetchall()
    conn.close()
    return [
        [int(n) for n in row[0].split(',')]
        for row in rows
    ]






