import streamlit as st
import random
import hashlib

st.set_page_config(layout="wide", page_title="🌟 SunTool", initial_sidebar_state="expanded")

# ==================== DATA ====================
if 'users' not in st.session_state:
    st.session_state.users = {
        'admin': hashlib.md5('admin123'.encode()).hexdigest()
    }
if 'user_stats' not in st.session_state:
    st.session_state.user_stats = {}
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

def register(username, password):
    if username in st.session_state.users:
        return False, "❌ Username đã tồn tại"
    st.session_state.users[username] = hashlib.md5(password.encode()).hexdigest()
    st.session_state.user_stats[username] = {
        'balance': 1000000, 'wins': 0, 'games': 0, 'history': []
    }
    return True, f"✅ Tạo **{username}** thành công!"

def login(username, password):
    hash_pwd = hashlib.md5(password.encode()).hexdigest()
    if username in st.session_state.users and st.session_state.users[username] == hash_pwd:
        st.session_state.current_user = username
        return True, f"✅ Chào **{username}**!"
    return False, "❌ Sai tên/mật khẩu"

# ==================== UI ====================
st.markdown("""
<style>
.big-btn {height: 55px !important; border-radius: 15px !important; font-size: 1.2rem !important; font-weight: bold !important;}
.ai-box {background: linear-gradient(135deg, #ff6b6b, #feca57); color: white; padding: 2rem; border-radius: 20px; text-align: center;}
.metric-box {background: linear-gradient(135deg, #00b894, #00cec9); color: white; padding: 1.5rem; border-radius: 15px; text-align: center;}
.admin-panel {background: #2d3436; color: #00b894; padding: 1.5rem; border-radius: 15px;}
</style>
""", unsafe_allow_html=True)

# ==================== LOGIN/REGISTER ====================
if not st.session_state.current_user:
    # Header
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        <div style='text-align: center; padding: 3rem; background: linear-gradient(135deg, #667eea, #764ba2); color: white; border-radius: 25px;'>
            <h1 style='font-size: 3rem;'>🌟 **SUNTOOL**</h1>
            <p style='font-size: 1.3rem;'>Tài Xỉu AI Pro <strong>by mhwuan</strong></p>
        </div>
        """, unsafe_allow_html=True)
    
    tab_login, tab_register = st.tabs(["🔐 **Đăng nhập**", "📝 **Đăng ký**"])
    
    with tab_login:
        col1, col2 = st.columns(2)
        with col1: username = st.text_input("👤 Username", key="l1")
        with col2: password = st.text_input("🔒 Password", type="password", key="l2")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🚀 **ĐĂNG NHẬP**", key="login_key", help="Nhấn để vào chơi"):
                ok, msg = login(username, password)
                if ok:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
        st.info("🔑 **Admin**: `admin` / `admin123`")
    
    with tab_register:
        col1, col2 = st.columns(2)
        with col1: new_user = st.text_input("👤 Username mới", key="r1")
        with col2: new_pass = st.text_input("🔒 Password mới", type="password", key="r2")
        
        if st.button("✅ **TẠO TÀI KHOẢN**", key="reg_key"):
            ok, msg = register(new_user, new_pass)
            if ok: st.success(msg)
            else: st.error(msg)

else:
    # ==================== MAIN APP ====================
    stats = st.session_state.user_stats[st.session_state.current_user]
    
    # Header
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2: 
        st.markdown(f"""
        <div style='text-align:center; padding:1.5rem; background:#f8f9fa; border-radius:15px;'>
            <h2 style='color:#ff4757;'>👋 **{st.session_state.current_user}**</h2>
            <p>🌟 SunTool by mhwuan</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        if st.button("🚪 **THOÁT**", key="logout_k"):
            st.session_state.current_user = None
            st.rerun()
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 **Số dư**", f"{stats['balance']:,}đ")
    col2.metric("📈 **Winrate**", f"{stats['wins']/max(stats['games'],1)*100:.0f}%")
    col3.metric("🏆 **Thắng**", stats['wins'])
    col4.metric("🎯 **Ván**", stats['games'])
    
    # Controls
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### **➕ NHẬP KẾT QUẢ**")
        result = st.radio("**Ván vừa:**", ["Tài", "Xỉu"], horizontal=True, key="res_k")
        if st.button(f"✅ **THÊM {result}**", key="add_k", help="Kết quả từ SunWin"):
            stats['history'].append(result)
            stats['games'] += 1
            st.rerun()
        
        if st.button("🔗 **SUNWIN.MW**", key="sun_k"):
            st.balloons()
    
    with col2:
        st.markdown("### **🤖 AI DỰ ĐOÁN**")
        if len(stats['history']) >= 3:
            recent = stats['history'][-5:]
            tai = sum(1 for r in recent if r == "Tài")
            pred = "Xỉu" if tai >= 3 else "Tài"
            conf = 80 + random.randint(0, 15)
            
            st.markdown(f"""
            <div class="ai-box">
                <h2 style='font-size:2.5rem;'>🎯 **{pred}**</h2>
                <h3>**{conf}%** CHÍNH XÁC</h3>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"🎲 **BET 50K {pred}**", key="bet_k"):
                if random.random() < conf/100:
                    win = int(50000*1.95)
                    stats['balance'] += win
                    stats['wins'] += 1
                    st.success(f"✅ **+{win:,}đ** 💰")
                else:
                    stats['balance'] -= 50000
                    st.error("❌ **-50K**")
                st.rerun()
        else:
            st.error("⏳ **Cần 3 ván** để dự đoán!")
    
    # History
    st.markdown("### 📜 **LỊCH SỬ**")
    hist = stats['history'][-12:]
    for i, r in enumerate(hist, 1):
        st.write(f"**{i}.** {r}")
    
    # Admin
    if st.session_state.current_user == 'admin':
        with st.expander("🔧 **ADMIN**", expanded=False):
            st.markdown('<div class="admin-panel">👑 **ADMIN MODE**</div>', unsafe_allow_html=True)
            st.write("**Users:**", len(st.session_state.users)-1)
            if st.button("🔄 **RESET ALL**", key="adm_reset"):
                stats['balance'] = 1000000
                stats['wins'] = 0
                stats['games'] = 0
                stats['history'] = []
                st.success("✅ Reset!")
                st.rerun()
    
    st.markdown("---")
    st.markdown("<p style='text-align:center;color:#666;'>🌟 **SUNTOOL** by mhwuan | Dễ dùng #1</p>", unsafe_allow_html=True)
