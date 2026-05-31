import streamlit as st
import datetime

# 1. 极简配置：隐藏头部菜单和水印，使其更像原生 App
st.set_page_config(page_title="维修助手", layout="centered")
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .stNumberInput {margin-top: -10px;}
    </style>
""", unsafe_allow_html=True)

st.title("维修效率助手")

# 2. 顶部基础信息
col_top1, col_top2 = st.columns(2)
with col_top1:
    quantity = st.number_input("总维修数量", min_value=0, value=0, step=1)
with col_top2:
    end_time = st.text_input("截止时间", value="22:00")

# 3. 紧凑型格状输入 (10-22点)
st.write("### 各时段工时")
hourly_hours = {}

# 循环生成每一行，时间左对齐，输入框右对齐
for hour in range(10, 23):
    col_l, col_r = st.columns([1, 2])
    with col_l:
        # 使用 markdown 调整文字间距，使其在垂直方向上与输入框对齐
        st.markdown(f"<br><div style='text-align: right; padding-right: 10px;'>{hour}</div>", unsafe_allow_html=True)
    with col_r:
        # 移除 step 参数让输入框更简洁，隐藏 label
        hourly_hours[hour] = st.number_input(
            f"{hour}", 
            min_value=0.0, 
            value=None, 
            label_visibility="collapsed"
        )

# 4. 生成报告按钮：全屏宽度，方便手指点击
if st.button("生成统计报告", use_container_width=True):
    total_hours = sum([h for h in hourly_hours.values() if h is not None])
    
    if total_hours > 0:
        efficiency = quantity / total_hours
        today = datetime.date.today().strftime("%m/%d")
        
        report = f"""
{today}
截止: {end_time}
维修数量: {quantity}
维修工时: {total_hours:.1f}
维修效率: {efficiency:.2f}
        """
        st.success("报告已生成！")
        st.code(report, language="text")
        st.info("长按上方文本即可复制")
    else:
        st.error("请填入至少一个时段的工时")
