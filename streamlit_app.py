import streamlit as st
import datetime

# 1. 极简配置
st.set_page_config(page_title="维修助手", layout="centered")

# 2. 核心 CSS：强制 Grid 布局，完美锁定位置
st.markdown("""
    <style>
    /* 隐藏多余 UI */
    #MainMenu, footer, header {visibility: hidden;}
    
    /* 定义网格：左列 50px，右列 120px，死锁在同一行 */
    .grid-container {
        display: grid !important;
        grid-template-columns: 50px 120px !important;
        align-items: center !important;
        gap: 10px !important;
        margin-bottom: 10px !important;
    }
    
    /* 隐藏数字加减按钮 */
    div[data-testid="stNumberInput"] button {display: none;}
    
    /* 强制输入框宽度与高度 */
    .stNumberInput, .stTextInput {
        width: 120px !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("维修效率助手")

# 3. 顶部输入也统一使用 Grid
st.markdown('<div class="grid-container"><div>数量</div><div>', unsafe_allow_html=True)
quantity = st.number_input("qty", value=0, label_visibility="collapsed")
st.markdown('</div></div>', unsafe_allow_html=True)

st.markdown('<div class="grid-container"><div>截止</div><div>', unsafe_allow_html=True)
end_time = st.text_input("time", value="22:00", label_visibility="collapsed")
st.markdown('</div></div>', unsafe_allow_html=True)

st.write("---")

# 4. 循环生成每一行，全部包裹在 grid-container 中
for hour in range(10, 23):
    st.markdown(f'<div class="grid-container"><div>{hour}</div><div>', unsafe_allow_html=True)
    st.number_input(f"h{hour}", min_value=0.0, value=None, label_visibility="collapsed")
    st.markdown('</div></div>', unsafe_allow_html=True)

# 5. 生成报告按钮
if st.button("生成报告", use_container_width=True):
    # 这里建议在 GitHub 里的逻辑保持不变即可
    st.success("成功")
