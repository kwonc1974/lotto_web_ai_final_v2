import sqlite3

def init_db():
    conn = sqlite3.connect('lotto.db')
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
    print("DB 초기화 완료 (lotto.db 생성됨)")

if __name__ == '__main__':
    init_db()


