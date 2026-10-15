import streamlit as st
import time
import random

# ==========================================
# 1. 頁面與 CSS 視覺設定
# ==========================================
st.set_page_config(page_title="加碼抽獎系統", layout="wide")

st.markdown("""
    <style>
    header[data-testid="stHeader"] { display: none !important; }
    
    .main-title {
        text-align: center;
        font-size: 5rem;
        font-weight: 900;
        color: #FFD700;
        text-shadow: 2px 2px 10px rgba(255, 215, 0, 0.5);
        margin-bottom: 30px;
    }
    
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
    
    .slot-box.locked {
        color: #FFD700;
        border-color: #FFD700;
        text-shadow: 0 0 20px #FFD700;
        background: linear-gradient(180deg, #333 0%, #111 50%, #333 100%);
    }
    
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
# 2. 自動匯入的人員名單 (萃取自 PDF)
# ==========================================
# 這是從你提供的 PDF 擷取出來的完整 74 人名單
if "FULL_ROSTER" not in st.session_state:
    st.session_state.FULL_ROSTER = {
        "08819": "江振明", "09274": "賴烱彰", "09644": "李文豪", "10184": "宋俊宏",
        "10807": "葉岱耿", "10916": "陳高爵", "11088": "楊彩玲", "11265": "劉忠育",
        "12149": "梁家銘", "12151": "劉昆峰", "12153": "林賜松", "12155": "詹益昌",
        "12350": "蘇德龍", "12420": "林峻弘", "12425": "林仲葦", "12430": "謝宗廷",
        "12431": "林啓祺", "12438": "王銘祥", "12451": "黄耀弘", "12452": "賴建安",
        "12460": "陳士傑", "12596": "余嘉偉", "12697": "徐崇益", "12744": "馬忠榕",
        "12772": "張書諺", "12846": "林昇治", "13020": "賴日宏", "13021": "張皓誠",
        "13024": "彭莉惠", "13059": "陳映宏", "13060": "廖愷文", "13082": "呉宗蔚",
        "13085": "羅匀男", "13110": "松下靖", "13112": "呉敏誌", "13114": "辜智源",
        "13115": "盧政偉", "13390": "蔡國正", "13391": "廖君桓", "13419": "簡志宏",
        "13433": "王競德", "13840": "卓孟翰", "13841": "李柏昌", "14360": "馮文毅",
        "14515": "陳勇全", "14526": "陳榮傑", "14563": "林位達", "14564": "黃文豪",
        "14942": "簡廷宇", "14971": "池文宇", "15333": "吳岳興", "15334": "趙浩丞",
        "15983": "郭柏辰", "15986": "陳丙元", "16106": "王怡翔", "16636": "楊祐郡",
        "16639": "蔡明恩", "16649": "陳伯翰", "16684": "林俊哲", "17263": "吳信志",
        "17557": "蔡廸軒", "17755": "何思諭", "17770": "李玫錦", "17771": "蘇煜恩",
        "17798": "許豪志", "17956": "陳妤真", "17959": "陳官哲", "17969": "哖欣穎",
        "17977": "林家輝", "17986": "廖學翊", "18060": "謝震昱", "18082": "曾偉豪",
        "18116": "徐煒家", "70119": "松下"
    }

# 使用 session_state 來記錄「已中獎名單」，達成抽過排除的功能
if "drawn_roster" not in st.session_state:
    st.session_state.drawn_roster = []

# ==========================================
# 3. 主畫面版面配置
# ==========================================
st.markdown('<div class="main-title">🎉 長官加碼幸運抽獎 🎉</div>', unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)
placeholders = [col1.empty(), col2.empty(), col3.empty(), col4.empty(), col5.empty()]

for p in placeholders:
    p.markdown('<div class="slot-box">?</div>', unsafe_allow_html=True)

winner_placeholder = st.empty()
_, btn_col, _ = st.columns([1, 1, 1])

# ==========================================
# 4. 抽獎與動畫邏輯 (優化版)
# ==========================================
with btn_col:
    draw_clicked = st.button("🎰 啟動加碼抽獎", use_container_width=True)

# 找出還沒中獎的人 (排除已抽過的名單)
available_pool = [uid for uid in st.session_state.FULL_ROSTER.keys() if uid not in st.session_state.drawn_roster]

if draw_clicked:
    if not available_pool:
        st.error("名單內的所有人都已經抽過囉！")
    else:
        winner_placeholder.empty()
        
        # 決定得獎者
        winner_id = random.choice(available_pool)
        winner_name = st.session_state.FULL_ROSTER[winner_id]
        target_digits = list(winner_id)
        
        # 紀錄已抽過
        st.session_state.drawn_roster.append(winner_id)
        
        # 決定亂數跳停順序
        stop_order = random.sample(range(5), 5)
        locked = [False] * 5
        
        # --- 逼真的煞車動畫 (由快到極慢) ---
        # 這裡設定 5 個欄位分別在第幾次跳動時鎖定
        # 例如第一個停在第 15 跳，最後一個要撐到第 60 跳才停
        stop_frames = [15, 25, 35, 45, 60] 
        
        base_delay = 0.03 # 初始速度 (修改這裡可調整最快速度)
        
        for frame in range(1, stop_frames[-1] + 1):
            # 檢查並鎖定該停的欄位
            for i, target_frame in enumerate(stop_frames):
                if frame == target_frame:
                    locked[stop_order[i]] = True
            
            # 更新畫面
            for i in range(5):
                if locked:
