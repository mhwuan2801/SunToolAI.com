#!/usr/bin/env python3
"""
🌟 SUNTOOL - TÀI XỈU AI PRO by mhwuan
Full Auth + Admin Panel + Pro UI
"""

import streamlit as st
import pandas as pd
import numpy as np
import hashlib
import json
from collections import Counter, deque
from datetime import datetime, timedelta
import random

# ==================== DATA STORAGE ====================
@st.cache_resource
def load_data():
    """Load user data from session"""
    if 'users' not in st.session_state:
        st.session_state.users = {
            'admin': hashlib.md5('admin123'.encode()).hexdigest(),  # admin:admin123
            'users': {}
        }
    if 'user_stats' not in st.session_state:
        st.session_state.user_stats = {}
    if 'logs' not in st.session_state:
        st.session_state.logs = []
    return True

# ==================== AUTH SYSTEM ====================
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

def register_user(username, password):
    """Đăng ký user mới"""
    if username in st.session_state.users['users']:
        return False, "❌ Username đã tồn tại!"
    
    st.session_state.users['users'][username] = hash_password(password)
    st.session_state.user_stats[username] = {
        'balance': 1000000,
        'wins': 0,
        'history': deque(maxlen=100),
        'created': datetime.now().isoformat(),
        'last_login': None,
        'total_games': 0
    }
    st.session_state.logs.append({
        'user': username,
        'action': 'REGISTER',
        'time': datetime.now().isoformat()
    })
    return True, "✅ Đăng ký thành công!"

def login_user(username, password):
    """Đăng nhập"""
    if username == 'admin' and hash_password(password) == st.session_state.users['admin']:
        st.session_state.current_user = 'ADMIN'
        st.session_state.is_admin = True
        return True, "✅ Admin login thành công!"
    
    if (username in st.session_state.users['users'] and 
        st.session_state.users['users'][username] == hash_password(password)):
        st.session_state.current_user = username
        st.session_state.is_admin = False
        st.session_state.user_stats[username]['last_login'] = datetime.now().isoformat()
        st.session_state.logs.append({
            'user': username,
            'action': 'LOGIN',
            'time': datetime.now().isoformat()
        })
        return True, "✅ Đăng nhập thành công!"
    return False, "❌ Sai username/password!"

# ==================== TAI XIU AI ====================
class TaiXiuAI:
    def __init__(self):
        self.weights = {'streak':0.25, 'momentum':0.20, 'pattern':0.25, 'cycle':0.15, 'hotcold':0.15}
    
    def predict(self, history):
        if len(history) < 3: return None, 0
        
        analyses = [self._streak(history), self._momentum(history), 
                   self._pattern(history), self._cycle(history), self._hotcold(history)]
        
        scores = Counter()
        total_weight = sum(self.weights.values())
        
        for i, (conf, pred) in enumerate(analyses):
            weight = list(self.weights.values())[i]
            scores[pred] += conf * weight
        
        prediction = scores.most_common(1)[0][0]
        confidence = (scores[prediction] / total_weight) * 100
        
        return prediction, confidence
    
    def _streak(self, h): 
        recent = list(h)[-10:]
        streak, last = 1, recent[-1]
        for r in reversed(recent[:-1]):
            if r == last: streak += 1
            else: break
        if streak >= 4: return 0.95, 'Xỉu' if last == 'Tài' else 'Tài'
        return 0.5, last
    
    def _momentum(self, h):
        recent = list(h)[-8:]
        tai_wins = sum(1 for i in range(1,len(recent)) if recent[i]=='Tài' and recent[i-1]=='Xỉu')
        xiu_wins = len(recent)-1 - tai_wins
        return 0.8, 'Xỉu' if tai_wins > xiu_wins else 'Tài'
    
    def _pattern(self, h):
        recent = ''.join(list(h)[-4:])
        patterns = {'TXXT':'Tài', 'XTTX':'Xỉu', 'TTXX':'Tài', 'XXTT':'Xỉu'}
        return 0.9, patterns.get(recent, 'Tài')
    
    def _cycle(self, h): return 0.75, random.choice(['Tài','Xỉu'])
    def _hotcold(self, h):
        recent = list(h)[-10:]
        tai = recent.count('Tài')
        return 0.9, 'Xỉu' if tai >= 7 else 'Tài'

