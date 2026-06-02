import streamlit as st
import datetime
import streamlit.components.v1 as components

# 1. 页面配置
st.set_page_config(page_title="预计维修数量工具", layout="centered")

# 2. 强力 CSS
st.markdown("""
    <style>
    header {display: none !important;}
    .block-container { padding-top: 1.5rem !important; padding-bottom: 2rem !important; }
    #MainMenu, footer {visibility: hidden !important; display: none !important;}
    .stDeployButton {display: none !important;}
    [data-testid="stDeployButton"] {display: none !important;}
    div[class*="viewerBadge"] {display: none !important;}
    .stApp {background-color: #FFFFFF;}
    div[data-testid="InputInstructions"] { display: none !important; }
    
    label[data-testid="stWidgetLabel"] div {
        font-size: 15px !important;
        font-weight: bold !important;
        color: #154A7F !important;
    }
    .subtitle { font-size: 12px; color: #888888; font-weight: normal; }

    div.stButton { display: flex !important; justify-content: center !important; width: 100% !important; }

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
        transition: all 0.15s ease !important; 
    }
    button[kind="primary"]:hover { background-color: #D1C4E9 !important; }
    button[kind="primary"]:active { 
        transform: scale(0.95) !important; 
        box-shadow: inset 0 3px 5px rgba(0,0,0,0.1) !important; 
        opacity: 0.8 !important;
    }

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
    .pred-data-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
        font-size: 15px;
    }
    .pred-highlight { font-size: 18px; font-weight: 900; color: #6200EE; }
    .pred-note { font-size: 12px; color: #7E6BC4; margin-top: 10px; text-align: right; }
    hr.dashed { border-top: 1px dashed #D1C4E9; margin: 12px 0; }
    
    div[data-baseweb="input"].is-filled {
        border-color: #4CAF50 !important;
        border-width: 2px !important;
        background-color: #F4FBF4 !important;
    }
    div[data-baseweb="input"].is-filled:focus-within { box-shadow: 0 0 0 1px #4CAF50 !important; }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------
# 3. 核心架构：全队共享数据
# -----------------------------------------
@st.cache_resource
def get_shared_data():
    return {
        "is_active": False,
        "close_time": "22",
        "efficiency": "40",
        "wait_qty": "",
        "repairing_qty": "",
        "hours": {h: "" for h in range(10, 23)},
        "updater_name": "",
        "update_time": ""
    }

shared_data = get_shared_data()

def safe_float(val, default=0.0):
    if not val: return default
    try: return float(val)
    except ValueError: return default

# -----------------------------------------
# 4. 极简密码验证系统 (带 LocalStorage 记忆)
# -----------------------------------------
# 注入一段 JS，用于读取本地浏览器的密码记忆
auth_check_js = """
<script>
    const doc = window.parent.document;
    if (localStorage.getItem('captain_auth') === '1984') {
        // 如果本地存了正确的密码，给 Streamlit 传一个隐藏信号
        let hiddenInput = doc.getElementById('auth_signal');
        if (hiddenInput && hiddenInput.value !== 'passed') {
            hiddenInput.value = 'passed';
            hiddenInput.dispatchEvent(new Event('input', { bubbles: true }));
        }
    }
</script>
"""
components.html(auth_check_js, height=0)

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# 接收 JS 传来的免密登录信号
auth_signal = st.text_input("auth_signal", key="auth_signal", label_visibility="collapsed", disabled=True)
if auth_signal == 'passed':
    st.session_state.authenticated = True

# 强制隐藏这个信号输入框
st.markdown("""<style>div[data-testid="stTextInput"]:has(input[aria-label="auth_signal"]) {display: none !important;}</style>""", unsafe_allow_html=True)

if not st.session_state.authenticated:
    st.markdown("<h2 style='text-align: center; color: #154A7F; margin-top: 80px;'>🔒 请输入访问口令</h2>", unsafe_allow_html=True)
    pwd = st.text_input("口令", type="password", label_visibility="collapsed", placeholder="请输入口令")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("进入系统", type="primary"):
            if pwd == "1984":
                st.session_state.authenticated = True
                # 密码正确，注入 JS 把密码存进 LocalStorage 永久记住
                save_auth_js = """<script>window.parent.localStorage.setItem('captain_auth', '1984');</script>"""
                components.html(save_auth_js, height=0)
                st.rerun()
            else:
                st.error("口令错误，请重试！")
    st.stop() 

# -----------------------------------------
# 5. 标题区
# -----------------------------------------
st.markdown("<h1>预计维修数量工具 V1.0</h1>", unsafe_allow_html=True)
st.markdown("<hr style='margin-top: -10px; border-top: 1px solid #d3d3d3;'>", unsafe_allow_html=True)

# -----------------------------------------
# 6. 表单输入区 (双向绑定全局数据，实现草稿共享)
# -----------------------------------------
st.markdown("当前排班人 <span class='subtitle'>(你的名字/昵称)</span>", unsafe_allow_html=True)
updater_name = st.text_input("updater", value=shared_data["updater_name"], label_visibility="collapsed", placeholder="例如: Ice")

st.markdown("关店时间 <span class='subtitle'>(支持半小时，如 22.5)</span>", unsafe_allow_html=True)
close_time_input = st.text_input("close_time", value=shared_data["close_time"], label_visibility="collapsed", placeholder="例如: 22.5")

st.markdown("维修工时排班 <span class='subtitle'>(随时可加减修改)</span>", unsafe_allow_html=True)
hours_input = {}
for h in range(10, 23):
    # 默认读取全局 shared_data 里的值
    hours_input[h] = st.text_input(f"{h}:00", value=shared_data["hours"][h], placeholder=f"{h}:00", label_visibility="collapsed")

st.markdown("当前等待维修数量 <span class='subtitle'>(积压排队的设备数)</span>", unsafe_allow_html=True)
wait_qty_input = st.text_input("wait_qty", value=shared_data["wait_qty"], label_visibility="collapsed", placeholder="请输入等待数量")

st.markdown("当前正在维修数量 <span class='subtitle'>(操作台上的设备数)</span>", unsafe_allow_html=True)
repairing_qty_input = st.text_input("repairing_qty", value=shared_data["repairing_qty"], label_visibility="collapsed", placeholder="请输入正在维修数量")

st.markdown("单台维修耗时 <span class='subtitle'>(分钟/台)</span>", unsafe_allow_html=True)
efficiency_input = st.text_input("efficiency", value=shared_data["efficiency"], label_visibility="collapsed", placeholder="例如: 40")

# 7. 计算按钮
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    generate_clicked = st.button("计算", type="primary")

if generate_clicked:
    if not updater_name.strip():
        st.warning("请在最上方填写当前排班人姓名！")
    else:
        bj_time = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
        
        # 将输入框的数据写入全局共享大屏 (草稿也一起保存了)
        shared_data["updater_name"] = updater_name.strip()
        shared_data["update_time"] = bj_time.strftime("%H:%M")
        shared_data["close_time"] = close_time_input.strip()
        shared_data["efficiency"] = efficiency_input.strip()
        shared_data["wait_qty"] = wait_qty_input.strip()
        shared_data["repairing_qty"] = repairing_qty_input.strip()
        for h in range(10, 23):
            shared_data["hours"][h] = hours_input[h].strip()
        
        shared_data["is_active"] = True
        st.toast("✅ 数据已同步至全队看板！", icon="🚀")

# 8. 渲染全队共享的实时看板
if shared_data["is_active"]:
    st.markdown("<div id='report_target'></div>", unsafe_allow_html=True)
    if generate_clicked:
        st.markdown("""<img src="x" onerror="setTimeout(function(){var t=window.parent.document.getElementById('report_target'); if(t){t.scrollIntoView({behavior: 'smooth', block: 'start'});}}, 300);" style="display:none;">""", unsafe_allow_html=True)

    close_hour = safe_float(shared_data["close_time"], 22.0)
    mins_per_device = safe_float(shared_data["efficiency"], 40.0)
    if mins_per_device <= 0: mins_per_device = 40.0 
    
    current_hour = (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).hour
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
    
    close_hour_display = int(close_hour)
    close_min_display = "30" if close_hour % 1 == 0.5 else "00"
    end_time_str = f"{close_hour_display}:{close_min_display}"
    
    accept_color = "#FF3B30" if can_accept < 0 else "#6200EE"
    accept_display = 0 if can_accept < 0 else can_accept
    
    warning_html = f"""<div class="pred-note" style="color: #FF3B30;">⚠️ 警告：当前任务已超出剩余产能 {abs(can_accept)} 台！</div>""" if can_accept < 0 else f"""<div class="pred-note">* 按单台耗时 {int(mins_per_device)} 分钟计算</div>"""

    card_html = f"""
    <div class="prediction-card">
        <div class="pred-title">
            <span>⏱️ 团队产能看板</span>
            <span style="font-size: 12px; color: #7E6BC4; font-weight: normal;">上次更新: {shared_data['updater_name']} @ {shared_data['update_time']}</span>
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

# 9. 注入全局前端魔法脚本 (强制数字键盘 + 回车跳跃)
magic_js = """
<script>
const doc = window.parent.document;

function killBadge() {
    const badges = doc.querySelectorAll('[class*="viewerBadge"], [class*="styles_viewerBadge"]');
    badges.forEach(b => { b.style.display = 'none'; b.style.opacity = '0'; });
}

function enhanceInputs() {
    killBadge();
    const inputs = Array.from(doc.querySelectorAll('input:not([type="hidden"]), textarea'));
    
    inputs.forEach((input, index) => {
        // 移除 inputmode，让 iOS 唤起默认的带数字排 QWERTY 键盘
        input.removeAttribute('inputmode');
        
        if (index < inputs.length - 1) {
            input.setAttribute('enterkeyhint', 'next');
        } else {
            input.setAttribute('enterkeyhint', 'done');
        }

        const wrapper = input.closest('div[data-baseweb="input"]');
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
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
        font-size: 15px;
    }
    .pred-highlight { font-size: 18px; font-weight: 900; color: #6200EE; }
    .pred-note { font-size: 12px; color: #7E6BC4; margin-top: 10px; text-align: right; }
    hr.dashed { border-top: 1px dashed #D1C4E9; margin: 12px 0; }
    
    div[data-baseweb="input"].is-filled {
        border-color: #4CAF50 !important;
        border-width: 2px !important;
        background-color: #F4FBF4 !important;
    }
    div[data-baseweb="input"].is-filled:focus-within { box-shadow: 0 0 0 1px #4CAF50 !important; }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------
# 3. 极简密码验证系统
# -----------------------------------------
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("<h2 style='text-align: center; color: #154A7F; margin-top: 80px;'>🔒 请输入访问口令</h2>", unsafe_allow_html=True)
    pwd = st.text_input("口令", type="password", label_visibility="collapsed", placeholder="请输入口令")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("进入系统", type="primary"):
            if pwd == "1984":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("口令错误，请重试！")
    st.stop() # 密码不对，停止加载后面的代码

# -----------------------------------------
# 4. 核心架构：全队共享数据 vs 个人草稿数据
# -----------------------------------------
@st.cache_resource
def get_shared_data():
    return {
        "is_active": False,
        "close_time": 22.0,
        "efficiency": 40.0,
        "wait_qty": 0,
        "repairing_qty": 0,
        "hours": {h: 0.0 for h in range(10, 23)},
        "updater_name": "",
        "update_time": ""
    }

shared_data = get_shared_data()

def safe_float(val, default=0.0):
    if not val: return default
    try: return float(val)
    except ValueError: return default

# 5. 标题区
st.markdown("<h1>预计维修数量工具 V1.0</h1>", unsafe_allow_html=True)
st.markdown("<hr style='margin-top: -10px; border-top: 1px solid #d3d3d3;'>", unsafe_allow_html=True)

# 6. 表单输入区 (个人草稿)
st.markdown("更新人 <span class='subtitle'>(你的名字/昵称)</span>", unsafe_allow_html=True)
updater_name = st.text_input("updater", value="", label_visibility="collapsed", placeholder="例如: Ice")

st.markdown("关店时间 <span class='subtitle'>(支持半小时，如 22.5)</span>", unsafe_allow_html=True)
close_time_input = st.text_input("close_time", value="22", label_visibility="collapsed", placeholder="例如: 22.5")

st.markdown("维修工时排班 <span class='subtitle'>(随时可加减修改)</span>", unsafe_allow_html=True)
hours_input = {}
for h in range(10, 23):
    hours_input[h] = st.text_input(f"{h}:00", value="", placeholder=f"{h}:00", label_visibility="collapsed")

st.markdown("当前等待维修数量 <span class='subtitle'>(积压排队的设备数)</span>", unsafe_allow_html=True)
wait_qty_input = st.text_input("wait_qty", value="", label_visibility="collapsed", placeholder="请输入等待数量")

st.markdown("当前正在维修数量 <span class='subtitle'>(操作台上的设备数)</span>", unsafe_allow_html=True)
repairing_qty_input = st.text_input("repairing_qty", value="", label_visibility="collapsed", placeholder="请输入正在维修数量")

st.markdown("单台维修耗时 <span class='subtitle'>(分钟/台)</span>", unsafe_allow_html=True)
efficiency_input = st.text_input("efficiency", value="40", label_visibility="collapsed", placeholder="例如: 40")

# 7. 计算按钮 (点击后将个人草稿同步到全队共享大屏)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    generate_clicked = st.button("计算", type="primary")

if generate_clicked:
    if not updater_name.strip():
        st.warning("请在最上方填写更新人姓名！")
    else:
        # 强制使用北京时间 (UTC+8)
        bj_time = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
        
        # 将输入框的数据写入全局共享大屏
        shared_data["updater_name"] = updater_name.strip()
        shared_data["update_time"] = bj_time.strftime("%H:%M")
        shared_data["close_time"] = safe_float(close_time_input, 22.0)
        shared_data["efficiency"] = safe_float(efficiency_input, 40.0)
        shared_data["wait_qty"] = int(safe_float(wait_qty_input))
        shared_data["repairing_qty"] = int(safe_float(repairing_qty_input))
        for h in range(10, 23):
            shared_data["hours"][h] = safe_float(hours_input[h])
        
        shared_data["is_active"] = True

# 8. 渲染全队共享的实时看板
if shared_data["is_active"]:
    # 锚点滚动
    st.markdown("<div id='report_target'></div>", unsafe_allow_html=True)
    if generate_clicked:
        st.markdown("""<img src="x" onerror="setTimeout(function(){var t=window.parent.document.getElementById('report_target'); if(t){t.scrollIntoView({behavior: 'smooth', block: 'start'});}}, 100);" style="display:none;">""", unsafe_allow_html=True)

    close_hour = shared_data["close_time"]
    mins_per_device = shared_data["efficiency"]
    if mins_per_device <= 0: mins_per_device = 40.0 
    
    # 强制使用北京时间计算当前小时
    current_hour = (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).hour
    start_hour = max(10, current_hour)
    
    remaining_hours = 0.0
    if start_hour < close_hour:
        max_box_hour = min(22, int(close_hour))
        for i in range(start_hour, max_box_hour + 1):
            remaining_hours += shared_data["hours"][i]
            
    wait_qty = shared_data["wait_qty"]
    repairing_qty = shared_data["repairing_qty"]
    
    total_capacity = int(remaining_hours / (mins_per_device / 60))
    can_accept = total_capacity - wait_qty - repairing_qty
    
    close_hour_display = int(close_hour)
    close_min_display = "30" if close_hour % 1 == 0.5 else "00"
    end_time_str = f"{close_hour_display}:{close_min_display}"
    
    accept_color = "#FF3B30" if can_accept < 0 else "#6200EE"
    accept_display = 0 if can_accept < 0 else can_accept
    
    warning_html = f"""<div class="pred-note" style="color: #FF3B30;">⚠️ 警告：当前任务已超出剩余产能 {abs(can_accept)} 台！</div>""" if can_accept < 0 else f"""<div class="pred-note">* 按单台耗时 {int(mins_per_device)} 分钟计算</div>"""

    # 渲染带有更新人信息的卡片
    card_html = f"""
    <div class="prediction-card">
        <div class="pred-title">
            <span>⏱️ 团队产能看板</span>
            <span style="font-size: 12px; color: #7E6BC4; font-weight: normal;">上次更新: {shared_data['updater_name']} @ {shared_data['update_time']}</span>
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

# 9. 注入全局前端魔法脚本 (强制数字键盘 + 回车跳跃)
magic_js = """
<script>
const doc = window.parent.document;

function killBadge() {
    const badges = doc.querySelectorAll('[class*="viewerBadge"], [class*="styles_viewerBadge"]');
    badges.forEach(b => { b.style.display = 'none'; b.style.opacity = '0'; });
}

function enhanceInputs() {
    killBadge();
    const inputs = Array.from(doc.querySelectorAll('input:not([type="hidden"]), textarea'));
    
    inputs.forEach((input, index) => {
        // --- 终极键盘魔法：强制唤起带小数点的数字键盘 ---
        // 除了第一个框（更新人名字）保留默认键盘，其他的全部变成数字键盘！
        if (index > 0) {
            input.setAttribute('inputmode', 'decimal');
        }
        
        if (index < inputs.length - 1) {
            input.setAttribute('enterkeyhint', 'next');
        } else {
            input.setAttribute('enterkeyhint', 'done');
        }

        const wrapper = input.closest('div[data-baseweb="input"]');
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
