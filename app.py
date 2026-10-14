import streamlit as st
import time
import random

# ==========================================
# 1. 頁面與 CSS 視覺設定
# ==========================================
st.set_page_config(page_title="加碼抽獎系統", layout="wide")

st.markdown("""
    <style>
    /* 隱藏預設選單與標頭 */
    header[data-testid="stHeader"] { display: none !important; }
    
    /* 大標題樣式 */
    .main-title {
        text-align: center;
        font-size: 5rem;
        font-weight: 900;
        color: #FFD700;
        text-shadow: 2px 2px 10px rgba(255, 215, 0, 0.5);
        margin-bottom: 30px;
    }
    
    /* 拉霸機數字框樣式 */
    .slot-box {
        background: linear-gradient(180deg, #222 0%, #000 50%, #222 100%);
        color: #ffffff;
        font-size: 8rem;
        font-weight: bold;
        text-align: center;
        border-radius: 15px;
        padding: 20px 0;
        border: 4px solid #555;
        box-shadow: inset 0px 10px 20px rgba(0,0,0,0.8), 0 10px 20px rgba(0,0,0,0.5);
        font-family: 'Courier New', Courier, monospace;
    }
    
    /* 數字鎖定後的發光樣式 */
    .slot-box.locked {
        color: #FFD700;
        border-color: #FFD700;
        text-shadow: 0 0 20px #FFD700;
        background: linear-gradient(180deg, #333 0%, #111 50%, #333 100%);
    }
    
    /* 恭喜中獎者姓名樣式 */
    .winner-name {
        text-align: center;
        font-size: 4rem;
        font-weight: 900;
        color: #00FF7F;
        margin-top: 30px;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.8);
        animation: pulse 1s infinite alternate;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        100% { transform: scale(1.05); }
    }
    
    /* 抽獎按鈕放大 */
    div[data-testid="stButton"] > button {
        background: linear-gradient(to bottom, #e52d27, #b31217) !important;
        color: white !important;
        height: 80px !important;
        font-size: 30px !important;
        font-weight: 900 !important;
        border-radius: 40px !important;
        border: 2px solid #fff !important;
        box-shadow: 0 8px 15px rgba(0,0,0,0.5) !important;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 模擬內部人員名單 (未來可替換為 Excel/CSV 讀取)
# ==========================================
# 這裡使用 Dictionary 對應 5位數卡號 -> 姓名
ROSTER = {
    "10001": "王大明",
    "20045": "李小華",
    "35099": "張阿春",
    "48102": "陳美麗",
    "55688": "林霸天",
    "88888": "總經理",
    "90321": "黃大仙"
}

# ==========================================
# 3. 主畫面版面配置
# ==========================================
st.markdown('<div class="main-title">🎉 長官加碼幸運抽獎 🎉</div>', unsafe_allow_html=True)

# 建立 5 個欄位來放置拉霸機數字
col1, col2, col3, col4, col5 = st.columns(5)
placeholders = [col1.empty(), col2.empty(), col3.empty(), col4.empty(), col5.empty()]

# 預設畫面顯示問號
for p in placeholders:
    p.markdown('<div class="slot-box">?</div>', unsafe_allow_html=True)

# 建立一個佔位符來顯示最終的得獎者姓名
winner_placeholder = st.empty()

# 置中放置抽獎按鈕
_, btn_col, _ = st.columns([1, 1, 1])

# ==========================================
# 4. 抽獎與動畫邏輯
# ==========================================
with btn_col:
    draw_clicked = st.button("🎰 啟動加碼抽獎", use_container_width=True)

if draw_clicked:
    # 每次按鈕按下時，先清空上一次的得獎者名字
    winner_placeholder.empty()
    
    # 步驟 A: 在背景先決定好得獎者是誰
    winner_id = random.choice(list(ROSTER.keys()))
    winner_name = ROSTER[winner_id]
    target_digits = list(winner_id)  # 將 "10001" 拆成 ['1', '0', '0', '0', '1']
    
    # 步驟 B: 決定數字鎖定的順序 (保證不會死板地由左至右)
    # random.sample(range(5), 5) 會產生如 [2, 0, 4, 1, 3] 的隨機順序
    stop_order = random.sample(range(5), 5)
    locked = [False] * 5
    
    # 步驟 C: 執行拉霸動畫
    total_frames = 100  # 總共跳動 100 個影格
    for frame in range(total_frames):
        # 根據影格進度，依序鎖定隨機欄位
        if frame == 20: locked[stop_order[0]] = True
        if frame == 40: locked[stop_order[1]] = True
        if frame == 60: locked[stop_order[2]] = True
        if frame == 80: locked[stop_order[3]] = True
        if frame == 99: locked[stop_order[4]] = True
        
        # 更新 5 個欄位的畫面
        for i in range(5):
            if locked[i]:
                # 已鎖定的欄位顯示正確數字與發光特效
                placeholders[i].markdown(f'<div class="slot-box locked">{target_digits[i]}</div>', unsafe_allow_html=True)
            else:
                # 未鎖定的欄位繼續亂數跳動
                placeholders[i].markdown(f'<div class="slot-box">{random.randint(0, 9)}</div>', unsafe_allow_html=True)
        
        # 控制滾動速度 (越小轉越快)
        time.sleep(0.04)
    
    # 步驟 D: 動畫結束，噴發氣球並顯示姓名
    st.balloons()
    winner_placeholder.markdown(f'<div class="winner-name">🎊 恭喜中獎：{winner_name} 🎊</div>', unsafe_allow_html=True)
