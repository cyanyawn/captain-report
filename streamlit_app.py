import streamlit as st
import datetime

# 隐藏右侧 Streamlit 默认菜单和水印，让它更像原生 App
st.set_page_config(page_title="维修助手", layout="centered")
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    div[data-testid="stNumberInput"] button {display: none;}
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

st.title("维修效率助手")

# 1. 顶部基础信息（单列）
quantity = st.number_input("全天总维修数量", min_value=0, value=0, step=1)
end_time = st.text_input("当前统计截止时间", value="22:00")

# 2. 紧凑单列列表输入
st.write("### 各时段工时")
hourly_hours = {}

# 使用循环生成 10-22 点的紧凑输入行
for hour in range(10, 23):
    # 用 columns 实现 左：时间，右：输入框 的单行对齐
    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown(f"<br> **{hour}:00**", unsafe_allow_html=True)
    with c2:
        hourly_hours[hour] = st.number_input(
            f"{hour}点", min_value=0.0, value=None, step=0.1, label_visibility="collapsed"
        )

# 3. 生成报告按钮（大按钮更适合手指点击）
if st.button("生成统计报告", use_container_width=True):
    total_hours = sum([h for h in hourly_hours.values() if h is not None])
    if total_hours > 0:
        efficiency = quantity / total_hours
        today = datetime.date.today().strftime("%m/%d")
        
        report = f"{today}\n截止目前: {end_time}\n维修数量: {quantity}\n维修工时: {total_hours:.1f}\n维修效率: {efficiency:.2f}"
        
        st.success("报告已生成！")
        st.code(report, language="text")
        st.info("长按上方文本即可复制")
    else:
        st.error("请至少输入一个时段的工时")
