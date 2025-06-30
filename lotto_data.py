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
        '미추첨'
    ))
    conn.commit()
    conn.close()

def get_recommendations():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT id, round, date, numbers, grade FROM recommendations ORDER BY id DESC')
    rows = c.fetchall()
    conn.close()

    today = datetime.datetime.now()
    updated_rows = []

    latest_winning = get_latest_winning_info()
    winning_date = datetime.datetime.strptime(latest_winning['date'], '%Y-%m-%d') if latest_winning else None
    winning_numbers = list(map(int, latest_winning['numbers'].split(','))) if latest_winning else []
    bonus_number = int(latest_winning['bonus']) if latest_winning else None
    cutoff_time = datetime.time(21, 0)

    for row in rows:
        rec_id, round_num, date_str, numbers_str, grade = row
        rec_date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
        rec_numbers = list(map(int, numbers_str.split(',')))

        # 기준: 추첨일 전이거나 토요일 21시 이전이면 '미추첨'
        if winning_date and today < datetime.datetime.combine(winning_date.date(), cutoff_time):
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






