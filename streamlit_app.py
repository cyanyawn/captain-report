import streamlit as st
import datetime

# 1. 强制移动端友好配置
st.set_page_config(page_title="维修助手", layout="centered")

# 核心 CSS：强制输入框不要全屏，且隐藏加减按钮
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    /* 隐藏加减按钮 */
    div[data-testid="stNumberInput"] button {display: none;}
    /* 约束输入框宽度，让它精致一点 */
    .stNumberInput {max-width: 150px;}
    </style>
""", unsafe_allow_html=True)

st.title("维修效率助手")

# 2. 顶部基础信息
quantity = st.number_input("总维修数量", min_value=0, value=0, step=1)
end_time = st.text_input("当前统计截止时间", value="22:00")

# 3. 紧凑型格状输入 (10-22点)
st.write("### 各时段工时")
hourly_hours = {}

for hour in range(10, 23):
    # 比例固定为 [1, 2]，时间在左，框在右
    col_l, col_r = st.columns([1, 2])
    with col_l:
        # 使用垂直间距调整，让数字和输入框对齐
        st.markdown(f"<br> **{hour}**", unsafe_allow_html=True)
    with col_r:
        # label_visibility="collapsed" 彻底隐藏标签
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
