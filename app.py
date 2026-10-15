import streamlit as st
import time
import random
import base64

# ==========================================
# ⚙️ 參數設定區
# ==========================================
# 👇 請將你的背景圖片上傳到 GitHub，並將檔名填寫在這裡 (例如: "bg.jpg" 或 "background.png")
BG_IMAGE_PATH = "bg.jpg"

BASE_DELAY = 0.015       
BRAKE_FACTOR = 0.15      
STOP_FRAMES = [20, 40, 60, 80, 100]  

# ==========================================
# 圖片轉碼工具 (讓 Streamlit 能直接讀取本地圖片做為背景)
# ==========================================
def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return ""

bg_base64 = get_base64_of_bin_file(BG_IMAGE_PATH)

# 如果有成功讀取到圖片，就套用圖片背景；否則套用預設深色背景
if bg_base64:
    bg_css = f"""
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url("data:image/jpeg;base64,{bg_base64}");
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    """
else:
    bg_css = "background: #222;"

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
        {bg_css}
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
        background: linear-gradient(180deg, rgba(51,51,51,0.9) 0%, rgba(17,17,17,0.9) 50%, rgba
