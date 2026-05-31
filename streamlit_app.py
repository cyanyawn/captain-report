import streamlit as st
import datetime
import streamlit.components.v1 as components

# 1. 页面配置
st.set_page_config(page_title="维修报告生成工具", layout="centered")

# --- 初始化所有的状态变量 (用于清空数据) ---
if 'end_time' not in st.session_state: st.session_state.end_time = ""
if 'qty' not in st.session_state: st.session_state.qty = None
for h in range(10, 23):
    if f'h{h}' not in st.session_state: st.session_state[f'h{h}'] = None
if 'notes' not in st.session_state: st.session_state.notes = ""
if 'report_text' not in st.session_state: st.session_state.report_text = ""
if 'scroll_to_top' not in st.session_state: st.session_state.scroll_to_top = False

# --- 清空数据的回调函数 ---
def clear_form():
    st.session_state.end_time = ""
    st.session_state.qty = None
    for h in range(10, 23):
        st.session_state[f"h{h}"] = None
    st.session_state.notes = ""
    st.session_state.report_text = ""
    st.session_state.scroll_to_top = True # 触发回到顶部

# 如果刚刚点击了清空，执行回到顶部的动画
if st.session_state.scroll_to_top:
    scroll_top_js = """
    <script>
    setTimeout(function() {
        window.parent.scrollTo({top: 0, behavior: 'smooth'});
    }, 100);
    </script>
    """
    components.html(scroll_top_js, height=0)
    st.session_state.scroll_to_top = False # 重置状态

