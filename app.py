from flask import Flask, render_template, request, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from api_winning import fetch_and_store_winning
from lotto_data import (
    get_latest_winning_info, get_recommendations, reset_db,
    save_recommendation, init_db  # ✅ DB 초기화 함수 포함
)
from hybrid_generator import generate_hybrid_numbers
from smart_generator import generate_weighted_numbers
import datetime

app = Flask(__name__)

# ✅ 앱 실행 시 DB 자동 생성 (Render 환경 대응)
init_db()

# 📦 단위 변환 필터 (ex. 1억, 500만 등)
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

# 🔷 홈 페이지
@app.route('/')
def index():
    return render_template("index.html")

# 🔷 결과 페이지
@app.route('/result')
def result():
    win_info = get_latest_winning_info()
    results = get_recommendations()
    return render_template("result.html", win_info=win_info, results=results)

# 🔷 DB 초기화 (비밀번호 체크)
@app.route('/reset_db')
def reset():
    pw = request.args.get('pw', '')
    if pw != '1234':
        return jsonify({"success": False, "message": "❌ 비밀번호가 틀렸습니다."})
    reset_db()
    return jsonify({"success": True, "message": "✅ DB가 초기화되었습니다."})

# 🔷 추천 번호 생성
@app.route('/generate')
def generate():
    now = datetime.datetime.now()
    # 추천 제한: 토요일 21시 이후, 일요일 차단
    if now.weekday() == 6 or (now.weekday() == 5 and now.hour >= 21):
        return jsonify({"error": "❌ 추천은 월~토요일 21시 이전까지만 가능합니다."})

    hybrid_count = int(request.args.get('hybrid', 0))
    smart_count = int(request.args.get('smart', 0))

    results = []

    if hybrid_count > 0:
        results += generate_hybrid_numbers(hybrid_count)

    if smart_count > 0:
        results += generate_weighted_numbers(smart_count)

    for line in results:
        save_recommendation(line)

    return jsonify(results)

# 🔷 수동으로 당첨번호 업데이트
@app.route('/update_winning')
def update_winning():
    try:
        latest = get_latest_winning_info()
        next_round = (latest['round'] + 1) if latest else 1
        fetch_and_store_winning(next_round)
        return jsonify({"success": True, "message": f"{next_round}회차 당첨번호 업데이트 완료"})
    except Exception as e:
        return jsonify({"success": False, "message": f"업데이트 실패: {str(e)}"})

# 🕒 로컬용 스케줄러 함수
def scheduled_job():
    latest = get_latest_winning_info()
    next_round = (latest['round'] + 1) if latest else 1
    print(f"[스케줄러] {next_round}회 당첨번호 조회 시도")
    fetch_and_store_winning(next_round)

# 🕒 토요일 21시 자동 실행 (로컬 전용 / Render는 cron-job.org 사용)
scheduler = BackgroundScheduler()
scheduler.add_job(scheduled_job, 'cron', day_of_week='sat', hour=21, minute=0)
scheduler.start()

# 앱 실행
if __name__ == '__main__':
    app.run(debug=True)























