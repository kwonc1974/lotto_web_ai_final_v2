import sqlite3

# DB 연결
conn = sqlite3.connect('lotto.db')
c = conn.cursor()

# winning_numbers 테이블 새로 생성 (당첨금 포함)
c.execute('DROP TABLE IF EXISTS winning_numbers')
c.execute('''
    CREATE TABLE winning_numbers (
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

print("🎉 DB 초기화 완료: winning_numbers 테이블 (당첨금 포함) 생성됨!")

