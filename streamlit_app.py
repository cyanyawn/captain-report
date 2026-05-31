import streamlit as st
import datetime
import streamlit.components.v1 as components

# 1. 页面配置
st.set_page_config(page_title="维修报告生成工具", layout="centered")

# 2. 强力 CSS：去留白、去提示、大字号按钮
st.markdown("""
    <style>
    /* --- 核心修改：去除顶部留白 --- */
    header {display: none !important;}
    .block-container {
        padding-top: 1.5rem !important;
    }

    /* 隐藏右上角菜单和底部水印 */
    #MainMenu, footer {visibility: hidden;}
    .stApp {background-color: #FFFFFF;}
    
    /* 隐藏数字输入框右侧自带的加减号 */
    div[data-testid="stNumberInput"] button { 
        display: none !important; 
    }
    
    /* --- 核心修改：隐藏 "Press Enter to apply" 提示 --- */
    div[data-testid="InputInstructions"] {
        display: none !important;
    }
    
    /* 调整默认标签(如10, 11等)的字体颜色和大小，保持黑色不加粗 */
    label[data-testid="stWidgetLabel"] div {
        font-size: 15px !important;
        color: #000000 !important;
    }

    /* 强制生成报告按钮的外层容器居中 */
    div.element-container:has(div.stButton),
    div.stButton {
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
    }

    /* 生成报告按钮外框样式 (浅绿色) */
    div.stButton > button {
        background-color: #dcf5d0 !important;
        color: #000000 !important;
        border: none !important;
        border-radius: 8px !important;
        width: 200px !important;
        height: 55px !important; /* 稍微加高一点点以适应大字 */
        margin: 10px auto 0 auto !important;
        display: block !important;
    }
    
    /* --- 核心修改：按钮文字加粗、变大 --- */
    div.stButton > button p {
        font-weight: 900 !important; /* 极粗 */
        font-size: 22px !important; /* 放大两个字号 */
        margin: 0 !important;
    }

    div.stButton > button:hover {
        background-color: #c8e6bb !important;
    }
    
    /* 自定义分割线样式 */
    hr {
        border-top: 1px solid #d3d3d3;
        margin: 25px 0;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 标题区
st.markdown("<h1>维修报告生成工具 V1.0</h1>", unsafe_allow_html=True)
st.markdown("<hr style='margin-top: -10px;'>", unsafe_allow_html=True)

# 4. 表单输入区

# --- 截止时间 ---
st.markdown("<div style='font-size: 15px; font-weight: bold; color: #154A7F; margin-bottom: 5px;'>截止时间</div>", unsafe_allow_html=True)
end_time = st.text_input("截止时间", value="", label_visibility="collapsed")

# --- 维修数量 ---
st.markdown("<div style='font-size: 15px; font-weight: bold; color: #154A7F; margin-bottom: 5px; margin-top: 15px;'>维修数量</div>", unsafe_allow_html=True)
qty = st.number_input("维修数量", min_value=0, step=1, value=None, label_visibility="collapsed")

# --- 维修工时 ---
st.markdown("<div style='font-size: 15px; font-weight: bold; color: #154A7F; margin-top: 25px; margin-bottom: 10px;'>维修工时</div>", unsafe_allow_html=True)

# 循环生成 10 到 22 的输入框 (这些保持黑色正常字体)
hourly_hours = {}
for hour in range(10, 23):
    hourly_hours[hour] = st.number_input(str(hour), min_value=0.0, step=1.0, value=None, key=f"h{hour}")

# --- 其他分享 ---
st.markdown("<div style='font-size: 15px; font-weight: bold; color: #154A7F; margin-bottom: 5px; margin-top: 20px;'>其他分享</div>", unsafe_allow_html=True)
notes = st.text_area("其他分享", value="", height=150, label_visibility="collapsed")

st.markdown("<hr>", unsafe_allow_html=True)

# 5. 生成报告逻辑
if 'report_text' not in st.session_state:
    st.session_state.report_text = ""

# 物理居中布局
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    generate_clicked = st.button("生成报告")

if generate_clicked:
    # --- 处理截止时间格式 ---
    formatted_time = end_time.strip()
    if formatted_time:
        # 如果用户输入的是纯数字（比如 "12"），自动加上 ":00"
        if formatted_time.isdigit():
            formatted_time = f"{formatted_time}:00"
        # 如果用户不小心输入了中文冒号，自动替换为英文冒号
        elif "：" in formatted_time:
            formatted_time = formatted_time.replace("：", ":")
    
    # 计算总工时和效率
    total_hours = sum([h for h in hourly_hours.values() if h is not None])
    eff = (qty / total_hours) if (qty is not None and total_hours > 0) else 0
    
    # 获取今天日期，格式如 05/31
    today = datetime.date.today().strftime("%m/%d")
    
    # 先组装基础部分 (使用处理过的时间 formatted_time)
    base_report = f"""{today}

截止时间：{formatted_time}
维修工时：{total_hours:.1f}
维修效率：{eff:.2f}"""

    # 智能判断：如果 notes 里面有内容（去除空格后不为空），才加上分享部分
    if notes.strip():
        st.session_state.report_text = base_report + f"\n\n分享：\n{notes}"
    else:
        st.session_state.report_text = base_report

# 6. 显示报告和粉色复制按钮
if st.session_state.report_text:
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # 将换行符替换为 HTML 的 <br> 以便在网页中正确显示文本
    report_display = st.session_state.report_text.replace('\n', '<br>')
    st.markdown(f"<div style='font-size:14px; line-height:1.6; color:#000;'>{report_display}</div>", unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # 注入一段 HTML 和 JavaScript 来实现“浅粉色复制按钮”，并居中
    html_code = f"""
    <div style="padding: 5px 0; display: flex; justify-content: center; width: 100%;">
        <textarea id="hiddenText" style="position:absolute; left:-9999px;">{st.session_state.report_text}</textarea>
        <button onclick="copyToClipboard()" style="background-color: #f8cbcc; color: black; font-weight: bold; border: none; border-radius: 8px; width: 200px; height: 50px; font-size: 18px; cursor: pointer; font-family: sans-serif;">点击复制报告内容</button>
    </div>
    <script>
    function copyToClipboard() {{
        var copyText = document.getElementById("hiddenText");
        copyText.select();
        copyText.setSelectionRange(0, 99999); // 兼容手机端
        document.execCommand("copy");
        
        // 复制成功后的按钮反馈效果
        var btn = document.querySelector("button");
        var originalText = btn.innerText;
        btn.innerText = "复制成功！";
        btn.style.backgroundColor = "#dcf5d0"; // 成功后短暂变成浅绿色
        setTimeout(function(){{ 
            btn.innerText = originalText; 
            btn.style.backgroundColor = "#f8cbcc"; // 恢复粉色
        }}, 2000);
    }}
    </script>
    """
    components.html(html_code, height=80)
