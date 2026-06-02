import streamlit as st
import datetime
import streamlit.components.v1 as components

# 1. 页面配置
st.set_page_config(page_title="预计维修数量工具", layout="centered")

# 2. 强力 CSS：隐藏多余元素，优化文本框外观
st.markdown("""
    <style>
    /* 去除顶部留白 */
    header {display: none !important;}
    .block-container { padding-top: 1.5rem !important; padding-bottom: 2rem !important; }

    /* 隐藏右上角菜单、底部水印和部署按钮 */
    #MainMenu, footer {visibility: hidden !important; display: none !important;}
    .stDeployButton {display: none !important;}
    [data-testid="stDeployButton"] {display: none !important;}
    div[class*="viewerBadge"] {display: none !important;}
    
    .stApp {background-color: #FFFFFF;}
    
    /* 隐藏输入框的回车提示和加减号 */
    div[data-testid="InputInstructions"] { display: none !important; }
    div[data-testid="stNumberInput"] button { display: none !important; }
    
    /* 标签字体 */
    label[data-testid="stWidgetLabel"] div {
        font-size: 15px !important;
        font-weight: bold !important;
        color: #154A7F !important;
    }
    
    .subtitle {
        font-size: 12px;
        color: #888888;
        font-weight: normal;
    }

    /* --- 按钮样式 --- */
    div.stButton {
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
    }

    /* 主按钮：计算 (紫色) */
    button[kind="primary"] {
        background-color: #E8E2F8 !important;
        color: #4A3082 !important;
        font-weight: 900 !important;
        font-size: 20px !important;
        border: 1px solid #D1C4E9 !important;
        border-radius: 8px !important;
        width: 100% !important;
        height: 55px !important;
        margin-top: 10px !important;
        display: block !important;
    }
    button[kind="primary"]:hover {
        background-color: #D1C4E9 !important;
    }

    /* 次按钮：刷新 (灰色) */
    button[kind="secondary"] {
        background-color: #f5f5f5 !important;
        color: #888888 !important;
        font-weight: bold !important;
        font-size: 16px !important;
        border: 1px solid #dddddd !important;
        border-radius: 8px !important;
        width: 200px !important;
        height: 45px !important;
        margin: 10px auto 0 auto !important;
        display: block !important;
    }
    button[kind="secondary"]:hover {
        background-color: #e8e8e8 !important;
        color: #333333 !important;
    }

    /* --- 看板样式 --- */
    .prediction-card {
        background: linear-gradient(135deg, #F4F0FF 0%, #E8E2F8 100%);
        border: 1px solid #D1C4E9;
        border-radius: 12px;
        padding: 15px;
        margin-top: 20px;
        color: #4A3082;
        box-shadow: 0 4px 12px rgba(74, 48, 130, 0.08);
    }
    .pred-title {
        font-size: 16px;
        font-weight: 900;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .live-badge {
        font-size: 12px;
        background-color: #4CAF50;
        color: white;
        padding: 2px 8px;
        border-radius: 12px;
    }
    .pred-data-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
        font-size: 15px;
    }
    .pred-highlight {
        font-size: 18px;
        font-weight: 900;
        color: #6200EE;
    }
    .pred-note {
        font-size: 12px;
        color: #7E6BC4;
        margin-top: 10px;
        text-align: right;
    }
    hr.dashed {
        border-top: 1px dashed #D1C4E9;
        margin: 12px 0;
    }
    
    /* 填入内容后的绿色边框效果 (保留微交互) */
    div[data-baseweb="input"].is-filled {
        border-color: #4CAF50 !important;
        border-width: 2px !important;
        background-color: #F4FBF4 !important;
    }
    div[data-baseweb="input"].is-filled:focus-within {
        box-shadow: 0 0 0 1px #4CAF50 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 核心魔法：创建全局共享数据存储
@st.cache_resource
def get_shared_data():
    return {
        "close_time": "22",
        "efficiency": "40",
        "wait_qty": "",
        "repairing_qty": "",
        "hours": {h: "" for h in range(10, 23)},
        "show_dashboard": False
    }

shared_data = get_shared_data()

# 辅助函数：安全地将字符串转为浮点数
def safe_float(val, default=0.0):
    if not val: return default
    try:
        return float(val)
    except ValueError:
        return default

# 4. 标题区
st.markdown("<h1>预计维修数量工具 V1.0</h1>", unsafe_allow_html=True)
st.markdown("<hr style='margin-top: -10px; border-top: 1px solid #d3d3d3;'>", unsafe_allow_html=True)

# 5. 表单输入区 (使用 text_input 替代 number_input，默认值设为空字符串)

st.markdown("关店时间 <span class='subtitle'>(支持半小时，如 22.5)</span>", unsafe_allow_html=True)
shared_data["close_time"] = st.text_input("close_time", value=shared_data["close_time"], label_visibility="collapsed", placeholder="例如: 22.5")

st.markdown("维修工时排班 <span class='subtitle'>(随时可加减修改)</span>", unsafe_allow_html=True)
for h in range(10, 23):
    val = st.text_input(f"{h}:00", value=shared_data["hours"][h], placeholder=f"{h}:00", label_visibility="collapsed")
    shared_data["hours"][h] = val

st.markdown("当前等待维修数量 <span class='subtitle'>(积压排队的设备数)</span>", unsafe_allow_html=True)
shared_data["wait_qty"] = st.text_input("wait_qty", value=shared_data["wait_qty"], label_visibility="collapsed", placeholder="请输入等待数量")

st.markdown("当前正在维修数量 <span class='subtitle'>(操作台上的设备数)</span>", unsafe_allow_html=True)
shared_data["repairing_qty"] = st.text_input("repairing_qty", value=shared_data["repairing_qty"], label_visibility="collapsed", placeholder="请输入正在维修数量")

st.markdown("单台维修耗时 <span class='subtitle'>(分钟/台)</span>", unsafe_allow_html=True)
shared_data["efficiency"] = st.text_input("efficiency", value=shared_data["efficiency"], label_visibility="collapsed", placeholder="例如: 40")

# 6. 按钮与计算逻辑
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    generate_clicked = st.button("计算", type="primary")

if generate_clicked:
    shared_data["show_dashboard"] = True

# 7. 渲染实时看板
if shared_data["show_dashboard"]:
    # 埋入一个不可见的锚点，用于自动滚动定位
    st.markdown("<div id='report_target'></div>", unsafe_allow_html=True)
    
    # 生成后自动滑到下方
    if generate_clicked:
        st.markdown(
            """<img src="x" onerror="setTimeout(function(){var t=window.parent.document.getElementById('report_target'); if(t){t.scrollIntoView({behavior: 'smooth', block: 'start'});}}, 100);" style="display:none;">""",
            unsafe_allow_html=True
        )

    close_hour = safe_float(shared_data["close_time"], 22.0)
    mins_per_device = safe_float(shared_data["efficiency"], 40.0)
    if mins_per_device <= 0: mins_per_device = 40.0 # 防呆
    
    current_hour = datetime.datetime.now().hour
    start_hour = max(10, current_hour)
    
    remaining_hours = 0.0
    if start_hour < close_hour:
        max_box_hour = min(22, int(close_hour))
        for i in range(start_hour, max_box_hour + 1):
            remaining_hours += safe_float(shared_data["hours"][i])
            
    wait_qty = int(safe_float(shared_data["wait_qty"]))
    repairing_qty = int(safe_float(shared_data["repairing_qty"]))
    
    total_capacity = int(remaining_hours / (mins_per_device / 60))
    can_accept = total_capacity - wait_qty - repairing_qty
    
    # 格式化时间显示
    close_hour_display = int(close_hour)
    close_min_display = "30" if close_hour % 1 == 0.5 else "00"
    end_time_str = f"{close_hour_display}:{close_min_display}"
    
    # 颜色和警告逻辑
    accept_color = "#FF3B30" if can_accept < 0 else "#6200EE"
    accept_display = 0 if can_accept < 0 else can_accept
    
    warning_html = f"""<div class="pred-note" style="color: #FF3B30;">⚠️ 警告：当前任务已超出剩余产能 {abs(can_accept)} 台！</div>""" if can_accept < 0 else f"""<div class="pred-note">* 按单台耗时 {int(mins_per_device)} 分钟计算</div>"""

    # 渲染卡片 HTML
    card_html = f"""
    <div class="prediction-card">
        <div class="pred-title">
            <span>⏱️ 实时产能看板</span>
            <span class="live-badge">全组共享中</span>
        </div>
        <div class="pred-data-row">
            <span>从 <strong>{start_hour}:00</strong> 到 <strong>{end_time_str}</strong> 剩余工时：</span>
            <span><span class="pred-highlight">{remaining_hours:.1f}</span> h</span>
        </div>
        <div class="pred-data-row">
            <span>剩余工时总产能：</span>
            <span><span class="pred-highlight">{total_capacity}</span> 台</span>
        </div>
        <div class="pred-data-row">
            <span>减去当前等待维修：</span>
            <span><span class="pred-highlight" style="color: #FF3B30;">{wait_qty}</span> 台</span>
        </div>
        <div class="pred-data-row">
            <span>减去当前正在维修：</span>
            <span><span class="pred-highlight" style="color: #FF3B30;">{repairing_qty}</span> 台</span>
        </div>
        <hr class="dashed">
        <div class="pred-data-row" style="font-size: 18px; font-weight: bold;">
            <span>✨ 还可以接入新单：</span>
            <span><span class="pred-highlight" style="font-size: 24px; color: {accept_color};">{accept_display}</span> 台</span>
        </div>
        {warning_html}
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

# 8. 刷新/清空按钮
def clear_data():
    shared_data["wait_qty"] = ""
    shared_data["repairing_qty"] = ""
    for h in range(10, 23):
        shared_data["hours"][h] = ""
    shared_data["show_dashboard"] = False

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
col_clear1, col_clear2, col_clear3 = st.columns([1, 2, 1])
with col_clear2:
    if st.button("刷新页面重置", type="secondary"):
        clear_data()
        st.rerun()

# 9. 注入全局前端魔法脚本 (变绿 + 回车跳跃 + 强制隐藏右下角徽章)
magic_js = """
<script>
const doc = window.parent.document;

// --- 徽章杀手：暴力隐藏右下角的头像和红船 ---
function killBadge() {
    const badges = doc.querySelectorAll('[class*="viewerBadge"], [class*="styles_viewerBadge"]');
    badges.forEach(b => {
        b.style.display = 'none';
        b.style.opacity = '0';
        b.style.visibility = 'hidden';
    });
    
    const allDivs = doc.querySelectorAll('div');
    allDivs.forEach(div => {
        const style = window.getComputedStyle(div);
        if (style.position === 'fixed' && style.bottom !== 'auto' && style.right !== 'auto') {
            if (div.innerHTML.includes('svg') || div.innerHTML.includes('img')) {
                div.style.display = 'none';
            }
        }
    });
}

function enhanceInputs() {
    killBadge();

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

killBadge();
setInterval(enhanceInputs, 500);
doc.body.addEventListener('input', enhanceInputs);

// 3. 监听回车键 (Enter) 拦截刷新，实现 Next 连点！
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
