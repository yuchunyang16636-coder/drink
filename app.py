import streamlit as st
import time
import random

# ==========================================
# ⚙️ 參數設定區 (你可以隨時在這裡修改)
# ==========================================
# 1. 背景圖片 (可以換成公司大樓照片、活動視覺圖的網址)
BG_IMAGE_URL = "https://images.unsplash.com/photo-1478147427282-58a87a120781?q=80&w=2070&auto=format&fit=crop"

# 2. 拉霸機節奏與速度設定
BASE_DELAY = 0.015       # 初始滾動速度 (越小越快、畫面越流暢)
BRAKE_FACTOR = 0.15      # 煞車摩擦力 (數字越大，最後幾個數字停下來前越慢、越吊胃口)
# 下面陣列代表五個格子分別在第幾次跳動時「鎖定」
# 如果覺得太快出現，可以把數字加大 (例如 [30, 60, 90, 120, 150])
STOP_FRAMES = [20, 40, 60, 80, 100]  

# ==========================================
# 1. 頁面與 CSS 視覺設定
# ==========================================
st.set_page_config(page_title="加碼抽獎系統", layout="wide")

st.markdown(f"""
    <style>
    /* 隱藏預設選單與標頭 */
    header[data-testid="stHeader"] {{ display: none !important; }}
    
    /* 替換背景圖片並加上暗色遮罩讓字體更清楚 */
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
        margin-bottom: 30px;
    }}
    
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
        font-size: 4.5rem;
        font-weight: 900;
        color: #00FF7F;
        margin-top: 20px;
        text-shadow: 3px 3px 10px rgba(0,0,0,0.9);
    }}
    
    /* 啟動按鈕放大優化 */
    div[data-testid="stButton"] > button {{
        background: linear-gradient(to bottom, #e52d27, #b31217) !important;
        color: white !important;
        height: 100px !important;
        border-radius: 50px !important;
        border: 3px solid #fff !important;
        box-shadow: 0 10px 25px rgba(0,0,0,0.7) !important;
        margin-top: 20px;
        margin-bottom: 20px;
    }}
    
    /* 啟動按鈕文字變大 */
    div[data-testid="stButton"] > button p {{
        font-size: 45px !important;
        font-weight: 900 !important;
        text-shadow: 2px 2px 5px rgba(0,0,0,0.5);
    }}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 自動匯入的人員名單
# ==========================================
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

if "drawn_roster" not in st.session_state:
    st.session_state.drawn_roster = []

# ==========================================
# 3. 主畫面版面配置
# ==========================================
st.markdown('<div class="main-title">🎉 長官加碼幸運抽獎 🎉</div>', unsafe_allow_html=True)

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
        
        # 決定得獎者
        winner_id = random.choice(available_pool)
        winner_name = st.session_state.FULL_ROSTER[winner_id]
        target_digits = list(winner_id)
        
        # 加入已抽過名單
        st.session_state.drawn_roster.append(winner_id)
        
        # 決定亂數停頓的順序
        stop_order = random.sample(range(5), 5)
        locked = [False] * 5
        
        # 拉霸滾動動畫 (流暢版)
        for frame in range(1, STOP_FRAMES[-1] + 1):
            for i, target_frame in enumerate(STOP_FRAMES):
                if frame >= target_frame:
                    locked[stop_order[i]] = True
            
            for i in range(5):
                if locked[i]:
                    placeholders[i].markdown(f'<div class="slot-box locked">{target_digits[i]}</div>', unsafe_allow_html=True)
                else:
                    placeholders[i].markdown(f'<div class="slot-box">{random.randint(0, 9)}</div>', unsafe_allow_html=True)
            
            # 煞車機制：依據目前進度加上摩擦力，越後面越慢
            current_delay = BASE_DELAY + (frame / STOP_FRAMES[-1])**3 * BRAKE_FACTOR
            time.sleep(current_delay)
        
        st.balloons()
        
        # 中獎者姓名特效：逐字出現 (打字機效果)
        display_text = "🎊 恭喜中獎："
        for char in winner_name:
            display_text += char
            winner_placeholder.markdown(f'<div class="winner-name">{display_text}</div>', unsafe_allow_html=True)
            time.sleep(0.4) # 每個字彈出來的間隔時間
            
        # 結尾補上彩帶符號
        winner_placeholder.markdown(f'<div class="winner-name">{display_text} 🎊</div>', unsafe_allow_html=True)

# ==========================================
# 5. 公開中獎名單 (顯示於主畫面下方)
# ==========================================
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown('<h3 style="color: #FFD700;">🏆 歷屆加碼中獎名單</h3>', unsafe_allow_html=True)

if st.session_state.drawn_roster:
    # 將已中獎的卡號轉換為「姓名 (卡號)」的格式並顯示
    winners_list = [f"**{st.session_state.FULL_ROSTER[uid]}** ({uid})" for uid in reversed(st.session_state.drawn_roster)]
    st.info(" 、 ".join(winners_list))
else:
    st.write("目前尚無人中獎，趕快按下啟動按鈕吧！")

# 左下角控制台
with st.sidebar:
    st.write(f"👥 可抽獎總人數: {len(available_pool)}")
    st.write(f"🏆 已中獎人數: {len(st.session_state.drawn_roster)}")
    if st.button("⚠️ 重置抽獎名單 (清空紀錄)"):
        st.session_state.drawn_roster = []
        st.rerun()
