from crawl_winning import crawl_latest_winning

def main():
    print("🧠 당첨번호 자동 업데이트 시작!")
    try:
        crawl_latest_winning()
        print("🎉 당첨번호 업데이트 완료!")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    main()
