import streamlit as st
import datetime

st.set_page_config(layout="wide") # 使用宽屏模式，让一行能放更多内容
st.title("维修效率助手")

# 1. 顶部基础信息
col_a, col_b = st.columns(2)
with col_a:
    quantity = st.number_input("总维修数量", min_value=0, value=0, step=1)
with col_b:
    end_time = st.text_input("截止时间", value="22:00")

# 2. 紧凑型表格布局 (3列，让它在一屏内显示完)
st.write("### 各时段工时 (输入后按回车跳转)")
hourly_hours = {}
cols = st.columns(3) # 每行显示3个点，节省空间

for i, hour in enumerate(range(10, 23)):
    with cols[i % 3]:
        # 使用 label_visibility="visible" 把时间放在输入框上方，极度节省高度
        hourly_hours[hour] = st.number_input(
            f"{hour}:00", 
            min_value=0.0, 
            value=None, 
            step=0.1
        )

# 3. 计算逻辑
if st.button("生成报告", use_container_width=True):
    total_hours = sum([h for h in hourly_hours.values() if h is not None])
    if total_hours > 0:
        efficiency = quantity / total_hours
        today = datetime.date.today().strftime("%m/%d")
        report = f"{today}\n截止目前: {end_time}\n维修数量: {quantity}\n维修工时: {total_hours:.1f}\n维修效率: {efficiency:.2f}"
        st.success("生成成功！")
        st.code(report, language="text")
    else:
        st.error("请至少输入一个工时")
