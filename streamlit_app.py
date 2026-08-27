import streamlit as st
import datetime
import streamlit.components.v1 as components

# 1. 页面配置
st.set_page_config(page_title="预计维修数量工具", layout="centered")

# 2. 强力 CSS (终极强制浅色模式)
st.markdown("""
    <style>
    /* =========================================
       🚀 终极强制浅色模式 (无视系统深色模式)
       ========================================= */
    /* 强行覆盖 Streamlit 的底层 CSS 变量 */
    :root, [data-theme="dark"], [data-theme="light"] {
        --primary-color: #6200EE !important;
        --background-color: #FFFFFF !important;
        --secondary-background-color: #F8F9FA !important;
        --text-color: #333333 !important;
        color-scheme: light !important;
    }
    
    /* 强制主容器白底黑字 */
    html, body, .stApp, [data-testid="stAppViewContainer"], .main, .block-container {
        background-color: #FFFFFF !important;
        color: #333333 !important;
    }
    
    /* 强制所有普通文本为深灰色 */
    .stMarkdown, .stMarkdown p, .stMarkdown span { 
        color: #333333 !important; 
    }
    
    /* 强制输入框白底黑字及边框颜色 */
    div[data-baseweb="input"], div[data-baseweb="input"] > div {
        background-color: #FFFFFF !important;
        border-color: #E0E0E0 !important;
    }
    input {
        color: #333333 !important;
        -webkit-text-fill-color: #333333 !important;
        background-color: #FFFFFF !important;
    }
    
    /* 强制弹窗 (Toast) 也是浅色 */
    div[data-testid="stToast"] {
        background-color: #FFFFFF !important;
        color: #333333 !important;
        border: 1px solid #D1C4E9 !important;
    }
    /* ========================================= */

    header {display: none !important;}
    .block-container { padding-top: 1.5rem !important; padding-bottom: 2rem !important; }
    #MainMenu, footer {visibility: hidden !important; display: none !important;}
    .stDeployButton {display: none !important;}
    [data-testid="stDeployButton"] {display: none !important;}
    div[class*="viewerBadge"] {display: none !important;}
    
    div[data-testid="InputInstructions"] { display: none !important; }
    div[data-testid="stNumberInput"] button { display: none !important; }
    
    label[data-testid="stWidgetLabel"] div {
        font-size: 15px !important;
        font-weight: bold !important;
        color: #154A7F !important;
    }
    .subtitle { font-size: 12px; color: #888888 !important; font-weight: normal; }

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

    button[kind="secondary"] {
        background-color: #f5f5f5 !important;
        color: #888888 !important;
        font-weight: bold !important;
        font-size: 16px !important;
        border: 1px solid #dddddd !important;
        border-radius: 8px !important;
        width: 100% !important;
        height: 45px !important;
        margin: 10px auto 0 auto !important;
        display: block !important;
    }
    button[kind="secondary"]:hover { background-color: #e8e8e8 !important; color: #333333 !important; }

    .prediction-card {
        background: linear-gradient(135deg, #F4F0FF 0%, #E8E2F8 100%);
        border: 1px solid #D1C4E9;
        border-radius: 12px;
        padding: 15px;
        margin-top: 20px;
        color: #4A3082 !important;
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
    .pred-highlight { font-size: 18px; font-weight: 900; color: #6200EE !important; }
    .pred-note { font-size: 12px; color: #7E6BC4 !important; margin-top: 10px; text-align: right; }
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
# 3. 获取北京时间
# -----------------------------------------
def get_bj_time():
    return datetime.datetime.utcnow() + datetime.timedelta(hours=8)

# -----------------------------------------
# 4. 核心架构：全队共享数据 + 自动清空逻辑
# -----------------------------------------
@st.cache_resource
def get_shared_data():
    return {
        "date": get_bj_time().date(), 
        "is_active": False,
        "close_time": 22.0,
        "efficiency": 40.0,
        "support_hours": None,
        "support_start_time": 14.0, 
        "wait_qty": None,
        "repairing_qty": None,
        "hours": {h: None for h in range(10, 23)},
        "updater_name": "",
        "update_time": ""
    }

shared_data = get_shared_data()

today_date = get_bj_time().date()
if shared_data["date"] < today_date:
    shared_data["date"] = today_date
    shared_data["is_active"] = False
    shared_data["support_hours"] = None
    shared_data["support_start_time"] = 14.0
    shared_data["wait_qty"] = None
    shared_data["repairing_qty"] = None
    for h in range(10, 23):
        shared_data["hours"][h] = None
    shared_data["updater_name"] = ""
    shared_data["update_time"] = ""

def calc_val(v):
    return float(v) if v is not None else 0.0

# -----------------------------------------
# 5. 极简原生密码验证系统
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
    st.stop() 

# -----------------------------------------
# 6. 标题区
# -----------------------------------------
st.markdown("<h1 style='color: #154A7F !important;'>预计维修数量工具 V1.1</h1>", unsafe_allow_html=True)
st.markdown("<hr style='margin-top: -10px; border-top: 1px solid #d3d3d3;'>", unsafe_allow_html=True)

# -----------------------------------------
# 7. 表单输入区
# -----------------------------------------
st.markdown("更新人 <span class='subtitle'>(你的名字/昵称)</span>", unsafe_allow_html=True)
updater_name = st.text_input("updater", value=shared_data["updater_name"], label_visibility="collapsed", placeholder="例如: Ice")

st.markdown("关店时间 <span class='subtitle'>(支持半小时，如 22.5)</span>", unsafe_allow_html=True)
close_time_input = st.number_input("close_time", value=shared_data["close_time"], step=0.5, label_visibility="collapsed")

st.markdown("维修工时排班 <span class='subtitle'>(随时可加减修改)</span>", unsafe_allow_html=True)
hours_input = {}
for h in range(10, 23):
    hours_input[h] = st.number_input(f"hour_{h}", value=shared_data["hours"][h], min_value=0.0, step=1.0, label_visibility="collapsed")

st.markdown("新增支援工时 <span class='subtitle'>(额外增加的总小时数)</span>", unsafe_allow_html=True)
support_hours_input = st.number_input("support_hours", value=shared_data.get("support_hours"), min_value=0.0, step=0.5, label_visibility="collapsed")

st.markdown("支援工时开始时间 <span class='subtitle'>(支持半小时，如 14.5 代表 14:30)</span>", unsafe_allow_html=True)
support_start_time_input = st.number_input("support_start_time", value=shared_data.get("support_start_time", 14.0), step=0.5, label_visibility="collapsed")

st.markdown("当前等待维修数量 <span class='subtitle'>(积压排队的设备数)</span>", unsafe_allow_html=True)
wait_qty_input = st.number_input("wait_qty", value=shared_data["wait_qty"], min_value=0.0, step=1.0, label_visibility="collapsed")

st.markdown("当前正在维修数量 <span class='subtitle'>(操作台上的设备数)</span>", unsafe_allow_html=True)
repairing_qty_input = st.number_input("repairing_qty", value=shared_data["repairing_qty"], min_value=0.0, step=1.0, label_visibility="collapsed")

st.markdown("单台维修耗时 <span class='subtitle'>(分钟/台)</span>", unsafe_allow_html=True)
efficiency_input = st.number_input("efficiency", value=shared_data["efficiency"], min_value=1.0, step=1.0, label_visibility="collapsed")

# 8. 计算按钮
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    generate_clicked = st.button("计算", type="primary")

if generate_clicked:
    if not updater_name.strip():
        st.warning("请在最上方填写更新人姓名！")
    else:
        shared_data["updater_name"] = updater_name.strip()
        shared_data["update_time"] = get_bj_time().strftime("%H:%M")
        shared_data["close_time"] = close_time_input
        shared_data["efficiency"] = efficiency_input
        shared_data["support_hours"] = support_hours_input
        shared_data["support_start_time"] = support_start_time_input  
        shared_data["wait_qty"] = wait_qty_input
        shared_data["repairing_qty"] = repairing_qty_input
        for h in range(10, 23):
            shared_data["hours"][h] = hours_input[h]
        
        shared_data["is_active"] = True
        st.toast("✅ 数据已同步至全队看板！", icon="🚀")

# 9. 渲染全队共享的实时看板
if shared_data["is_active"]:
    st.markdown("<div id='report_target'></div>", unsafe_allow_html=True)
    if generate_clicked:
        st.markdown("""<img src="x" onerror="setTimeout(function(){var t=window.parent.document.getElementById('report_target'); if(t){t.scrollIntoView({behavior: 'smooth', block: 'start'});}}, 300);" style="display:none;">""", unsafe_allow_html=True)

    close_hour = shared_data["close_time"]
    mins_per_device = shared_data["efficiency"]
    if mins_per_device <= 0: mins_per_device = 40.0 
    
    now = get_bj_time()
    curr_h = now.hour
    curr_m = now.minute
    now_mins = curr_h * 60 + curr_m
    close_mins = int(close_hour * 60)
    
    close_hour_display = int(close_hour)
    close_min_display = "30" if close_hour % 1 == 0.5 else "00"
    end_time_str = f"{close_hour_display}:{close_min_display}"
    
    if now_mins < 10 * 60:
        start_time_str = "10:00"
    elif now_mins >= close_mins:
        start_time_str = end_time_str
    else:
        start_time_str = f"{curr_h:02d}:{curr_m:02d}"
    
    remaining_hours = 0.0
    
    # 宏观剩余工时计算
    for i in range(10, 23):
        if i >= close_hour:
            continue
            
        block_start_mins = i * 60
        block_end_mins = int(min(i + 1, close_hour) * 60)
        block_total_mins = block_end_mins - block_start_mins
        
        if block_total_mins <= 0:
            continue
            
        if now_mins >= block_end_mins:
            left_mins = 0
        elif now_mins <= block_start_mins:
            left_mins = block_total_mins
        else:
            left_mins = block_end_mins - now_mins
            
        ratio = left_mins / block_total_mins
        val = calc_val(shared_data["hours"][i])
        remaining_hours += val * ratio
    
    support_hours_total = calc_val(shared_data.get("support_hours"))
    support_start_time = calc_val(shared_data.get("support_start_time", 14.0))
    remaining_support_hours = 0.0
    
    if support_hours_total > 0:
        support_start_mins = int(support_start_time * 60)
        total_support_duration_mins = close_mins - support_start_mins
        
        if total_support_duration_mins > 0:
            if now_mins <= support_start_mins:
                support_left_ratio = 1.0
            elif now_mins >= close_mins:
                support_left_ratio = 0.0
            else:
                support_left_ratio = (close_mins - now_mins) / total_support_duration_mins
            
            remaining_support_hours = support_hours_total * support_left_ratio
            remaining_hours += remaining_support_hours
            
    wait_qty = int(calc_val(shared_data["wait_qty"]))
    repairing_qty = int(calc_val(shared_data["repairing_qty"]))
    
    total_capacity = int(remaining_hours / (mins_per_device / 60))
    can_accept = total_capacity - wait_qty - repairing_qty
    
    accept_color = "#FF3B30" if can_accept < 0 else "#6200EE"
    accept_display = 0 if can_accept < 0 else can_accept

    # ==========================================
    # 🌟 新增核心逻辑：90分钟 SLA 微观预警系统 🌟
    # ==========================================
    target_tat_mins = 90
    queue_qty = wait_qty + repairing_qty
    # 清理当前队列所需的绝对工时
    required_labor_hours_for_queue = queue_qty * (mins_per_device / 60.0)

    # 设定未来 90 分钟的滑动时间窗口
    t_start = now_mins
    t_end = min(now_mins + target_tat_mins, close_mins)
    window_duration = t_end - t_start

    available_labor_hours_in_window = 0.0

    if window_duration > 0:
        # 1. 扫描常规排班在未来 90 分钟内的可用工时
        for i in range(10, 23):
            if i >= close_hour: continue
            block_start = i * 60
            block_end = int(min(i + 1, close_hour) * 60)
            
            # 计算当前小时块与 90 分钟窗口的重叠时间
            overlap_start = max(t_start, block_start)
            overlap_end = min(t_end, block_end)
            overlap_mins = max(0, overlap_end - overlap_start)
            
            if overlap_mins > 0:
                tech_count = calc_val(shared_data["hours"][i])
                available_labor_hours_in_window += tech_count * (overlap_mins / 60.0)
                
        # 2. 扫描支援排班在未来 90 分钟内的可用工时
        if support_hours_total > 0:
            support_start_mins = int(support_start_time * 60)
            total_support_duration_mins = close_mins - support_start_mins
            
            if total_support_duration_mins > 0:
                # 算出支援技师的人数密度
                support_tech_count = support_hours_total / (total_support_duration_mins / 60.0)
                
                overlap_start = max(t_start, support_start_mins)
                overlap_end = min(t_end, close_mins)
                overlap_mins = max(0, overlap_end - overlap_start)
                
                if overlap_mins > 0:
                    available_labor_hours_in_window += support_tech_count * (overlap_mins / 60.0)

    # 计算工时缺口
    sla_shortfall_hours = required_labor_hours_for_queue - available_labor_hours_in_window
    
    # 构建 SLA 专属 UI 模块
    if queue_qty == 0:
        sla_html = f"""
        <hr class="dashed">
        <div class="pred-data-row">
            <span>🎯 90分钟 SLA 状态：</span>
            <span><span class="pred-highlight" style="color: #4CAF50 !important; font-size: 16px;">🟢 队列为空</span></span>
        </div>
        """
    elif sla_shortfall_hours <= 0:
        sla_html = f"""
        <hr class="dashed">
        <div class="pred-data-row">
            <span>🎯 90分钟 SLA 状态：</span>
            <span><span class="pred-highlight" style="color: #4CAF50 !important; font-size: 16px;">🟢 达标 (产能充足)</span></span>
        </div>
        <div class="pred-note" style="text-align: right; margin-top: 4px;">
            未来 90 分钟可用工时: <strong>{available_labor_hours_in_window:.1f}h</strong> | 清理队列需: <strong>{required_labor_hours_for_queue:.1f}h</strong>
        </div>
        """
    else:
        sla_html = f"""
        <hr class="dashed">
        <div class="pred-data-row">
            <span>🎯 90分钟 SLA 状态：</span>
            <span><span class="pred-highlight" style="color: #FF3B30 !important; font-size: 16px;">🔴 超时预警</span></span>
        </div>
        <div class="pred-note" style="color: #FF3B30 !important; font-size: 13px; line-height: 1.6; text-align: right; margin-top: 4px;">
            未来 90 分钟仅有 <strong>{available_labor_hours_in_window:.1f}h</strong> 工时，但清理队列需 <strong>{required_labor_hours_for_queue:.1f}h</strong><br>
            ⚡️ 建议立即在接下来的 90 分钟内增加 <strong>{sla_shortfall_hours:.1f}</strong> 小时支援工时！
        </div>
        """
    # ==========================================

    if can_accept < 0:
        excess_qty = abs(can_accept)
        extra_hours_needed = (excess_qty * mins_per_device) / 60.0
        warning_html = f"<div class='pred-note' style='color: #FF3B30 !important; font-size: 13px; line-height: 1.6; text-align: right;'>⚠️ 警告：当前任务已超出全天剩余总产能 <strong>{excess_qty}</strong> 台！<br>⏳ 预计还需 <strong>{extra_hours_needed:.1f}</strong> 小时才能清掉队列</div>"
    else:
        warning_html = f"<div class='pred-note' style='text-align: right;'>* 按单台耗时 {int(mins_per_device)} 分钟计算</div>"

    if support_hours_total > 0:
        support_row_html = f"""<div class="pred-data-row" style="color: #4CAF50;">
<span>➕ 包含剩余支援工时：</span>
<span><span class="pred-highlight" style="color: #4CAF50 !important;">{remaining_support_hours:.1f}</span> h <span style="font-size: 12px; color: #888888; font-weight: normal;">(总 {support_hours_total:.1f}h)</span></span>
</div>"""
    else:
        support_row_html = ""

    # 组装最终卡片
    card_html = f"""<div class="prediction-card">
<div class="pred-title">
<span>⏱️ 团队产能看板</span>
<span style="font-size: 12px; color: #7E6BC4; font-weight: normal;">上次更新: {shared_data['updater_name']} @ {shared_data['update_time']}</span>
</div>
<div class="pred-data-row">
<span>从 <strong>{start_time_str}</strong> 到 <strong>{end_time_str}</strong> 剩余总工时：</span>
<span><span class="pred-highlight">{remaining_hours:.1f}</span> h</span>
</div>
{support_row_html}
<div class="pred-data-row">
<span>剩余工时总产能：</span>
<span><span class="pred-highlight" style="color: #FF3B30 !important;">{total_capacity}</span> 台</span>
</div>
<div class="pred-data-row">
<span>减去当前等待维修：</span>
<span><span class="pred-highlight" style="color: #4CAF50 !important;">{wait_qty}</span> 台</span>
</div>
<div class="pred-data-row">
<span>减去当前正在维修：</span>
<span><span class="pred-highlight" style="color: #4CAF50 !important;">{repairing_qty}</span> 台</span>
</div>

{sla_html}

<hr class="dashed">
<div class="pred-data-row" style="font-size: 18px; font-weight: bold;">
<span>✨ 还可以接入新单：</span>
<span><span class="pred-highlight" style="font-size: 24px; color: {accept_color} !important;">{accept_display}</span> 台</span>
</div>
{warning_html}
</div>"""
    
    st.markdown(card_html, unsafe_allow_html=True)

# 10. 手动清空与刷新按钮
def clear_data():
    shared_data["is_active"] = False
    shared_data["support_hours"] = None
    shared_data["support_start_time"] = 14.0
    shared_data["wait_qty"] = None
    shared_data["repairing_qty"] = None
    for h in range(10, 23):
        shared_data["hours"][h] = None
    shared_data["updater_name"] = ""
    shared_data["update_time"] = ""

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    if st.button("刷新数据", type="secondary"):
        st.toast("🔄 数据已更新至最新！")
        st.rerun()
with col_btn2:
    if st.button("清空今日数据", type="secondary"):
        clear_data()
        st.rerun()

# 11. 注入全局前端魔法脚本
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
        if (input.getAttribute('type') === 'number') {
            input.removeAttribute('inputmode');
            input.removeAttribute('pattern');
        }

        let label = input.getAttribute('aria-label');
        if (label && label.startsWith('hour_')) {
            let hour = label.split('_')[1];
            input.setAttribute('placeholder', hour + ':00');
        } else if (label === 'support_hours') {
            input.setAttribute('placeholder', '请输入支援工时');
        } else if (label === 'support_start_time') {
            input.setAttribute('placeholder', '请输入开始时间');
        } else if (label === 'wait_qty') {
            input.setAttribute('placeholder', '请输入等待数量');
        } else if (label === 'repairing_qty') {
            input.setAttribute('placeholder', '请输入正在维修数量');
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
        
        if (!input.dataset.focusedAttached) {
            input.addEventListener('focus', function() {
                setTimeout(() => this.select(), 50);
            });
            input.dataset.focusedAttached = 'true';
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
