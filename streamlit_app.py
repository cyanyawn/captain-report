import streamlit as st
import datetime

# 1. 极致精简配置
st.set_page_config(page_title="维修助手", layout="centered")

# 核心 CSS：强制一行显示，并统一输入框大小
st.markdown("""
    <style>
    /* 隐藏顶部菜单、水印 */
    #MainMenu, footer, header {visibility: hidden;}
    
    /* 强制：让每一行变成 Flex 布局，时间在左，输入框在右 */
    div[data-testid="column"] {
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    /* 隐藏加减按钮 */
    div[data-testid="stNumberInput"] button {display: none;}
    
    /* 统一输入框宽度：包括总维修数量、截止时间、时段工时 */
    .stNumberInput, .stTextInput {
        max-width: 120px !important;
        margin-top: -15px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("维修效率助手")

# 2. 顶部基础信息 (手动控制对齐)
c_qty1, c_qty2 = st.columns([1, 2])
with c_qty1: st.write("总维修数量")
with c_qty2: quantity = st.number_input("qty", value=0, label_visibility="collapsed")

c_time1, c_time2 = st.columns([1, 2])
with c_time1: st.write("截止时间")
with c_time2: end_time = st.text_input("time", value="22:00", label_visibility="collapsed")

# 3. 紧凑型格状输入 (10-22点)
st.write("---")
st.write("### 各时段工时")
hourly_hours = {}

for hour in range(10, 23):
    col_l, col_r = st.columns([1, 2])
    with col_l:
        st.write(f"**{hour}**")
    with col_r:
        hourly_hours[hour] = st.number_input(
            f"{hour}", 
            min_value=0.0, 
            value=None, 
            label_visibility="collapsed"
        )

# 4. 生成报告按钮
if st.button("生成统计报告", use_container_width=True):
    total_hours = sum([h for h in hourly_hours.values() if h is not None])
    if total_hours > 0:
        efficiency = quantity / total_hours
        today = datetime.date.today().strftime("%m/%d")
        report = f"{today}\n截止: {end_time}\n数量: {quantity}\n工时: {total_hours:.1f}\n效率: {efficiency:.2f}"
        st.success("报告已生成！")
        st.code(report, language="text")
    else:
        st.error("请填入至少一个时段的工时")
