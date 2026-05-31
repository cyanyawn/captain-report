import streamlit as st
import datetime

st.title("维修效率计算器")

# 输入区域
col1, col2 = st.columns(2)
with col1:
    quantity = st.number_input("维修数量", min_value=0)
with col2:
    hours = st.number_input("维修工时", min_value=0.1, format="%.2f")

# 计算与输出
if st.button("生成报告"):
    if hours > 0:
        efficiency = quantity / hours
        today = datetime.date.today().strftime("%m/%d")
        now = datetime.datetime.now().strftime("%H:%M")
        
        report = f"""
        {today}
        截止目前: {now}
        维修数量: {quantity}
        维修工时: {hours}
        维修效率: {efficiency:.2f}
        """
        st.success("报告已生成！")
        st.code(report, language="text")
        st.info("长按上方文本即可复制发送")
    else:
        st.error("工时不能为0哦")
