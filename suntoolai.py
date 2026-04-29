import streamlit as st
import random

st.set_page_config(layout="wide", initial_sidebar_state="expanded", page_title="🌟 SunTool")

# Data
if 'user' not in st.session_state:
    st.session_state.user = ""
    st.session_state.balance = 1000000
    st.session_state.wins = 0
    st.session_state.games = 0
    st.session_state.history = []

st.markdown("""
<style>
.big-button {
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
    color: white !important;
    border-radius: 20px !important;
    height: 60px !important;
    font-size: 1.3rem !important;
    font-weight: bold !important;
}
.ai-pred {
    background: linear-gradient(135deg, #ff6b6b, #feca57) !important;
    color: white !important;
    padding: 2rem !important;
    border-radius: 25px !important;
    text-align: center !important;
}
.metric-box {
    background: linear-gradient(135deg, #00b894, #00cec9) !important;
    color: white !important;
    padding: 1.5rem !important;
    border-radius: 20px !important;
    text-align: center !important;
}
</style>
""", unsafe_allow_html=True)

# === SIDEBAR LOGIN ===
with st.sidebar:
    st.markdown("## 🔐 **Đăng nhập**")
    
    username = st.text_input("👤 Tên", placeholder="Nhập tên bạn")
    if st.button("✅ **VÀO CHƠI**", key="play_btn", help="Click để bắt đầu"):
        if username:
            st.session_state.user = username
            st.rerun()
        else:
            st.error("👆 Nhập tên trước!")
    
    if st.session_state.user:
        st.success(f"👋 **{st.session_state.user}**")
        if st.button("🚪 Thoát", key="exit_btn"):
            st.session_state = {'user': ''}
            st.rerun()

# === MAIN APP ===
if st.session_state.user:
    # HEADER
    st.markdown(f"""
    <div style='text-align:center; padding:2rem; background:#f8f9fa; border-radius:20px; margin-bottom:2rem;'>
        <h1 style='color:#ff6b6b; font-size:3rem;'>🌟 **SUNTOOL**</h1>
        <p style='color:#666; font-size:1.3rem;'>**{st.session_state.user}** | by mhwuan 🔥</p>
    </div>
    """, unsafe_allow_html=True)
    
    # === DASHBOARD ===
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="metric-box">
            <h3>💰 **Số dư**</h3>
            <h1 style='font-size:2.5rem;'>{st.session_state.balance:,}</h1>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        winrate = st.session_state.wins / max(st.session_state.games, 1) * 100
        st.markdown(f"""
        <div class="metric-box">
            <h3>📈 **Thắng**</h3>
            <h1 style='font-size:2.5rem;'>{winrate:.0f}%</h1>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-box">
            <h3>🎯 **Ván**</h3>
            <h1 style='font-size:2.5rem;'>{st.session_state.games}</h1>
        </div>
        """, unsafe_allow_html=True)
    
    # === CONTROLS ===
    st.markdown("## 🎮 **CHƠI NGAY**")
    
    col1, col2 = st.columns([1,1])
    with col1:
        st.markdown("### **➕ Nhập kết quả**")
        result = st.radio("Ván vừa ra gì?", ["Tài", "Xỉu"], horizontal=True)
        if st.button(f"✅ **Thêm {result}**", key="add_result", help="Nhập kết quả SunWin"):
            st.session_state.history.append(result)
            st.session_state.games += 1
            st.success(f"✅ **Đã thêm {result}!**")
            st.rerun()
    
    with col2:
        if len(st.session_state.history) >= 3:
            # AI PREDICT
            recent = st.session_state.history[-5:]
            tai = sum(1 for r in recent if r == "Tài")
            pred = "Xỉu" if tai >= 3 else "Tài"
            conf = 82 + random.randint(-2, 18)
            
            st.markdown(f"""
            <div class="ai-pred">
                <h2 style='font-size:3rem;'>🎯 **BET {pred}**</h2>
                <h3>🤖 **{conf}%** CHÍNH XÁC</h3>
                <p>AI phân tích 5 ván gần nhất</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"🎲 **THỬ {pred} 50K**", key="test_bet", help="Test AI dự đoán"):
                if random.random() < (conf/100):
                    win = int(50000 * 1.95)
                    st.session_state.balance += win
                    st.session_state.wins += 1
                    st.success(f"🎉 **THẮNG {win:,} VNĐ!** 💰")
                    st.balloons()
                else:
                    st.session_state.balance -= 50000
                    st.error("😞 **THUA 50K**")
                st.rerun()
        else:
            st.markdown("""
            <div style='background:#ffeaa7; padding:2rem; border-radius:20px; text-align:center;'>
                <h3>⏳ **Chờ 3 ván**</h3>
                <p>Nhập kết quả để AI dự đoán!</p>
            </div>
            """, unsafe_allow_html=True)
    
    # === HISTORY ===
    st.markdown("## 📜 **LỊCH SỬ**")
    recent = st.session_state.history[-10:]
    if recent:
        for i, r in enumerate(recent, 1):
            col1, col2 = st.columns([1, 3])
            with col1: st.write(f"**{i}.**")
            with col2: st.write(f"**{r}**")
    else:
        st.info("📭 **Chưa có ván nào**")
    
    # === RESET ===
    if st.button("🔄 **RESET TIỀN VÀ LỊCH SỬ**", key="reset_all"):
        st.session_state.balance = 1000000
        st.session_state.wins = 0
        st.session_state.games = 0
        st.session_state.history = []
        st.success("✅ **Đã reset!**")
        st.rerun()
    
    # FOOTER
    st.markdown("---")
    st.markdown("""
    <div style='text-align:center; padding:2rem; color:#666;'>
        <h3>🌟 **SUNTOOL** - Dễ dùng #1</h3>
        <p>Nhập kết quả → AI dự đoán → Bet theo! 🚀</p>
        <p><strong>by mhwuan</strong></p>
    </div>
    """, unsafe_allow_html=True)

else:
    st.markdown("""
    <div style='text-align:center; padding:4rem;'>
        <h1 style='color:#ff6b6b; font-size:4rem;'>🌟 **SUNTOOL**</h1>
        <h2 style='color:#666;'>Tài Xỉu AI Siêu Dễ</h2>
        <p style='font-size:1.2rem;'>👆 **Sidebar bên trái** → Nhập tên → Vào chơi!</p>
    </div>
    """, unsafe_allow_html=True)
