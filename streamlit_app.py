import streamlit as st
import datetime

st.title("维修效率计算器")

# 1. 维修数量输入
quantity = st.number_input("全天总维修数量", min_value=0, value=0, step=1)

# 2. 截止时间输入
end_time = st.text_input("当前统计截止时间 (例如 22:00)", value="22:00")

# 3. 表格化布局：每一行对应一个小时和输入框
st.write("### 请输入各时段工时")
hourly_hours = {}

# 循环生成每一行，确保时间与输入框并排对齐
for hour in range(10, 23):
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(f"<br> **{hour}:00**", unsafe_allow_html=True)
    with col2:
        # 使用 label_visibility="collapsed" 让输入框紧凑
        hourly_hours[hour] = st.number_input(
            f"{hour}点工时", 
            min_value=0.0, 
            value=None, 
            step=0.1, 
            label_visibility="collapsed"
        )

# 4. 计算逻辑
if st.button("生成报告"):
    # 过滤掉 None 值，只计算有填写的工时
    total_hours = sum([h for h in hourly_hours.values() if h is not None])
    
    if total_hours > 0:
        efficiency = quantity / total_hours
        today = datetime.date.today().strftime("%m/%d")
        
        report = f"""
{today}
截止目前: {end_time}
维修数量: {quantity}
维修工时: {total_hours:.1f}
维修效率: {efficiency:.2f}
        """
        st.success("报告已生成！")
        st.code(report, language="text")
        st.info("长按上方文本即可复制发送")
    else:
        st.error("请至少输入一个时段的工时哦")
