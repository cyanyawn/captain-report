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
    div[data-testid="stNumberInput"] button { display: none !important; }
    
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
st.markdown("<h1>预计维修数量工具 V1.0</h1>", unsafe_allow_html=True)
st.markdown("<hr style='margin-top: -10px; border-top: 1px solid #d3d3d3;'>", unsafe_allow_html=True)

# -----------------------------------------
# 7. 表单输入区 (坚决使用 number_input 保护键盘)
# -----------------------------------------
st.markdown("更新人 <span class='subtitle'>(你的名字/昵称)</span>", unsafe_allow_html=True)
updater_name = st.text_input("updater", value=shared_data["updater_name"], label_visibility="collapsed", placeholder="例如: Ice")

st.markdown("关店时间 <span class='subtitle'>(支持半小时，如 22.5)</span>", unsafe_allow_html=True)
close_time_input = st.number_input("close_time", value=shared_data["close_time"], step=0.5, label_visibility="collapsed")

st.markdown("维修工时排班 <span class='subtitle'>(随时可加减修改)</span>", unsafe_allow_html=True)
hours_input = {}
for h in range(10, 23):
    hours_input[h] = st.number_input(f"hour_{h}", value=shared_data["hours"][h], min_value=0.0, step=1.0, label_visibility="collapsed")

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
    
    current_hour = get_bj_time().hour
    start_hour = max(10, current_hour)
    
    remaining_hours = 0.0
    if start_hour < close_hour:
        max_box_hour = min(22