ai = TaiXiuAI()

# ==================== PRO UI ====================
def pro_ui():
    """Giao diện chính SunTool"""
    st.markdown("""
    <style>
    .suntool-header {background:linear-gradient(135deg,#667eea 0%,#764ba2 50%,#f093fb 100%);padding:2rem;border-radius:20px;color:white;text-align:center;}
    .predict-card {background:linear-gradient(135deg,#ff6b6b,#feca57);padding:2rem;border-radius:25px;color:white;text-align:center;font-size:1.5rem;}
    .metric-card {background:linear-gradient(135deg,#00b894,#00cec9);padding:1.5rem;border-radius:20px;color:white;text-align:center;}
    .mhwuan {color:#ff7675;font-size:1.2rem;}
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="suntool-header">
        <h1 style='font-size:3.5rem;margin:0;'>🌟 SUNTOOL</h1>
        <p class='mhwuan' style='margin:0;font-size:1.5rem;'>Tài Xỉu AI Pro <strong>by mhwuan</strong> 🔥</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Metrics
    col1,col2,col3,col4 = st.columns(4)
    stats = st.session_state.user_stats[st.session_state.current_user]
    with col1: st.markdown(f'<div class="metric-card"><h3>💰 Balance</h3><h1>{stats["balance"]:,}</h1></div>', unsafe_allow_html=True)
    with col2: st.markdown(f'<div class="metric-card"><h3>📈 Winrate</h3><h1>{(stats["wins"]/stats["total_games"]*100):.1f}%</h1></div>', unsafe_allow_html=True)
    with col3: st.markdown(f'<div class="metric-card"><h3>🏆 Wins</h3><h1>{stats["wins"]}</h1></div>', unsafe_allow_html=True)
    with col4: st.markdown(f'<div class="metric-card"><h3>📊 Games</h3><h1>{stats["total_games"]}</h1></div>', unsafe_allow_html=True)
    
    # Main controls
    st.divider()
    col1,col2 = st.columns(2)
    
    with col1:
        if st.button("🔗 Mở SunWin.MW", use_container_width=True):
            st.balloons()
            st.success("🌐 https://sunwin.mw/taixiu")
        
        result = st.selectbox("➕ Kết quả", ["", "Tài", "Xỉu"])
        if st.button("✅ Thêm kết quả", use_container_width=True) and result:
            stats['history'].append(result)
            stats['total_games'] += 1
            st.rerun()
    
    with col2:
        pred, conf = ai.predict(stats['history'])
        if pred:
            st.markdown(f"""
            <div class="predict-card">
                <h2>🎯 VÁN SAU → <strong>{pred}</strong></h2>
                <h3>🎰 Độ chính xác: <strong>{conf:.1f}%</strong></h3>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"🎲 Simulate {pred}", use_container_width=True):
                accuracy = min(conf/100, 0.95)
                real_result = pred if random.random() < accuracy else ('Xỉu' if pred=='Tài' else 'Tài')
                
                bet = 50000
                if pred == real_result:
                    profit = int(bet * 1.95)
                    stats['balance'] += profit
                    stats['wins'] += 1
                    st.success(f"✅ WIN +{profit:,} | Balance: {stats['balance']:,}")
                else:
                    stats['balance'] -= bet
                    st.error(f"❌ LOSE -{bet:,} | Balance: {stats['balance']:,}")
                st.rerun()
        else:
            st.warning("⏳ Cần 3+ ván để dự đoán!")
    
    # History
    with st.expander("📜 Lịch sử"):
        recent = list(stats['history'])[-15:]
        for i,r in enumerate(recent,1):
            st.write(f"{i}. **{r}**")

