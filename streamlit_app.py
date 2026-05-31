import streamlit as st
import datetime

# 极致精简配置
st.set_page_config(page_title="维修助手", layout="centered")
st.markdown("""<style>
    #MainMenu, footer, header {visibility: hidden;}
    div[data-testid="stTextInput"] {margin-bottom: -15px;}
</style>""", unsafe_allow_html=True)

st.title("维修效率助手")

# 1. 顶部基础信息
quantity = st.text_input("全天总维修数量", value="0")
end_time = st.text_input("当前统计截止时间", value="22:00")

# 2. 紧凑输入列表 (用 text_input 模拟数字输入，响应速度更快)
st.write("### 各时段工时")
hourly_hours = {}

for hour in range(10, 23):
    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown(f"<br> **{hour}:00**", unsafe_allow_html=True)
    with c2:
        # 使用 key 属性，这能帮助浏览器更好地管理焦点
        val = st.text_input(f"h{hour}", value="", label_visibility="collapsed")
        hourly_hours[hour] = float(val) if val.replace('.','',1).isdigit() else 0.0

# 3. 统计
if st.button("生成统计报告", use_container_width=True):
    total_hours = sum(hourly_hours.values())
    efficiency = float(quantity) / total_hours if total_hours > 0 else 0
    today = datetime.date.today().strftime("%m/%d")
    report = f"{today}\n截止: {end_time}\n数量: {quantity}\n工时: {total_hours:.1f}\n效率: {efficiency:.2f}"
    st.success("报告已生成！")
    st.code(report, language="text")
