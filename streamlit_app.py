import streamlit as st
import datetime

# 1. 极简 UI 配置：隐藏多余内容
st.set_page_config(page_title="维修助手", layout="centered")
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .stNumberInput {margin-top: -10px;}
    </style>
""", unsafe_allow_html=True)

st.title("维修效率助手")

# 2. 基础信息：放在顶部，一行搞定
col_top1, col_top2 = st.columns(2)
with col_top1:
    quantity = st.number_input("总维修数量", min_value=0, value=0, step=1)
with col_top2:
    end_time = st.text_input("截止时间", value="22:00")

# 3. 紧凑型格状输入：这是最核心的部分，完全不需要下拉
st.write("### 各时段工时")
hourly_hours = {}

# 循环生成行，将时间与输入框放在同一行
for hour in range(10, 23):
    col_l, col_r = st.columns([1, 2])
    with col_l:
        st.markdown(f"**{hour}:00**")
    with col_r:
        # 这里移除 step 参数可以进一步减小输入框宽度
        hourly_hours[hour] = st.number_input(
            f"{hour}", 
            min_value=0.0, 
            value=None, 
            label_visibility="collapsed"
        )

# 4. 计算按钮：做成全屏宽度，方便手指点击
if st.button("生成报告", use_container_width=True):
    total_hours = sum([h for h in hourly_hours.values() if h is not None])
    if total_hours > 0:
        efficiency = quantity / total_hours
        today = datetime.date.today().strftime("%m/%d")
        report = f"{today}\n截止: {end_time}\n维修数量: {quantity}\n维修工时: {total_hours:.1f}\n效率: {efficiency:.2f}"
        st.success("报告已生成！")
        st.code(report, language="text")
    else:
        st.error("请填入工时")
