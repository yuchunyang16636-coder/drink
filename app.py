import streamlit as st
import datetime

# ==========================================
# 1. 頁面基本設定與日系文青 CSS
# ==========================================
st.set_page_config(page_title="辦公室訂飲料系統", page_icon="🧋", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@700;900&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Zen Maru Gothic', sans-serif !important;
        font-weight: 700 !important;
    }
    .main-title {
        text-align: center;
        font-size: clamp(2rem, 8vw, 3.5rem); 
        font-weight: 900;
        color: #5A544B; 
        margin-bottom: 10px;
    }
    .sub-title {
        text-align: center;
        color: #8B9A92; 
        font-size: clamp(1.1rem, 4vw, 1.5rem);
        margin-bottom: 40px;
    }
    div[data-testid="stButton"] > button {
        background-color: #A3B19B !important; 
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 12px !important; 
        transition: all 0.3s ease !important;
    }
    div[data-testid="stButton"] > button:hover {
        background-color: #8F9E87 !important; 
        transform: translateY(-2px); 
    }
    .price-tag {
        font-size: 1.5rem;
        color: #d9534f;
        text-align: right;
        font-weight: 900;
        padding-top: 10px;
    }
    /* 訂單卡片樣式 */
    .order-card {
        background-color: #f9f9f9;
        border-left: 5px solid #A3B19B;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    header[data-testid="stHeader"] { display: none !important; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 多層次飲料店資料庫 (Shop -> Category -> Drink -> Size/Price)
# ==========================================
# 根據菜單圖片建立的結構範例。未來新增菜單只需依照此格式往下加即可。
SHOP_MENUS = {
    "得正": {
        "categories": {
            "Original TEA (原味茶)": {
                "紅茶": {"M": 25, "L": 30},
                "綠茶": {"M": 25, "L": 30},
                "春烏龍": {"M": 30, "L": 35},
                "焙烏龍": {"M": 30, "L": 35}
            },
            "Classic MILK TEA (奶茶)": {
                "奶茶": {"M": 45, "L": 50},
                "焙烏龍奶茶": {"M": 45, "L": 50},
                "珍珠奶茶": {"M": 55, "L": 60}
            }
        },
        "toppings": {"珍珠": 10, "黃金珍珠": 10, "焙烏龍茶凍": 10}
    },
    "可不可熟成紅茶": {
        "categories": {
            "乎乾。好茶": {
                "熟成紅茶": {"M": 30, "L": 35},
                "麗春紅茶": {"M": 30, "L": 35},
                "春芽綠茶": {"M": 30, "L": 35}
            },
            "乎乾。鮮奶茶": {
                "熟成歐蕾": {"M": 55, "L": 65},
                "白玉歐蕾": {"M": 60, "L": 70}
            }
        },
        "toppings": {"白玉珍珠": 10, "水玉晶球": 15, "春梅凍": 15}
    },
    "50嵐": {
        "categories": {
            "找好茶": {
                "茉莉綠茶": {"M": 30, "L": 35},
                "四季春青茶": {"M": 30, "L": 35},
                "波霸綠": {"M": 35, "L": 45}
            },
            "找奶茶": {
                "奶茶": {"M": 40, "L": 55},
                "波霸奶茶": {"M": 40, "L": 55}
            }
        },
        "toppings": {"波霸": 10, "珍珠": 10, "燕麥": 10, "椰果": 10}
    }
}

SUGAR_OPTIONS = ["正常糖", "少糖", "半糖", "微糖", "一分糖", "無糖"]
ICE_OPTIONS = ["正常冰", "少冰", "微冰", "去冰", "完全去冰", "溫", "熱"]

# ==========================================
# 3. 初始化 Session State
# ==========================================
if "page" not in st.session_state: st.session_state.page = "home"
if "device_type" not in st.session_state: st.session_state.device_type = ""
if "order_date" not in st.session_state: st.session_state.order_date = datetime.date.today()
if "shop_name" not in st.session_state: st.session_state.shop_name = "請選擇..."
if "orders" not in st.session_state: st.session_state.orders = []

def delete_order(index):
    st.session_state.orders.pop(index)

# ==========================================
# 4. 第一頁：極簡首頁 (選擇裝置)
# ==========================================
if st.session_state.page == "home":
    st.markdown('<div class="main-title">🧋 辦公室訂飲料系統</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">請選擇您的點餐裝置</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💻 電腦版", use_container_width=True):
            st.session_state.device_type = "網頁版"
            st.session_state.page = "order"
            st.rerun()
    with col2:
        if st.button("📱 手機版", use_container_width=True):
            st.session_state.device_type = "手機版"
            st.session_state.page = "order"
            st.rerun()

# ==========================================
# 5. 第二頁：點餐與購物車
# ==========================================
elif st.session_state.page == "order":
    col_back, col_title = st.columns([1, 4])
    with col_back:
        if st.button("⬅️ 返回首頁"):
            st.session_state.page = "home"
            st.rerun()
    with col_title:
        st.markdown(f"<div style='text-align: right; color: #8B9A92; padding-top: 10px;'>模式：{st.session_state.device_type}</div>", unsafe_allow_html=True)
        
    st.markdown("---")
    
    # --- 步驟 1：店家選擇 ---
    st.markdown("### 📋 步驟 1：設定飲料店")
    shop_options = ["請選擇..."] + list(SHOP_MENUS.keys()) + ["其他 (自行輸入)"]
    selected_shop = st.selectbox("🏪 選擇飲料店", options=shop_options, index=shop_options.index(st.session_state.shop_name) if st.session_state.shop_name in shop_options else 0)
    st.session_state.shop_name = selected_shop

    if st.session_state.shop_name != "請選擇...":
        st.markdown("---")
        # --- 步驟 2：點餐表單 ---
        st.markdown(f"### 📝 步驟 2：填寫點餐單 ({st.session_state.shop_name})")
        
        with st.container(border=True):
            user_name = st.text_input("👤 您的姓名 (必填)")
            
            # 計價變數初始化
            base_price = 0
            toppings_price = 0
            
            if st.session_state.shop_name == "其他 (自行輸入)":
                drink_name = st.text_input("🥤 飲料名稱")
                size = st.selectbox("📏 尺寸", ["M", "L", "瓶裝"])
                base_price = st.number_input("💰 飲料單價 (元)", min_value=0, value=0)
                selected_toppings = []
            else:
                # 動態連動選單：分類 -> 飲料 -> 尺寸 -> 價格
                shop_data = SHOP_MENUS[st.session_state.shop_name]
                categories = list(shop_data["categories"].keys())
                
                col_cat, col_drink = st.columns(2)
                with col_cat:
                    selected_category = st.selectbox("📑 選擇分類", categories)
                with col_drink:
                    drinks_in_cat = list(shop_data["categories"][selected_category].keys())
                    drink_name = st.selectbox("🥤 選擇飲料", drinks_in_cat)
                
                # 取得該飲料支援的尺寸與價格
                available_sizes = shop_data["categories"][selected_category][drink_name]
                
                col_size, col_topping = st.columns(2)
                with col_size:
                    size = st.radio("📏 尺寸", list(available_sizes.keys()), horizontal=True)
                    base_price = available_sizes[size] # 讀取基礎價格
                
                with col_topping:
                    available_toppings = list(shop_data["toppings"].keys())
                    selected_toppings = st.multiselect("➕ 加料 (可複選)", available_toppings)
                    # 計算加料總價
                    for t in selected_toppings:
                        toppings_price += shop_data["toppings"][t]

            col_sugar, col_ice = st.columns(2)
            with col_sugar:
                sugar = st.selectbox("🍬 甜度", SUGAR_OPTIONS, index=2)
            with col_ice:
                ice = st.selectbox("🧊 冰塊", ICE_OPTIONS, index=3)
                
            note = st.text_input("📝 備註 (其他客製化要求)")
            
            # 即時計算總價
            total_price = base_price + toppings_price
            st.markdown(f"<div class='price-tag'>小計：{total_price} 元</div>", unsafe_allow_html=True)
            
            if st.button("✅ 加入訂單", use_container_width=True, type="primary"):
                if user_name.strip() == "":
                    st.error("⚠️ 請填寫姓名！")
                else:
                    st.session_state.orders.append({
                        "name": user_name,
                        "drink": drink_name,
                        "size": size,
                        "toppings": ", ".join(selected_toppings) if selected_toppings else "無",
                        "sugar": sugar,
                        "ice": ice,
                        "note": note,
                        "price": total_price
                    })
                    st.success(f"已將 {user_name} 的 {drink_name} 加入清單！")
                    st.rerun()

        # --- 步驟 3：購物車清單與刪除修改功能 ---
        st.markdown("---")
        st.markdown("### 🛒 目前訂單清單")
        
        if len(st.session_state.orders) == 0:
            st.info("目前還沒有人點餐喔！")
        else:
            total_amount = sum(order["price"] for order in st.session_state.orders)
            st.markdown(f"**總杯數：** {len(st.session_state.orders)} 杯 ｜ **總金額：** {total_amount} 元")
            
            # 顯示每一筆訂單並附帶刪除按鈕
            for i, order in enumerate(st.session_state.orders):
                st.markdown(f"""
                <div class="order-card">
                    <b>👤 {order["name"]}</b> ── {order["drink"]} ({order["size"]}) <br>
                    <span style="color:#666; font-size:0.9em;">
                    🍬 {order["sugar"]} | 🧊 {order["ice"]} | ➕ 加料: {order["toppings"]} | 💰 ${order["price"]}<br>
                    📝 備註: {order["note"]}
                    </span>
                </div>
                """, unsafe_allow_html=True)
                
                # Streamlit 的按鈕需要獨立的 key
                if st.button("❌ 刪除此筆", key=f"del_{i}"):
                    delete_order(i)
                    st.rerun()
