from flask import Flask, render_template, request, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from api_winning import fetch_and_store_winning
from lotto_data import get_latest_winning_info, get_recommendations, reset_db

app = Flask(__name__)

def humanize_money(value):
    try:
        value = int(value)
        if value >= 10**8:
            return f"{value / 10**8:.1f}억"
        elif value >= 10**4:
            return f"{value / 10**4:.1f}만"
        else:
            return f"{value}원"
    except:
        return str(value)

app.jinja_env.filters['humanize_money'] = humanize_money

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/result')
def result():
    win_info = get_latest_winning_info()
    results = get_recommendations()
    return render_template("result.html", win_info=win_info, results=results)

@app.route('/reset_db')
def reset():
    pw = request.args.get('pw', '')
    if pw != '1234':
        return jsonify({"success": False, "message": "❌ 비밀번호가 틀렸습니다."})
    reset_db()
    return jsonify({"success": True, "message": "✅ DB가 초기화되었습니다."})

def scheduled_job():
    latest = get_latest_winning_info()
    next_round = (latest['round'] + 1) if latest else 1
    print(f"스케줄러: {next_round}회 당첨번호 조회 시도")
    fetch_and_store_winning(next_round)

# 스케줄러는 gunicorn 실행 시 같이 작동하도록 여기서 시작
scheduler = BackgroundScheduler()
scheduler.add_job(scheduled_job, 'cron', day_of_week='sat', hour=21, minute=0)
scheduler.start()




















