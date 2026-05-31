import streamlit as st
import datetime

# 1. 极致精简配置
st.set_page_config(page_title="Work Report", layout="centered")

# 2. 强力 CSS：锁定布局，配色与大小优化
st.markdown("""
    <style>
    /* 隐藏所有多余 UI */
    #MainMenu, footer, header {visibility: hidden;}
    
    /* 全局背景色 */
    .stApp {background-color: #FFFFFF;}
    
    /* 定义行布局：强制左标签、右输入框 */
    .row-box {
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        justify-content: space-between !important;
        padding: 5px 0 !important;
    }
    
    /* 标签文字样式 */
    .label-text { font-size: 14px; color: #333333; font-weight: 500; }
    
    /* 输入框样式：强制宽度，隐藏加减号 */
    .stNumberInput, .stTextInput, .stTextArea { width: 140px !important; }
    div[data-testid="stNumberInput"] button { display: none !important; }
    </style>
""", unsafe_allow_html=True)

st.title("Work Report V1.0")

# 辅助函数：生成一行布局
def row(label, component):
    st.markdown(f'<div class="row-box"><div class="label-text">{label}</div><div>', unsafe_allow_html=True)
    component
    st.markdown('</div></div>', unsafe_allow_html=True)

# 3. 页面内容
end_time = st.text_input("et", value="22:00", label_visibility="collapsed")
row("Deadline", end_time)

qty = st.number_input("qty", value=0, step=1, label_visibility="collapsed")
row("Quantity", qty)

st.write("---")
st.markdown("### Working Hours")
hourly_hours = {}
for hour in range(10, 23):
    val = st.number_input(f"h{hour}", min_value=0.0, value=None, label_visibility="collapsed")
    row(f"{hour}:00", val)
    hourly_hours[hour] = val

st.write("---")
notes = st.text_area("notes", value="", placeholder="Additional info...", label_visibility="collapsed")
st.markdown("Other Notes")
st.markdown(f'<div style="margin-top:-10px;">', unsafe_allow_html=True)
notes
st.markdown('</div>', unsafe_allow_html=True)

# 4. 按钮
st.write("---")
if st.button("Generate Report", use_container_width=True):
    total = sum([h for h in hourly_hours.values() if h is not None])
    eff = (qty / total) if total > 0 else 0
    today = datetime.date.today().strftime("%m/%d")
    
    report = f"{today}\nDeadline: {end_time}\nQuantity: {qty}\nHours: {total:.1f}\nEfficiency: {eff:.2f}\n\nNotes: {notes}"
    st.success("Report Generated!")
    st.code(report, language="text")
    st.info("Long press the text above to copy")
