from flask import Flask, request, render_template
import requests

app = Flask(__name__)

# 💡 1. 建立中俄文題庫
zh_ru_dict = {
    "你好": "Здравствуйте (Zdravstvuyte)",
    "謝謝": "Спасибо (Spasibo)",
    "請": "Пожалуйста (Pozhaluysta)",
    "對不起": "Извините (Izvinite)",
    "再見": "До свидания (Do svidaniya)",
    "早安": "Доброе утро (Dobroye utro)",
    "晚安": "Спокойной ноchi (Spokoynoy nochi)",
    "老師": "Учитель (Uchitel')",
    "學生": "Студент (Student)",
    "朋友": "Друг (Drug)",
    "家人": "Семья (Sem'ya)",
    "愛": "Любовь (Lyubov')"
}


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/competition')
def competition():
    return render_template('competition.html')


# 💡 2. 中翻俄文查詢功能
@app.route('/ask', methods=['GET', 'POST'])
def ask():
    if request.method == 'POST':
        question1 = request.form.get('question', '').strip()
        # 查詢俄文題庫，若查不到則給予提示
        answer1 = zh_ru_dict.get(question1, "抱歉，我目前沒有這個詞的俄文對應。")
        return render_template('ask.html', question=question1, answer=answer1)
    return render_template('ask.html', question="", answer="")


# 💡 3. 恢復原本的課外活動（留下原本的版面與互動邏輯）
@app.route('/activities', methods=['GET', 'POST'])
def activities():
    if request.method == 'POST':
        # 讀取學生的問題
        question = request.form.get('question', '').strip()
        # 查詢課外活動的對應答案（預設提示）
        answer1 = "抱歉，我目前沒有這個詞的韓文對應。"
        # 回傳答案給學生
        return render_template('activities.html', question=question, answer=answer1)
    # GET 時給空白欄位
    return render_template('activities.html', question="", answer="")


# 💡 4. 新增：第八版面獨立的西洋棋歷史介紹路由
@app.route('/chess')
def chess():
    # 建立西洋棋歷史的結構化資料，方便網頁渲染
    chess_history = {
        "title": "西洋棋的千古演變史",
        "origin": "西洋棋最早可追溯至西元 6 世紀的印度「恰圖蘭卡」（Chaturanga），當時這款遊戲代表了由戰車、大象、騎兵和步兵組成的古代軍隊。",
        "evolution": "隨後傳入波斯並演變為「沙特蘭茲」（Shatranj）。15 世紀末，這項遊戲在歐洲進行了重大改革，國王、皇后與主教擁有了現代的移動規則，讓節奏變得更加快速刺激。",
        "modern": "19 世紀中葉，現代西洋棋錦標賽正式誕生。如今在 AI 與電腦深藍（Deep Blue）的挑戰下，西洋棋已成為全球最普及、最受推崇的智力競技運動之一。"
    }
    # 對應讀取 templates/chess.html
    return render_template('chess.html', history=chess_history)


# 💡 5. 固定查詢 00918（大華優利高填息30）股價
@app.route('/stock', methods=['GET', 'POST'])
def stock():
    stock_no = "00918"  # 固定為 00918
    stock_name = "大華優利高填息30"
    
    # 修正：更新為台灣證交所正確的 API 完整網址
    url = f"https://twse.com.tw{stock_no}"
    
    try:
        res = requests.get(url)
        data = res.json()
        
        if data.get("stat") == "OK":
            # data["data"][-1] 為當月最新一天的交易紀錄，陣列中第 6 個元素 (索引 6) 為收盤價
            latest_trade = data["data"][-1]
            trade_date = latest_trade[0]   # 交易日期
            closing_price = latest_trade[6] # 最新收盤價
            answer = f"日期：{trade_date}，最新收盤價為：{closing_price} 元"
        else:
            answer = "目前證交所未回傳資料，可能為非交易日或系統維護中。"
    except Exception as e:
        answer = f"連線證交所失敗: {e}"

    # 因為改為自動查詢，無論 GET 還是 POST 都直接把 00918 的結果帶入網頁中呈現
    return render_template('stock.html', question=f"{stock_no} {stock_name}", answer=answer)


@app.route('/leadership')
def leadership():
    return render_template('leadership.html')

@app.route('/club')
def club():
    return render_template('club.html')

@app.route('/electives')
def electives():
    return render_template('electives.html')

@app.route('/ai')
def ai():
    return render_template('ai.html')


if __name__ == '__main__':
    app.run(debug=True)


if __name__ == '__main__':
    app.run(debug=True)
