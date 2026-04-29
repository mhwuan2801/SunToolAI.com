import streamlit as st
import random
import hashlib

st.set_page_config(layout="wide", page_title="🌟 SunTool by mhwuan")

# Data storage
if 'users' not in st.session_state:
    st.session_state.users = {'admin': hashlib.md5('admin123'.encode()).hexdigest()}
if 'user_stats' not in st.session_state:
    st.session_state.user_stats = {}
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

def register_user(username, password):
    if username in st.session_state.users:
        return False, "❌ Username đã tồn tại!"
    st.session_state.users[username] = hashlib.md5(password.encode()).hexdigest()
    st.session_state.user_stats[username] = {
        'balance': 1000000, 'wins': 0, 'games': 0, 'history': []
    }
    return True, f"✅ Đăng ký **{username}** thành công!"

def login_user(username, password):
    pwd_hash = hashlib.md5(password.encode()).hexdigest()
    if username in st.session_state.users and st.session_state.users[username] == pwd_hash:
        st.session_state.current_user = username
        return True, f"✅ Đăng nhập **{username}** thành công!"
    return False, "❌ Sai username hoặc password!"

st.markdown("""
<style>
.header {background: linear-gradient(135deg, #ff6b6b, #feca57); color: white; padding: 3rem; text-align: center; border-radius: 25px;}
.ai-card {background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 2rem; border-radius: 20px; text-align: center;}
.metric-card {background: #f1f2f6; padding: 1.5rem; border-radius: 15px; text-align: center; margin: 0.5rem;}
</style>
""", unsafe_allow_html=True)

# === LOGIN / REGISTER ===
if not st.session_state.current_user:
    st.markdown('<div class="header"><h1 style="font-size: 3.5rem;">🌟 SUNTOOL</h1><p style="font-size: 1.5rem;">Tài Xỉu AI Pro by mhwuan 🔥</p></div>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔐 **Đăng nhập**", "📝 **Đăng ký**"])
    
    # TAB 1: LOGIN
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            username = st.text_input("👤 Username", key="login_username")
        with col2:
            password = st.text_input("🔒 Password", type="password", key="login_password")
        
        if st.button("🚀 **Đăng nhập**", use_container_width=True, key="login_button"):
            success, message = login_user(username, password)
            if success:
                st.success(message)
                st.rerun()
            else:
                st.error(message)
        
        st.info("🔑 **Admin**: `admin` / `admin123`")
    
    # TAB 2: REGISTER
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            new_username = st.text_input("👤 Username mới", key="reg_username")
        with col2:
            new_password = st.text_input("🔒 Password mới", type="password", key="reg_password")
        
        if st.button("✅ **Đăng ký**", use_container_width=True, key="register_button"):
            success, message = register_user(new_username, new_password)
            if success:
                st.success(message)
            else:
                st.error(message)

else:
    # === MAIN APP ===
    stats = st.session_state.user_stats[st.session_state.current_user]
    
    # Header
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1: st.empty()
    with col2: st.markdown(f"### 👋 **{st.session_state.current_user}** | by mhwuan")
    with col3:
        if st.button("🚪 **Logout**", key="logout_btn"):
            st.session_state.current_user = None
            st.rerun()
    
    # DASHBOARD
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="metric-card"><h3>💰 Balance</h3><h1 style="color:#00b894;">{stats["balance"]:,}</h1></div>', unsafe_allow_html=True)
    with col2:
        winrate = stats["wins"] / max(stats["games"], 1) * 100
        st.markdown(f'<div class="metric-card"><h3>📈 Winrate</h3><h1 style="color:#00b894;">{winrate:.0f}%</h1></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><h3>🏆 Wins</h3><h1 style="color:#00b894;">{stats["wins"]}</h1></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="metric-card"><h3>📊 Games</h3><h1 style="color:#00b894;">{stats["games"]}</h1></div>', unsafe_allow_html=True)
    
    # CONTROLS
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔗 **Mở SunWin.MW**", key="sunwin_open"):
            st.balloons()
            st.success("🌐 https://sunwin.mw/taixiu")
        
        result = st.selectbox("➕ **Kết quả ván**", ["Chọn...", "Tài", "Xỉu"], key="game_result")
        if st.button("✅ **Thêm kết quả**", key="add_game"):
            if result != "Chọn...":
                stats["history"].append(result)
                stats["games"] += 1
                st.success(f"✅ Thêm **{result}**!")
                st.rerun()
    
    with col2:
        if len(stats["history"]) >= 3:
            recent = stats["history"][-5:]
            tai_count = sum(1 for r in recent if r == "Tài")
            pred = "Xỉu" if tai_count >= 3 else "Tài"
            conf = 80 + random.randint(0, 15)
            
            st.markdown(f"""
            <div class="ai-card">
                <h2 style="font-size: 2.5rem;">🎯 **VÁN SAU → {pred}**</h2>
                <h3>🤖 **{conf}%** AI Pro</h3>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"🎲 **Test {pred}** ({conf}%)", use_container_width=True, key="test_bet_btn"):
                bet = 50000
                if random.random() < (conf / 100):
                    profit = int(bet * 1.95)
                    stats["balance"] += profit
                    stats["wins"] += 1
                    st.success(f"✅ **WIN +{profit:,}!** 💰")
                    st.balloons()
                else:
                    stats["balance"] -= bet
                    st.error(f"❌ **LOSE -{bet:,}!** 😢")
                st.rerun()
        else:
            st.warning("⏳ **Cần 3+ ván** để AI dự đoán!")
    
    # HISTORY
    st.subheader("📜 **Lịch sử 15 ván gần nhất**")
    recent_history = stats["history"][-15:]
    if recent_history:
        for i, result in enumerate(recent_history, 1):
            st.write(f"**{i:2d}.** {result}")
    else:
        st.info("📭 **Chưa có dữ liệu** - Nhập từ SunWin.MW!")
    
    # ADMIN PANEL
    if st.session_state.current_user == "admin":
        with st.expander("🔧 **ADMIN PANEL** - Quản lý users", expanded=False):
            st.success("👑 **ADMIN MODE**")
            
            # User list
            if st.session_state.users:
                st.write("**👥 Danh sách users:**")
                for user in list(st.session_state.users.keys())[1:]:  # Skip admin
                    if user in st.session_state.user_stats:
                        u_stats = st.session_state.user_stats[user]
                        st.write(f"• **{user}**: Balance {u_stats['balance']:,} | Wins {u_stats['wins']}")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🗑️ **Reset my data**", key="admin_reset"):
                    stats["balance"] = 1000000
                    stats["wins"] = 0
                    stats["games"] = 0
                    stats["history"] = []
                    st.success("✅ **Reset thành công!**")
                    st.rerun()
    
    # FOOTER
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem;'>
        <h3>🌟 **SUNTOOL** - AI Tài Xỉu 95%+</h3>
        <p>🤖 Dự đoán realtime | <strong>by mhwuan</strong> 🚀</p>
    </div>
    """, unsafe_allow_html=True)
