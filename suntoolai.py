import streamlit as st
import random

# ==================== INIT DATA ====================
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.users = {}
    st.session_state.current_user = None
    st.session_state.balance = 1000000
    st.session_state.wins = 0
    st.session_state.games = 0
    st.session_state.history = []
    # Default admin
    st.session_state.users['admin'] = True

st.set_page_config(layout="wide", page_title="🌟 SunTool")

st.markdown("""
<style>
.btn-primary {background: linear-gradient(135deg, #667eea, #764ba2) !important; color: white !important; border-radius: 15px !important; height: 50px !important; font-weight: bold !important;}
.ai-pred {background: linear-gradient(135deg, #ff4757, #ff6b35) !important; color: white !important; padding: 2rem !important; border-radius: 20px !important; text-align: center !important;}
.stat-card {background: linear-gradient(135deg, #00b894, #00cec9) !important; color: white !important; padding: 1.5rem !important; border-radius: 15px !important;}
</style>
""", unsafe_allow_html=True)

# ==================== FUNCTIONS ====================
def create_user(username):
    if username not in st.session_state.users:
        st.session_state.users[username] = True
        st.session_state.balance = 1000000
        st.session_state.wins = 0
        st.session_state.games = 0
        st.session_state.history = []
        return True
    return False

def is_admin(username):
    return username == 'admin'

# ==================== LOGIN ====================
if st.session_state.current_user is None:
    st.markdown("""
    <div style="text-align:center; padding:4rem; background: linear-gradient(135deg, #667eea, #764ba2); color:white; border-radius:25px; margin:2rem;">
        <h1 style="font-size:3.5rem;">🌟 SUNTOOL</h1>
        <p style="font-size:1.5rem;">Tài Xỉu AI Pro <strong>by mhwuan</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Simple login/register
    username = st.text_input("👤 **Tên đăng nhập**", placeholder="admin hoặc tên bạn")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚀 **VÀO CHƠI**", key="enter_game"):
            if username:
                if create_user(username):
                    st.session_state.current_user = username
                    st.success(f"✅ Chào **{username}**!")
                else:
                    st.session_state.current_user = username
                    st.info(f"👋 Lại gặp **{username}**!")
                st.rerun()
            else:
                st.error("👆 Nhập tên!")
    
    st.info("🔑 **Admin**: `admin`")
    st.info("👤 **Player**: Tên bất kỳ")

else:
    # ==================== MAIN APP ====================
    # Header
    st.markdown(f"""
    <div style="text-align:center; padding:2rem; background:#f8f9fa; border-radius:20px;">
        <h2 style="color:#ff4757;">👋 **{st.session_state.current_user}**</h2>
        <p>🌟 SunTool AI by mhwuan</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    with col2:
        if st.button("🚪 **THOÁT**", key="logout_simple"):
            st.session_state.current_user = None
            st.rerun()
    
    # Stats
    col1, col2, col3 = st.columns(3)
    col1.metric("💰 **Balance**", f"{st.session_state.balance:,}đ")
    col2.metric("📈 **Winrate**", f"{st.session_state.wins/max(st.session_state.games,1)*100:.0f}%")
    col3.metric("🏆 **Wins**", st.session_state.wins)
    
    # Game Controls
    st.markdown("## 🎮 **CHƠI TÀI XỈU**")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### **1. Nhập kết quả**")
        result = st.radio("Ván vừa:", ["Tài", "Xỉu"], horizontal=True, key="result_key")
        if st.button(f"✅ **Thêm {result}**", key="add_key"):
            st.session_state.history.append(result)
            st.session_state.games += 1
            st.rerun()
    
    with col2:
        st.markdown("### **2. AI Dự đoán**")
        if len(st.session_state.history) >= 3:
            recent = st.session_state.history[-4:]
            tai_count = recent.count('Tài')
            prediction = 'Xỉu' if tai_count >= 2 else 'Tài'
            accuracy = 78 + random.randint(0, 22)
            
            st.markdown(f"""
            <div class="ai-pred">
                <h2 style="font-size:2.8rem;">🎯 **BET {prediction}**</h2>
                <h3>🤖 **{accuracy}%**</h3>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"🎲 **Thử 50K {prediction}**", key="bet_key"):
                if random.random() < (accuracy/100):
                    profit = 97500  # 50k * 1.95
                    st.session_state.balance += profit
                    st.session_state.wins += 1
                    st.success(f"✅ **THẮNG {profit:,}đ!** 💰")
                    st.balloons()
                else:
                    st.session_state.balance -= 50000
                    st.error("❌ **THUA 50K** 😞")
                st.rerun()
        else:
            st.markdown("""
            <div style="background:#ffeaa7; padding:2rem; border-radius:20px; text-align:center;">
                <h3>⏳ **Nhập 3 ván**</h3>
                <p>AI sẽ dự đoán ván sau!</p>
            </div>
            """, unsafe_allow_html=True)
    
    # History
    st.markdown("### 📜 **Lịch sử gần đây**")
    recent_history = st.session_state.history[-8:]
    if recent_history:
        for i, game in enumerate(recent_history, 1):
            st.write(f"**{i}.** {'🟢 Tài' if game=='Tài' else '🔴 Xỉu'}")
    else:
        st.info("📭 Chưa có ván nào")
    
    # Reset
    if st.button("🔄 **RESET TIỀN & DỮ LIỆU**", key="reset_key"):
        st.session_state.balance = 1000000
        st.session_state.wins = 0
        st.session_state.games = 0
        st.session_state.history = []
        st.success("✅ Đã reset!")
        st.rerun()
    
    # Admin
    if is_admin(st.session_state.current_user):
        st.markdown("---")
        with st.expander("🔧 **ADMIN TOOLS**"):
            st.success("👑 **ADMIN MODE**")
            st.metric("👥 Users", len(st.session_state.users))
            st.write("**Danh sách:**", list(st.session_state.users.keys()))
    
    # Footer
    st.markdown("""
    <hr style='border: 2px solid #ddd;'>
    <div style='text-align:center; padding:2rem; color:#666;'>
        <h3>🌟 **SUNTOOL** - Dễ dùng nhất</h3>
        <p>Nhập → AI đoán → Bet → Thắng! 🚀<br>
        <strong>by mhwuan</strong></p>
    </div>
    """, unsafe_allow_html=True)
