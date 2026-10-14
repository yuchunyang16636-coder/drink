import streamlit as st
import openpyxl
import io
from datetime import datetime
from openai import OpenAI

# ==========================================
# 1. 網頁基本設定與 UI
# ==========================================
st.set_page_config(page_title="AI 技術報告自動生成器", layout="wide", page_icon="📄")

st.title("📄 AI 技術報告自動生成器")
st.markdown("> 將零散的實驗筆記與數據交給 AI，一鍵自動提煉並輸出為公司標準 Excel 技術報告！")

# 側邊欄設定 API Key
with st.sidebar:
    st.header("⚙️ 系統設定")
    api_key = st.text_input("請輸入 OpenAI API Key", type="password")
    st.info("※ 必須提供 API Key 才能喚醒 AI 進行文字彙整。")

# ==========================================
# 2. 報告基本資料輸入區
# ==========================================
st.subheader("1. 填寫報告基本資訊")
col1, col2, col3 = st.columns(3)
with col1:
    report_title = st.text_input("報告標題", "カエル外觀檢查機自動化檢討")
with col2:
    department = st.selectbox("課別", ["生産技術一課", "生産技術二課", "生産技術三課", "カメラ生産技術課", "実装技術課"])
with col3:
    author = st.text_input("作成者", "你的名字")

# ==========================================
# 3. 原始草稿輸入區
# ==========================================
st.subheader("2. 貼上原始草稿 / 實驗筆記")
raw_notes = st.text_area(
    label="請盡情貼上散亂的重點、數據或遇到什麼困難與解法：",
    height=200, 
    placeholder="例如：\n之前測試了CCD跟EOS R5，不良現象都不清楚。\n後來發現EOS M3加上CCS光源跟0.5mm光圈最好，不用UV光也能看清楚。\n但是M3停產了要找替代品。\n另外短焦距鏡片YN4-2183距離只有18mm太近，加了YN3-1114輔助鏡片拉長到51mm，問題解決。"
)

# ==========================================
# 4. 核心處理邏輯 (AI 提煉 + 寫入 Excel)
# ==========================================
if st.button("🚀 施展魔法：自動生成 Excel 報告！", type="primary", use_container_width=True):
    if not api_key:
        st.error("⚠️ 請先在左側輸入 OpenAI API Key！")
    elif not raw_notes.strip():
        st.warning("⚠️ 請先輸入一些草稿內容讓 AI 處理喔！")
    else:
        with st.spinner("🧠 AI 正在燃燒腦力為您整理專業報告..."):
            try:
                # -------------------------
                # Step A: 呼叫 OpenAI API
                # -------------------------
                client = OpenAI(api_key=api_key)
                prompt = f"""
                請將以下工程師的零散研究筆記與數據，整理成一份專業的日文/中文技術檢討報告。
                請嚴格輸出兩個段落，並以 '|||' 分隔（前面是目的與過程，後面是結論與課題）：
                1. 目的與檢討過程 (專業、客觀，控制在200字以內)
                2. 結論與後續課題 (條理分明，控制在150字以內)

                原始筆記：
                {raw_notes}
                """
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3
                )
                
                # 解析 AI 回傳結果
                result_text = response.choices[0].message.content
                parts = result_text.split('|||')
                purpose_text = parts[0].strip() if len(parts) > 0 else "無法生成目的"
                conclusion_text = parts[1].strip() if len(parts) > 1 else "無法生成結論"

                st.success("✅ AI 彙整完成！正在為您寫入 Excel...")
                
                # 預覽區塊
                with st.expander("👀 點我預覽 AI 寫好的報告內容", expanded=True):
                    st.markdown("**【目的與檢討過程】**")
                    st.write(purpose_text)
                    st.markdown("**【結論與後續課題】**")
                    st.write(conclusion_text)

                # -------------------------
                # Step B: 將內容寫入 Excel
                # -------------------------
                try:
                    # 讀取剛剛請你準備好的 template.xlsx
                    wb = openpyxl.load_workbook("template.xlsx")
                    sheet = wb.worksheets[0]

                    # 填入基本資料 (座標依據你提供的範本結構，若有偏差可自行修改如 'J2', 'L4' 等)
                    sheet['J2'] = report_title                  # 標題
                    sheet['J4'] = datetime.now().strftime("%Y/%m/%d") # 日期
                    sheet['L4'] = department                    # 課別
                    sheet['J3'] = author                        # 作成者
                    
                    # 填入 AI 生成的大段落文字
                    sheet['C6'] = purpose_text                  # 目的與過程
                    sheet['C12'] = conclusion_text              # 結論與後續

                    # 將編輯好的 Excel 存入記憶體緩衝區 (BytesIO) 以供直接下載
                    output = io.BytesIO()
                    wb.save(output)
                    output.seek(0)

                    st.markdown("---")
                    st.download_button(
                        label="📥 下載完成的 Excel 技術報告",
                        data=output,
                        file_name=f"{datetime.now().strftime('%Y%m%d')}_{report_title}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        type="primary",
                        use_container_width=True
                    )
                except FileNotFoundError:
                    st.error("❌ 找不到 `template.xlsx`！請先將公司的 `技術報告範本.xls` 另存新檔為 `template.xlsx` 並放在同一資料夾下。")
                    
            except Exception as e:
                st.error(f"❌ 發生未預期的錯誤：{e}")
