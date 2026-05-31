import streamlit as st
import datetime

# 1. 极致精简配置
st.set_page_config(page_title="维修报告助手", layout="centered")

# 2. 精致化 CSS 配色方案
st.markdown("""
    <style>
    /* 隐藏多余界面元素 */
    #MainMenu, footer, header {visibility: hidden;}
    
    /* 页面基础字体与颜色 */
    .stApp {background-color: #FAFAFA;}
    
    /* 标题样式 */
    h1 {font-size: 24px !important; color: #333 !important; margin-bottom: 20px;}
    h3 {font-size: 18px !important; color: #555 !important; margin-top: 20px;}
    
    /* 强制 Grid 布局，锁定左列(标签)右列(输入框) */
    .grid-container {
        display: grid !important;
        grid-template-columns: 80px 1fr !important;
        align-items: center !important;
        gap: 15px !important;
        margin-bottom: 8px !important;
    }
    
    /* 标签文字样式 */
    .label-text {font-size: 14px; color: #666;}
    
    /* 输入框样式微调 */
    .stNumberInput, .stTextInput, .stTextArea {margin-top: -10px !important;}
    div[data-testid="stNumberInput"] button {display: none;}
    </style>
""", unsafe_allow_html=True)

st.title("维修报告生成工具 V1.0")

# 3. 布局逻辑
# 使用 HTML div 包装的 Grid 布局
def input_row(label, component):
    st.markdown(f'<div class="grid-container"><div class="label-text">{label}</div><div>', unsafe_allow_html=True)
    component
    st.markdown('</div></div>', unsafe_allow_html=True)

# 顶部基础信息
quantity = st.number_input("qty", value=0, label_visibility="collapsed")
input_row("维修数量", quantity)

end_time = st.text_input("time", value="22:00", label_visibility="collapsed")
input_row("截止时间", end_time)

# 4. 工时输入 (10-22点)
st.write("---")
st.subheader("维修工时")
hourly_hours = {}
for hour in range(10, 23):
    hourly_hours[hour] = st.number_input(f"h{hour}", min_value=0.0, value=None, label_visibility="collapsed")
    input_row(f"{hour}:00", hourly_hours[hour])

# 5. 其他分享
st.write("---")
notes = st.text_area("notes", value="", placeholder="备注信息...", label_visibility="collapsed")
st.write("其他分享")
st.markdown(f'<div style="margin-top:-10px;">', unsafe_allow_html=True)
notes
st.markdown('</div>', unsafe_allow_html=True)

# 6. 生成报告按钮
if st.button("生成报告", use_container_width=True):
    total_hours = sum([h for h in hourly_hours.values() if h is not None])
    today = datetime.date.today().strftime("%m/%d")
    
    report = f"{today}\n截止目前: {end_time}\n维修数量: {quantity}\n维修工时: {total_hours:.1f}\n维修效率: {(quantity/total_hours if total_hours>0 else 0):.2f}\n\n备注: {notes}"
    
    st.success("报告已生成！")
    st.code(report, language="text")
    st.info("长按上方文本即可复制发送")
