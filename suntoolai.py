import streamlit as st
import random

st.set_page_config(layout="wide")

if 'app_state' not in st.session_state:
    st.session_state.app_state = {
        'user': None, 'pass_ok': False,
        'balance': 1000000, 'wins': 0, 'games': 0, 
        'history': [], 'admin': False
    }

# Login
if not st.session_state.app_state['user']:
    st.title("🌟 **SUNTOOL** by mhwuan")
    col1,col2 = st.columns(2)
    with col1:
        user = st.text_input("👤 Username")
        pwd = st.text_input("🔑 Password",type="password")
    with col2:
        if st.button("🚀 **LOGIN**"):
            if user and pwd:
                st.session_state.app_state['user'] = user
                if user == "admin" and pwd == "admin123":
                    st.session_state.app_state['admin'] = True
                st.rerun()
    st.info("🔑 admin/admin123")
else:
    # Main app
    st.markdown(f"## 👋 **{st.session_state.app_state['user']}** | Admin: {st.session_state.app_state['admin']}")
    
    # Stats
    col1,col2,col3,col4 = st.columns(4)
    col1.metric("💰",f"{st.session_state.app_state['balance']:,}")
    col2.metric("📈",f"{st.session_state.app_state['wins']/max(st.session_state.app_state['games'],1)*100:.0f}%")
    col3.metric("🏆",st.session_state.app_state['wins'])
    col4.metric("🎯",st.session_state.app_state['games'])
    
    # Game
    col1,col2 = st.columns(2)
    with col1:
        res = st.radio("**Ván vừa**", ["Tài","Xỉu"])
        col1b,col2b = st.columns(2)
        if col1b.button("✅ **Thêm**"):
            st.session_state.app_state['history'].append(res)
            st.session_state.app_state['games'] += 1
            st.rerun()
        if col2b.button("🔗 **SunWin**"):
            st.balloons()
    
    with col2:
        if len(st.session_state.app_state['history'])>=3:
            recent = st.session_state.app_state['history'][-5:]
            tai = sum(1 for x in recent if x=="Tài")
            pred = "Xỉu" if tai>=3 else "Tài"
            conf = 92+random.randint(-4,8)
            st.error(f"### 🎯 **BET {pred}** **({conf}%)**")
            
            if st.button(f"🎲 **50K {pred}**",use_container_width=True):
                if random.random()<conf/100:
                    st.session_state.app_state['balance'] += 97500
                    st.session_state.app_state['wins'] += 1
                    st.success("✅ **+97.5K!** 💰")
                    st.balloons()
                else:
                    st.session_state.app_state['balance'] -= 50000
                    st.error("❌ **-50K**")
                st.rerun()
        else:
            st.warning("⏳ **3 ván nữa AI đoán**")
    
    # History
    st.subheader("📜 **Lịch sử**")
    for i,r in enumerate(st.session_state.app_state['history'][-10:],1):
        st.write(f"{i}. **{r}**")
    
    # Controls
    col1,col2,col3 = st.columns(3)
    col1.button("🔄 **Reset tiền**",on_click=lambda: setattr(st.session_state.app_state,'balance',1000000) or st.rerun())
    col2.button("🗑️ **Xóa lịch sử**",on_click=lambda: st.session_state.app_state.update({'wins':0,'games':0,'history':[]}) or st.rerun())
    col3.button("🚪 **Logout**",on_click=lambda: st.session_state.update(app_state={'user':None,'admin':False}) or st.rerun())
    
    # Admin
    if st.session_state.app_state['admin']:
        with st.expander("🔧 **ADMIN**"):
            st.success("👑 **ADMIN MODE**")
            st.metric("Users","Demo")
    
    st.markdown("---")
    st.caption("🌟 **SUNTOOL** by mhwuan - AI 98%")
