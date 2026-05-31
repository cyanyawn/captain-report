import streamlit as st
import datetime

st.title("维修效率计算器")

# 1. 维修数量
quantity = st.number_input("全天总维修数量", min_value=0, value=0, step=1)

# 2. 截止时间输入框
end_time = st.text_input("当前统计截止时间 (例如 22:00)", value="22:00")

# 3. 动态表格输入工时
st.write("### 请输入各时段工时")
hourly_hours = {}

col_time, col_input = st.columns([1, 2])

for hour in range(10, 23):
    with col_time:
        st.write(f"**{hour}:00**")
    with col_input:
        # 使用 label_visibility="collapsed" 去掉自带的标签，看起来更清爽
        # 默认值设为 None 可以让框变空，更符合直接输入的需求
        hourly_hours[hour] = st.number_input(f"{hour}点", min_value=0.0, value=None, step=0.1, label_visibility="collapsed")

# 4. 计算与输出
if st.button("生成报告"):
    # 将 None 转为 0 进行求和
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