# 2. 强力 CSS：去留白、去提示、主次按钮样式、变绿反馈
st.markdown("""
    <style>
    /* 去除顶部留白 */
    header {display: none !important;}
    .block-container { padding-top: 1.5rem !important; }

    /* 隐藏右上角菜单和底部水印 */
    #MainMenu, footer {visibility: hidden;}
    .stApp {background-color: #FFFFFF;}
    
    /* 隐藏数字输入框右侧自带的加减号和回车提示 */
    div[data-testid="stNumberInput"] button { display: none !important; }
    div[data-testid="InputInstructions"] { display: none !important; }
    
    /* 标签字体 */
    label[data-testid="stWidgetLabel"] div {
        font-size: 15px !important;
        color: #000000 !important;
    }

    /* 强制所有按钮的外层容器居中 */
    div.element-container:has(div.stButton), div.stButton {
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
    }

    /* --- 主按钮：生成报告 --- */
    button[kind="primary"] {
        background-color: #dcf5d0 !important;
        color: #000000 !important;
        border: none !important;
        border-radius: 8px !important;
        width: 200px !important;
        height: 55px !important;
        margin: 10px auto 0 auto !important;
        display: block !important;
    }
    button[kind="primary"] p {
        font-weight: 900 !important; /* 极粗 */
        font-size: 22px !important; /* 放大字号 */
        margin: 0 !important;
    }
    button[kind="primary"]:hover {
        background-color: #c8e6bb !important;
    }

    /* --- 次按钮：清空数据 --- */
    button[kind="secondary"] {
        background-color: #f5f5f5 !important;
        color: #888888 !important;
        border: 1px solid #dddddd !important;
        border-radius: 8px !important;
        width: 200px !important;
        height: 45px !important;
        margin: 10px auto 0 auto !important;
        display: block !important;
    }
    button[kind="secondary"] p {
        font-weight: bold !important;
        font-size: 16px !important;
        margin: 0 !important;
    }
    button[kind="secondary"]:hover {
        background-color: #e8e8e8 !important;
        color: #333333 !important;
    }
    
    /* 填入内容后的绿色边框效果 */
    div[data-baseweb="input"].is-filled,
    div[data-baseweb="textarea"].is-filled {
        border-color: #4CAF50 !important;
        border-width: 2px !important;
        background-color: #F4FBF4 !important;
    }
    div[data-baseweb="input"].is-filled:focus-within,
    div[data-baseweb="textarea"].is-filled:focus-within {
        box-shadow: 0 0 0 1px #4CAF50 !important;
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

# 4. 表单输入区 (绑定了 key 以便清空)

# --- 截止时间 ---
st.markdown("<div style='font-size: 15px; font-weight: bold; color: #154A7F; margin-bottom: 5px;'>截止时间</div>", unsafe_allow_html=True)
st.text_input("截止时间", key="end_time", label_visibility="collapsed")

# --- 维修数量 ---
st.markdown("<div style='font-size: 15px; font-weight: bold; color: #154A7F; margin-bottom: 5px; margin-top: 15px;'>维修数量</div>", unsafe_allow_html=True)
st.number_input("维修数量", min_value=0, step=1, value=None, key="qty", label_visibility="collapsed")

# --- 维修工时 ---
st.markdown("<div style='font-size: 15px; font-weight: bold; color: #154A7F; margin-top: 25px; margin-bottom: 10px;'>维修工时</div>", unsafe_allow_html=True)

# 循环生成 10 到 22 的输入框
for hour in range(10, 23):
    st.number_input(str(hour), min_value=0.0, step=1.0, value=None, key=f"h{hour}")

# --- 其他分享 ---
st.markdown("<div style='font-size: 15px; font-weight: bold; color: #154A7F; margin-bottom: 5px; margin-top: 20px;'>其他分享</div>", unsafe_allow_html=True)
st.text_area("其他分享", key="notes", height=150, label_visibility="collapsed")

st.markdown("<hr>", unsafe_allow_html=True)

# 5. 生成报告逻辑
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    # 设置为 primary 主按钮
    generate_clicked = st.button("生成报告", type="primary")

if generate_clicked:
    # 处理截止时间格式
    formatted_time = st.session_state.end_time.strip()
    if formatted_time:
        if formatted_time.isdigit():
            formatted_time = f"{formatted_time}:00"
        elif "：" in formatted_time:
            formatted_time = formatted_time.replace("：", ":")
    
    # 计算总工时和效率
    total_hours = sum([st.session_state[f"h{h}"] for h in range(10, 23) if st.session_state[f"h{h}"] is not None])
    qty_val = st.session_state.qty
    eff = (qty_val / total_hours) if (qty_val is not None and total_hours > 0) else 0
    
    # 获取今天日期
    today = datetime.date.today().strftime("%m/%d")
    
    base_report = f"""{today}

截止时间：{formatted_time}
维修工时：{total_hours:.1f}
维修效率：{eff:.2f}"""

    notes_val = st.session_state.notes
    if notes_val.strip():
        st.session_state.report_text = base_report + f"\n\n分享：\n{notes_val}"
    else:
        st.session_state.report_text = base_report

# 6. 显示报告、复制按钮 和 清空按钮
if st.session_state.report_text:
    # 埋入一个不可见的锚点，用于自动滚动定位
    st.markdown("<div id='report_target'></div>", unsafe_allow_html=True)
    
    if generate_clicked:
        scroll_down_js = """
        <script>
        setTimeout(function() {
            var target = window.parent.document.getElementById('report_target');
            if (target) {
                target.scrollIntoView({behavior: 'smooth', block: 'start'});
            }
        }, 100);
        </script>
        """
        components.html(scroll_down_js, height=0)

    # 显示报告文本
    report_display = st.session_state.report_text.replace('\n', '<br>')
    st.markdown(f"<div style='font-size:14px; line-height:1.6; color:#000;'>{report_display}</div>", unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # 注入 HTML 复制按钮 (带 readonly 防键盘弹出)
    html_code = f"""
    <div style="padding: 5px 0; display: flex; justify-content: center; width: 100%;">
        <textarea id="hiddenText" readonly style="position:absolute; left:-9999px;">{st.session_state.report_text}</textarea>
        <button onclick="copyToClipboard()" style="background-color: #f8cbcc; color: black; font-weight: bold; border: none; border-radius: 8px; width: 200px; height: 50px; font-size: 18px; cursor: pointer; font-family: sans-serif;">点击复制报告内容</button>
    </div>
    <script>
    function copyToClipboard() {{
        var copyText = document.getElementById("hiddenText");
        copyText.select();
        copyText.setSelectionRange(0, 99999); 
        document.execCommand("copy");
        
        var btn = document.querySelector("button");
        var originalText = btn.innerText;
        btn.innerText = "复制成功！";
        btn.style.backgroundColor = "#dcf5d0"; 
        setTimeout(function(){{ 
            btn.innerText = originalText; 
            btn.style.backgroundColor = "#f8cbcc"; 
        }}, 2000);
    }}
    </script>
    """
    components.html(html_code, height=80)
    
    # --- 新增：清空数据按钮 ---
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True) # 稍微加点间距
    col_clear1, col_clear2, col_clear3 = st.columns([1, 2, 1])
    with col_clear2:
        # 设置为 secondary 次按钮，并绑定清空回调函数
        st.button("清空数据", type="secondary", on_click=clear_form)

# 7. 注入全局前端魔法脚本 (变绿 + 回车跳跃)
magic_js = """
<script>
const doc = window.parent.document;

function enhanceInputs() {
    const inputs = Array.from(doc.querySelectorAll('input:not([type="hidden"]), textarea'));
    
    inputs.forEach((input, index) => {
        // 1. 改变 iOS 键盘的 "换行" 按钮为 "下一项" (Next)
        if (index < inputs.length - 1) {
            input.setAttribute('enterkeyhint', 'next');
        } else {
            input.setAttribute('enterkeyhint', 'done');
        }

        // 2. 检查是否有值，如果有值就加上 'is-filled' 的 CSS 类让它变绿
        const wrapper = input.closest('div[data-baseweb="input"]') || input.closest('div[data-baseweb="textarea"]');
        if (wrapper) {
            if (input.value && input.value.trim() !== '') {
                wrapper.classList.add('is-filled');
            } else {
                wrapper.classList.remove('is-filled');
            }
        }
    });
}

// 每半秒检查一次状态
setInterval(enhanceInputs, 500);
doc.body.addEventListener('input', enhanceInputs);

// 3. 监听回车键 (Enter)
doc.body.addEventListener('keydown', function(e) {
    if (e.key === 'Enter') {
        if (e.target.tagName === 'INPUT') {
            e.preventDefault(); 
            const inputs = Array.from(doc.querySelectorAll('input:not([type="hidden"]), textarea'));
            const currentIndex = inputs.indexOf(e.target);
            
            if (currentIndex > -1 && currentIndex < inputs.length - 1) {
                inputs[currentIndex + 1].focus();
            } else {
                e.target.blur();
            }
        }
    }
}, true);
</script>
"""
components.html(magic_js, height=0)
