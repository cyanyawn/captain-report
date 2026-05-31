import streamlit as st
import datetime

# 1. 极致精简配置
st.set_page_config(page_title="维修助手", layout="centered")

# 核心 CSS：强制一行显示，输入框固定大小
st.markdown("""
    <style>
    /* 强制所有容器内的元素水平对齐，不换行 */
    div[data-testid="column"] { display: flex !important; align-items: center !important; }
    
    /* 隐藏数字输入框的加减按钮 */
    div[data-testid="stNumberInput"] button { display: none !important; }
    
    /* 限制所有输入框的宽度，防止它们抢占全屏 */
    .stNumberInput, .stTextInput { width: 120px !important; }
    
    /* 强制垂直间距对齐 */
    div.stNumberInput { margin-top: -10px !important; }
    </style>
""", unsafe_allow_html=True)

st.title("维修效率助手")

# 2. 团队录入区域
# 即使是顶部输入，也手动控制布局，保持和下方表格一致
col_t1, col_t2 = st.columns([1, 2])
with col_t1: st.write("维修总数")
with col_t2: quantity = st.number_input("qty", value=0, label_visibility="collapsed")

col_t3, col_t4 = st.columns([1, 2])
with col_t3: st.write("截止时间")
with col_t4: end_time = st.text_input("time", value="22:00", label_visibility="collapsed")

st.write("---")
st.write("### 各时段工时")

hourly_hours = {}

# 3. 最稳定的行布局：每一行都强制是一个 col_left 和 col_right
for hour in range(10, 23):
    c1, c2 = st.columns([1, 2])
    with c1:
        st.write(f"**{hour}**")
    with c2:
        hourly_hours[hour] = st.number_input(
            f"h{hour}", min_value=0.0, value=None, label_visibility="collapsed"
        )

# 4. 大按钮，方便团队同事点击
if st.button("生成统计报告", use_container_width=True):
    total_hours = sum([h for h in hourly_hours.values() if h is not None])
    if total_hours > 0:
        efficiency = quantity / total_hours
        today = datetime.date.today().strftime("%m/%d")
        report = f"{today}\n截止: {end_time}\n数量: {quantity}\n工时: {total_hours:.1f}\n效率: {efficiency:.2f}"
        st.success("报告已生成！")
        st.code(report, language="text")
        st.info("长按上方文本复制发送")
    else:
        st.error("请填入至少一个时段的工时")