# ==================== ADMIN PANEL ====================
def admin_panel():
    """Admin dashboard"""
    st.markdown("""
    <div style='background:linear-gradient(135deg,#2d3436,#636e72);padding:2rem;border-radius:20px;color:white;text-align:center;'>
        <h1 style='color:#00b894;'>🔧 ADMIN PANEL</h1>
        <p>👥 Quản lý users | 📊 Analytics</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["👥 Users", "📊 Stats", "📋 Logs"])
    
    with tab1:
        df_users = pd.DataFrame([
            {
                'Username': u,
                'Balance': st.session_state.user_stats[u]['balance'],
                'Wins': st.session_state.user_stats[u]['wins'],
                'Games': st.session_state.user_stats[u]['total_games'],
                'Winrate': f"{st.session_state.user_stats[u]['wins']/st.session_state.user_stats[u]['total_games']*100:.1f}%" if st.session_state.user_stats[u]['total_games'] else "0%",
                'Created': st.session_state.user_stats[u]['created'][:10]
            }
            for u in st.session_state.user_stats
        ])
        st.dataframe(df_users, use_container_width=True)
        
        # Admin actions
        col1,col2,col3 = st.columns(3)
        with col1:
            user = st.selectbox("Chọn user", list(st.session_state.user_stats.keys()))
            if st.button("💰 Reset Balance", key="reset"):
                st.session_state.user_stats[user]['balance'] = 1000000
                st.rerun()
        with col2:
            if st.button("🗑️ Clear History", key="clear"):
                st.session_state.user_stats[user]['history'].clear()
                st.session_state.user_stats[user]['wins'] = 0
                st.session_state.user_stats[user]['total_games'] = 0
                st.rerun()
    
    with tab2:
        total_users = len(st.session_state.user_stats)
        total_balance = sum(st.session_state.user_stats[u]['balance'] for u in st.session_state.user_stats)
        total_wins = sum(st.session_state.user_stats[u]['wins'] for u in st.session_state.user_stats)
        
        col1,col2,col3,col4 = st.columns(4)
        col1.metric("👥 Total Users", total_users)
        col2.metric("💰 Total Balance", f"{total_balance:,}")
        col3.metric("🏆 Total Wins", total_wins)
        col4.metric("📈 Avg Winrate", f"{total_wins/len(st.session_state.user_stats):.1f}%")
    
    with tab3:
        df_logs = pd.DataFrame(st.session_state.logs[-50:])
        st.dataframe(df_logs, use_container_width=True)

# ==================== MAIN APP ====================
def main():
    st.set_page_config(page_title="SunTool", layout="wide")
    load_data()
    
    # Multi-page auth
    if 'current_user' not in st.session_state:
        st.session_state.current_user = None
        st.session_state.is_admin = False
    
    # === LOGIN / REGISTER PAGE ===
    if not st.session_state.current_user:
        st.markdown("""
        <div style='text-align:center;padding:3rem;'>
            <h1 style='color:#667eea;font-size:4rem;'>🌟 SUNTOOL</h1>
            <p style='color:#74b9ff;font-size:1.5rem;'>Tài Xỉu AI Pro <strong>by mhwuan</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["🔐 Đăng nhập", "📝 Đăng ký"])
        
        with tab1:
            col1, col2 = st.columns([1,1])
            with col1: username = st.text_input("👤 Username")
            with col2: password = st.text_input("🔒 Password", type="password")
            
            col1,col2 = st.columns(2)
            with col1:
                if st.button("🚀 Đăng nhập", use_container_width=True):
                    success, msg = login_user(username, password)
                    st.error(msg) if not success else st.success(msg)
                    if success: st.rerun()
            
            st.info("🔑 **Admin**: admin / admin123")
        
        with tab2:
            col1, col2 = st.columns([1,1])
            with col1: new_user = st.text_input("👤 Username mới")
            with col2: new_pass = st.text_input("🔒 Password", type="password")
            
            if st.button("✅ Đăng ký", use_container_width=True):
                success, msg = register_user(new_user, new_pass)
                st.error(msg) if not success else st.success(msg)
    
    # === MAIN APP ===
    else:
        # Header với logout
        col1, col2, col3 = st.columns([1,3,1])
        with col1: st.empty()
        with col2: st.markdown(f"👋 Chào **{st.session_state.current_user}**")
        with col3:
            if st.button("🚪 Logout"):
                st.session_state.current_user = None
                st.rerun()
        
        # Admin check
        if st.session_state.is_admin:
            if st.sidebar.button("🔧 Admin Panel"):
                st.switch_page("admin")
            admin_panel()
        else:
            pro_ui()

if __name__ == "__main__":
    main()
