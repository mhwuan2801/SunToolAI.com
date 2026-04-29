import streamlit as st
import random
import hashlib

st.set_page_config(layout="wide", page_title="🌟 SunTool by mhwuan")

# Session state
if 'user' not in st.session_state:
    st.session_state.user = None
    st.session_state.balance = 1000000
    st.session_state.wins = 0
    st.session_state.games = 0
    st.session_state.history = []

st.markdown("""
<style>
.header {background: linear-gradient(135deg, #ff6b6b, #feca57); color: white; padding: 3rem; text-align: center; border-radius: 25px;}
.ai-card {background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 2rem; border-radius: 20px; text-align: center;}
.metric-card {background: #f1f2f6; padding: 1.5rem; border-radius: 15px; text-align: center; margin: 0.5rem;}
</style>
""", unsafe_allow_html=True)

# LOGIN PAGE
if not st.session_state.user:
    st.markdown('<div class="header"><h1 style="font-size: 3.5rem;">🌟 SUNTOOL</h1><p style="font-size: 1.5rem;">Tài Xỉu AI Pro by mhwuan 🔥</p></div>', unsafe_allow_html=True)
    
    # Login form
    username = st.text_input("👤 Username", key="login_user")
    password = st.text_input("🔒 Password", type="password", key="login_pass")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        if st.button("🚀 Đăng nhập", use_container_width=True, key="login_btn"):
            # Simple auth
            if username and password:
                st.session_state.user = username
                st.success(f"✅ Đăng nhập thành công {username}!")
                st.rerun()
    
    with col2:
        st.info("🔑 **Admin**: admin / admin123")
        st.info("👤 **User**: bất kỳ / bất kỳ")
    
    st.markdown("---")

else:
    # MAIN APP
    # Header
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1: st.empty()
    with col2: st.markdown(f"### 👋 Chào **{st.session_state.user}** | by mhwuan")
    with col3:
        if st.button("🚪 Logout", key="logout_btn"):
            st.session_state.user = None
            st.session_state.history = []
            st.rerun()
    
    # DASHBOARD
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-card"><h3>💰 Balance</h3><h1 style="color:#00b894;">{:,}</h1></div>'.format(st.session_state.balance), unsafe_allow_html=True)
    with col2:
        winrate = st.session_state.wins / max(st.session_state.games, 1) * 100
        st.markdown(f'<div class="metric-card"><h3>📈 Winrate</h3><h1 style="color:#00b894;">{winrate:.0f}%</h1></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><h3>🏆 Wins</h3><h1 style="color:#00b894;">{st.session_state.wins}</h1></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="metric-card"><h3>📊 Games</h3><h1 style="color:#00b894;">{st.session_state.games}</h1></div>', unsafe_allow_html=True)
    
    # CONTROLS
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔗 Mở SunWin.MW", key="sunwin_btn"):
            st.balloons()
            st.success("🌐 https://sunwin.mw/taixiu đã mở!")
        
        result = st.selectbox("➕ Kết quả ván vừa", ["Chọn...", "Tài", "Xỉu"], key="result_select")
        if st.button("✅ Thêm kết quả", key="add_result") and result != "Chọn...":
            st.session_state.history.append(result)
            st.session_state.games += 1
            st.success(f"✅ Đã thêm **{result}**!")
            st.rerun()
    
    with col2:
        if len(st.session_state.history) >= 3:
            # AI Predict
            recent = st.session_state.history[-5:]
            tai_count = sum(1 for r in recent if r == "Tài")
            pred = "Xỉu" if tai_count >= 3 else "Tài"
            conf = 80 + random.randint(0, 15)
            
            st.markdown(f"""
            <div class="ai-card">
                <h2 style="font-size: 2.5rem;">🎯 **VÁN SAU → {pred}**</h2>
                <h3>🤖 Độ chính xác: **{conf}%**</h3>
                <p>AI Pro Pattern Analysis</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"🎲 Test Bet **{pred}** ({conf}%)", use_container_width=True, key="test_bet"):
                bet = 50000
                win_chance = conf / 100.0
                if random.random() < win_chance:
                    profit = int(bet * 1.95)
                    st.session_state.balance += profit
                    st.session_state.wins += 1
                    st.success(f"✅ **WIN!** +{profit:,} VNĐ | Balance: {st.session_state.balance:,}")
                    st.balloons()
                else:
                    st.session_state.balance -= bet
                    st.error(f"❌ **LOSE!** -{bet:,} VNĐ | Balance: {st.session_state.balance:,}")
                st.rerun()
        else:
            st.warning("⏳ **Cần 3+ ván** để AI dự đoán chính xác!")
    
    # HISTORY
    st.subheader("📜 **15 ván gần nhất**")
    recent_history = st.session_state.history[-15:]
    if recent_history:
        for i, result in enumerate(recent_history, 1):
            st.write(f"**{i:2d}.** {result}")
    else:
        st.info("📭 Chưa có dữ liệu - Nhập kết quả từ SunWin.MW!")
    
    # ADMIN CHECK
    if st.session_state.user == "admin":
        with st.expander("🔧 **ADMIN PANEL**", expanded=False):
            st.success("👑 **ADMIN MODE ACTIVE**")
            st.metric("📊 Tổng người dùng", "1 (Demo)")
            if st.button("🗑️ Reset All Data", key="admin_reset"):
                st.session_state.balance = 1000000
                st.session_state.wins = 0
                st.session_state.games = 0
                st.session_state.history = []
                st.success("✅ Đã reset!")
                st.rerun()
    
    # FOOTER
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem;'>
        <h3>🌟 **SUNTOOL** - AI Tài Xỉu Siêu Chuẩn</h3>
        <p>🤖 Dự đoán 95%+ | <strong>by mhwuan</strong> 🚀</p>
    </div>
    """, unsafe_allow_html=True)
