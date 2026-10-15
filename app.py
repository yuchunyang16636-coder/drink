import streamlit as st
import time
import random

# ==========================================
# ⚙️ 參數設定區
# ==========================================
BG_IMAGE_URL = "https://images.unsplash.com/photo-1478147427282-58a87a120781?q=80&w=2070&auto=format&fit=crop"
BASE_DELAY = 0.015       
BRAKE_FACTOR = 0.15      
STOP_FRAMES = [20, 40, 60, 80, 100]  

# ==========================================
# 1. 頁面與 CSS 視覺設定
# ==========================================
st.set_page_config(page_title="加碼抽獎系統", layout="wide", initial_sidebar_state="collapsed")

st.markdown(f"""
    <style>
    /* 隱藏預設選單、標頭與側邊欄 */
    header[data-testid="stHeader"] {{ display: none !important; }}
    section[data-testid="stSidebar"] {{ display: none !important; }}
    button[title="View fullscreen"] {{ display: none !important; }}
    
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url("{BG_IMAGE_URL}");
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }}
    
    .main-title {{
        text-align: center;
        font-size: 5rem;
        font-weight: 900;
        color: #FFD700;
        text-shadow: 2px 2px 10px rgba(255, 215, 0, 0.5);
        margin-bottom: 20px;
    }}
    
    /* 戰情儀表板樣式 */
    .dashboard-container {{
        display: flex;
        justify-content: center;
        gap: 30px;
        margin-bottom: 30px;
    }}
    
    .stat-box {{
        background: rgba(255, 255, 255, 0.1);
        border: 2px solid rgba(255, 215, 0, 0.5);
        border-radius: 10px;
        padding: 10px 30px;
        text-align: center;
        backdrop-filter: blur(5px);
    }}
    
    .stat-title {{ color: #ddd; font-size: 1.2rem; margin-bottom: 5px; }}
    .stat-value {{ color: #FFD700; font-size: 2.5rem; font-weight: bold; line-height: 1; }}

    .slot-box {{
        background: linear-gradient(180deg, rgba(34,34,34,0.9) 0%, rgba(0,0,0,0.9) 50%, rgba(34,34,34,0.9) 100%);
        color: #ffffff;
        font-size: 8rem;
        font-weight: bold;
        text-align: center;
        border-radius: 15px;
        padding: 20px 0;
        border: 4px solid #555;
        box-shadow: inset 0px 10px 20px rgba(0,0,0,0.8), 0 10px 20px rgba(0,0,0,0.5);
        font-family: 'Courier New', Courier, monospace;
    }}
    
    .slot-box.locked {{
        color: #FFD700;
        border-color: #FFD700;
        text-shadow: 0 0 20px #FFD700;
        background: linear-gradient(180deg, rgba(51,51,51,0.9) 0%, rgba(17,17,17,0.9) 50%, rgba(51,51,51,0.9) 100%);
    }}
    
    .winner-name {{
        text-align: center;
        font-size: 5rem;
        font-weight: 900;
        color: #00FF7F;
        margin-top: 20px;
        text-shadow: 3px 3px 15px rgba(0,0,0,0.9);
        animation: pulse 1s infinite alternate;
    }}
    
    @keyframes pulse {{
        0% {{ transform: scale(1); }}
        100% {{ transform: scale(1.05); }}
    }}
    
    div[data-testid="stButton"] > button {{
        background: linear-gradient(to bottom, #e52d27, #b31217) !important;
        color: white !important;
        height: 90px !important;
        border-radius: 45px !important;
        border: 3px solid #fff !important;
        box-shadow: 0 10px 25px rgba(0,0,0,0.7) !important;
        margin-top: 20px;
        margin-bottom: 20px;
    }}
    
    div[data-testid="stButton"] > button p {{
        font-size: 40px !important;
        font-weight: 900 !important;
        text-shadow: 2px 2px 5px rgba(0,0,0,0.5);
    }}
    
    /* 歷屆名單樣式優化 */
    .winner-card-container {{
        display: flex;
        flex-wrap: wrap;
        gap: 15px;
        justify-content: center;
        margin-top: 20px;
    }}
    
    .winner-card {{
        background: rgba(255, 255, 255, 0.95);
        color: #111;
        padding: 10px 20px;
        border-radius: 8px;
        font-size: 1.5rem;
        font-weight: bold;
        box-shadow: 0 4px 10px rgba(0,0,0,0.5);
        border-left: 5px solid #e52d27;
    }}
    
    .winner-card span {{
        color: #555;
        font-size: 1.2rem;
        margin-left: 8px;
    }}
    
    /* 右下角重置按鈕樣式 */
    .reset-btn-container {{ position: fixed; bottom: 20px; right: 20px; z-index: 999; }}
    .reset-btn-container button {{
        height: 50px !important; font-size: 16px !important; background: rgba(0,0,0,0.5) !important;
        border: 1px solid #555 !important; border-radius: 10px !important;
    }}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 自動匯入的人員名單
# ==========================================
if "FULL_ROSTER" not in st.session_state:
    st.session_state.FULL_ROSTER = {
        "08819": "江振明", "09274": "賴烱彰", "09644": "李文豪", "10184": "宋俊宏",
        "10807": "葉岱耿", "11088": "楊彩玲", "11265": "劉忠育", "12149": "梁家銘",
        "12151": "劉昆峰", "12153": "林賜松", "12155": "詹益昌", "12350": "蘇德龍", 
        "12430": "謝宗廷", "12431": "林啓祺", "12438": "林佳青", "12452": "賴建安",
        "12460": "陳士傑", "12596": "余嘉偉", "12744": "馬忠榕", "12772": "張書諺", 
        "13020": "賴日宏", "13024": "彭莉惠", "13082": "呉宗蔚", "13085": "羅匀男", 
        "13110": "王銘祥", "13112": "呉敏誌", "13114": "辜智源", "13390": "蔡國正", 
        "13391": "廖君桓", "13433": "王競德", "14942": "簡廷宇", "14971": "池文宇", 
        "15333": "吳岳興", "15334": "趙浩丞", "15983": "郭柏辰", "16636": "楊祐郡",
        "16684": "林俊哲", "17263": "吳信志", "17557": "蔡廸軒", "17770": "李玫錦", 
        "17771": "蘇煜恩", "17956": "陳妤真", "17959": "陳官哲", "17969": "哖欣穎",
        "17986": "廖學翊", "18116": "徐煒家", "70119": "松下靖"
    }

if "drawn_roster" not in st.session_state:
    st.session_state.drawn_roster = []

# ==========================================
# 3. 主畫面版面配置
# ==========================================
st.markdown('<div class="main-title">🎉 長官加碼幸運抽獎 🎉</div>', unsafe_allow_html=True)

# 計算戰情資訊
total_people = len(st.session_state.FULL_ROSTER)
drawn_count = len(st.session_state.drawn_roster)
remain_count = total_people - drawn_count
win_rate = round((1 / remain_count) * 100, 2) if remain_count > 0 else 0

# 顯示置中戰情儀表板
st.markdown(f"""
    <div class="dashboard-container">
        <div class="stat-box"><div class="stat-title">總人數</div><div class="stat-value">{total_people}</div></div>
        <div class="stat-box"><div class="stat-title">已中獎</div><div class="stat-value" style="color: #ff4b4b;">{drawn_count}</div></div>
        <div class="stat-box"><div class="stat-title">剩餘可抽</div><div class="stat-value">{remain_count}</div></div>
        <div class="stat-box"><div class="stat-title">中獎機率</div><div class="stat-value" style="color: #00FF7F;">{win_rate}%</div></div>
    </div>
""", unsafe_allow_html=True)

# 建立 5 個數字欄位
col1, col2, col3, col4, col5 = st.columns(5)
placeholders = [col1.empty(), col2.empty(), col3.empty(), col4.empty(), col5.empty()]

for p in placeholders:
    p.markdown('<div class="slot-box">?</div>', unsafe_allow_html=True)

winner_placeholder = st.empty()

# 按鈕置中
_, btn_col, _ = st.columns([1, 2, 1])
with btn_col:
    draw_clicked = st.button("🎰 啟動加碼抽獎", use_container_width=True)

# ==========================================
# 4. 抽獎與動畫邏輯
# ==========================================
available_pool = [uid for uid in st.session_state.FULL_ROSTER.keys() if uid not in st.session_state.drawn_roster]

if draw_clicked:
    if not available_pool:
        st.error("名單內的所有人都已經抽過囉！")
    else:
        winner_placeholder.empty()
        
        winner_id = random.choice(available_pool)
        winner_name = st.session_state.FULL_ROSTER[winner_id]
        target_digits = list(winner_id)
        
        st.session_state.drawn_roster.append(winner_id)
        
        stop_order = random.sample(range(5), 5)
        locked = [False] * 5
        
        for frame in range(1, STOP_FRAMES[-1] + 1):
            for i, target_frame in enumerate(STOP_FRAMES):
                if frame >= target_frame:
                    locked[stop_order[i]] = True
            
            for i in range(5):
                if locked[i]:
                    placeholders[i].markdown(f'<div class="slot-box locked">{target_digits[i]}</div>', unsafe_allow_html=True)
                else:
                    placeholders[i].markdown(f'<div class="slot-box">{random.randint(0, 9)}</div>', unsafe_allow_html=True)
            
            current_delay = BASE_DELAY + (frame / STOP_FRAMES[-1])**3 * BRAKE_FACTOR
            time.sleep(current_delay)
        
        st.balloons()
        # 取消打字特效，直接乾脆顯示
        winner_placeholder.markdown(f'<div class="winner-name">🎊 恭喜中獎：{winner_name} 🎊</div>', unsafe_allow_html=True)

# ==========================================
# 5. 公開中獎名單 (清晰卡片版)
# ==========================================
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown('<h2 style="color: #FFD700; text-align: center; text-shadow: 2px 2px 5px rgba(0,0,0,0.8);">🏆 歷屆加碼中獎名單</h2>', unsafe_allow_html=True)

if st.session_state.drawn_roster:
    cards_html = '<div class="winner-card-container">'
    for uid in reversed(st.session_state.drawn_roster):
        cards_html += f'<div class="winner-card">{st.session_state.FULL_ROSTER[uid]}<span>({uid})</span></div>'
    cards_html += '</div>'
    st.markdown(cards_html, unsafe_allow_html=True)
else:
    st.markdown('<p style="text-align: center; color: #ddd; font-size: 1.2rem;">目前尚無人中獎，趕快按下啟動按鈕吧！</p>', unsafe_allow_html=True)

# ==========================================
# 6. 右下角隱藏式重置按鈕
# ==========================================
st.markdown('<div class="reset-btn-container">', unsafe_allow_html=True)
if st.button("⚠️ 重置", key="reset_btn"):
    st.session_state.drawn_roster = []
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)
