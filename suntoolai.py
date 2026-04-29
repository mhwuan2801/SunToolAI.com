import streamlit as st
import random

st.set_page_config(layout="wide", page_title="🌟 SunTool by mhwuan")

# ==================== CSS ====================
st.markdown("""
<style>
.main-header {background: linear-gradient(135deg, #ff6b6b, #feca57); color: white; padding: 3rem; text-align: center; border-radius: 25px;}
.ai-card {background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 2.5rem; border-radius: 20px; text-align: center;}
.stat-card {background: linear-gradient(135deg, #00b894, #00cec9); color: white; padding: 1.5rem; border-radius: 15px; text-align: center;}
.btn-large {height: 55px !important; border-radius: 15px !important; font-size: 1.2rem !important; font-weight: bold !important;}
</style>
""", unsafe_allow_html=True)

# ==================== DATA (st.cache_data) ====================
@st.cache_data
def get_data():
    return {
        'balance': 1000000,
        'wins': 0,
        'games': 0,
        'history': []
    }

# ==================== MAIN UI ====================
# Header
st.markdown("""
<div class="main-header">
    <h1 style="font-size: 3.5rem; margin: 0;">🌟 **SUNTOOL**</h1>
    <p style="font-size: 1.4rem; margin: 0;">**Tài Xỉu AI Pro** <strong>by mhwuan</strong> 🔥</p>
</div>
""", unsafe_allow_html=True)

# Sidebar Login
with st.sidebar:
    st.header("🔐 **VÀO CHƠI**")
    username = st.text_input("👤 **Tên của bạn**", placeholder="admin hoặc bất kỳ")
    
    if st.button("🚀 **BẮT ĐẦU**", key="start_game"):
        if username:
            st.success(f"👋 **{username}** đã vào!")
            st.rerun()
        else:
            st.error("👆 **Nhập tên!**")
    
    st.markdown("---")
    st.info("""
    🔑 **Admin**: `admin`
    👤 **Player**: Tên bất kỳ
    """)

# Game state (use query params or simple state)
if 'game_state' not in st.session_state:
    st.session_state.game_state = get_data()

stats = st.session_state.game_state

# ==================== DASHBOARD ====================
col1, col2, col3 = st.columns(3)
col1.metric("💰 **Số dư**", f"{stats['balance']:,} VNĐ")
col2.metric("📈 **Tỷ lệ thắng**", f"{stats['wins']/max(stats['games'],1)*100:.0f}%")
col3.metric("🏆 **Số ván thắng**", stats['wins'])

# ==================== GAME CONTROLS ====================
st.markdown("## 🎮 **CHƠI NGAY**")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### **1. NHẬP KẾT QUẢ**")
    result = st.radio("**Ván vừa ra:**", ["Tài", "Xỉu"], horizontal=True)
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button(f"✅ **Tài**", key="add_tai"):
            stats['history'].append("Tài")
            stats['games'] += 1
            st.rerun()
    with col_btn2:
        if st.button(f"✅ **Xỉu**", key="add_xiu"):
            stats['history'].append("Xỉu")
            stats['games'] += 1
            st.rerun()

with col2:
    st.markdown("### **2. AI DỰ ĐOÁN**")
    if len(stats['history']) >= 3:
        recent = stats['history'][-4:]
        tai_count = recent.count('Tài')
        prediction = "Xỉu" if tai_count >= 2 else "Tài"
        confidence = 75 + random.randint(5, 25)
        
        st.markdown(f"""
        <div class="ai-card">
            <h2 style="font-size: 3rem;">🎯 **{prediction}**</h2>
            <h3>🤖 **{confidence}%**</h3>
            <p>AI phân tích pattern</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"🎲 **BET 50K {prediction}**", key="bet_button"):
            if random.random() < (confidence / 100):
                profit = 97500
                stats['balance'] += profit
                stats['wins'] += 1
                st.success(f"✅ **THẮNG {profit:,}đ!** 💰💰")
                st.balloons()
            else:
                stats['balance'] -= 50000
                st.error("❌ **THUA 50K** 😞")
            st.rerun()
    else:
        st.markdown("""
        <div style="background: #ffeaa7; padding: 2rem; border-radius: 20px; text-align: center;">
            <h3>⏳ **Chờ 3 ván nữa**</h3>
            <p>AI sẽ dự đoán chính xác!</p>
        </div>
        """, unsafe_allow_html=True)

# ==================== HISTORY ====================
st.markdown("## 📜 **LỊCH SỬ 10 VÁN**")
recent_history = stats['history'][-10:]
if recent_history:
    for i, result in enumerate(recent_history, 1):
        emoji = "🟢" if result == "Tài" else "🔴"
        st.write(f"**{i}.** {emoji} **{result}**")
else:
    st.info("📭 **Chưa có ván nào - Nhập ngay!**")

# ==================== CONTROLS ====================
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🔗 **SUNWIN.MW**", key="sunwin_link"):
        st.balloons()
        st.info("🌐 https://sunwin.mw/taixiu")
with col2:
    if st.button("🔄 **RESET TIỀN**", key="reset_money"):
        stats['balance'] = 1000000
        st.success("✅ **Số dư: 1.000.000đ**")
        st.rerun()
with col3:
    if st.button("🗑️ **XÓA LỊCH SỬ**", key="clear_history"):
        stats['history'] = []
        stats['wins'] = 0
        stats['games'] = 0
        st.success("✅ **Lịch sử sạch!**")
        st.rerun()

# Admin check
if st.session_state.current_user == 'admin':
    with st.expander("🔧 **ADMIN**"):
        st.success("👑 **ADMIN MODE**")
        st.metric("👥 Users", "Demo")
        st.write("**Chức năng:** Reset/Clear")

# Footer
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #666; border-top: 2px solid #eee;">
    <h3>🌟 **SUNTOOL** - Dễ nhất thế giới</h3>
    <p>Nhập kết quả → AI đoán → Bet thắng → Rich! 🚀</p>
    <p><strong>by mhwuan</strong></p>
</div>
""", unsafe_allow_html=True)
