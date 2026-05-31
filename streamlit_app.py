import streamlit as st
import datetime

# 1. 极致精简配置
st.set_page_config(page_title="维修助手", layout="centered")

# 核心 CSS：强制一行显示，输入框固定 100px
st.markdown("""
    <style>
    /* 隐藏多余 UI */
    #MainMenu, footer, header {visibility: hidden;}
    
    /* 强制每一行容器使用 Flex 布局，且不换行 */
    .row-container {
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        justify-content: flex-start !important;
        gap: 10px !important;
        margin-bottom: 5px !important;
    }
    
    /* 强制输入框和文字宽度 */
    .time-label { width: 40px !important; font-weight: bold; }
    .stNumberInput { width: 120px !important; }
    div[data-testid="stNumberInput"] button {display: none;}
    </style>
""", unsafe_allow_html=True)

st.title("维修效率助手")

# 2. 顶部输入
quantity = st.number_input("总维修数量", min_value=0, value=0, step=1)
end_time = st.text_input("截止时间", value="22:00")

# 3. 紧凑型格状输入 (10-22点)
st.write("---")
st.write("### 各时段工时")
hourly_hours = {}

for hour in range(10, 23):
    # 使用自定义的 container 来包装每一行
    with st.container():
        st.markdown(f'<div class="row-container">', unsafe_allow_html=True)
        # 用两列实现
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown(f'<div class="time-label">{hour}</div>', unsafe_allow_html=True)
        with col2:
            hourly_hours[hour] = st.number_input(
                f"h{hour}", 
                min_value=0.0, 
                value=None, 
                label_visibility="collapsed"
            )
        st.markdown('</div>', unsafe_allow_html=True)

# 4. 按钮
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
