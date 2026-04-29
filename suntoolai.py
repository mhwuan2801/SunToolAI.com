#!/usr/bin/env python3
"""
🌟 SUNTOOLAI - TÀI XỈU PREDICTOR BY MHWUAN
SunWin.MW Auto Predictor + Admin Panel
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import random
import json
import os
from datetime import datetime
import hashlib

app = Flask(__name__)
app.secret_key = 'suntoolai-mhwuan-sunwin-2024-v2'

# ==================== DATA STORAGE ====================
users = {}
history = []
balance = 1000000
wins = 0

# Admin credentials
ADMIN_USER = 'admin123'
ADMIN_PASS = '123123'

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_data():
    global users, history, balance, wins
    try:
        if os.path.exists('suntoolai_data.json'):
            with open('suntoolai_data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                users = data.get('users', {})
                history = data.get('history', [])
                balance = data.get('balance', 1000000)
                wins = data.get('wins', 0)
    except:
        pass

def save_data():
    data = {
        'users': users,
        'history': history[-100:],  # Giữ 100 ván gần nhất
        'balance': balance,
        'wins': wins,
        'timestamp': datetime.now().isoformat()
    }
    with open('suntoolai_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def is_admin():
    return session.get('user') == ADMIN_USER

# ==================== ROUTES ====================

@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        
        # Admin login
        if username == ADMIN_USER and password == ADMIN_PASS:
            session['user'] = username
            session['is_admin'] = True
            flash('👑 Đăng nhập Admin SunToolAI thành công!')
            save_data()
            return redirect(url_for('admin'))
        
        # User login
        hashed_pass = hash_password(password)
        if username in users and users[username]['password'] == hashed_pass:
            session['user'] = username
            session['is_admin'] = False
            flash(f'🎉 Chào {username} - SunToolAI ready!')
            save_data()
            return redirect(url_for('dashboard'))
        
        flash('❌ Sai tài khoản/mật khẩu!')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        
        if len(username) < 3:
            flash('❌ Tên ≥ 3 ký tự!')
            return render_template('register.html')
        
        if username in users:
            flash('❌ Tài khoản đã tồn tại!')
            return render_template('register.html')
        
        users[username] = {
            'password': hash_password(password),
            'created_at': datetime.now().strftime('%d/%m/%Y %H:%M'),
            'predictions': 0,
            'wins': 0,
            'winrate': '0%'
        }
        save_data()
        flash('✅ Đăng ký SunToolAI thành công! Đăng nhập ngay.')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    winrate = (wins / len(history) * 100) if history else 0
    stats = {
        'user': session['user'],
        'history_count': len(history),
        'balance': f'{balance:,}',
        'wins': wins,
        'winrate': f'{winrate:.1f}%'
    }
    return render_template('dashboard.html', stats=stats)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    global history, balance, wins
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'add_result':
            result = request.form['result'].strip().title()
            if result in ['Tài', 'Xỉu']:
                history.append(result)
                users[session['user']]['predictions'] += 1
                save_data()
                return jsonify({
                    'success': True, 
                    'message': f'✅ Đã thêm {result}',
                    'total': len(history)
                })
        
        elif action == 'predict':
            pred = suntoolai_predict()
            return jsonify({'prediction': pred})
        
        elif action == 'simulate':
            real_result = random.choices(['Tài', 'Xỉu'], weights=[48, 52])[0]
            ai_pred = suntoolai_predict()
            bet = 50000
            
            if ai_pred['result'] == real_result:
                profit = int(bet * 1.95)
                balance += profit
                wins += 1
                users[session['user']]['wins'] += 1
                save_data()
                return jsonify({
                    'win': True,
                    'pred': ai_pred['result'],
                    'result': real_result,
                    'profit': f'+{profit:,}',
                    'balance': f'{balance:,}',
                    'winrate': f'{wins/len(history)*100:.1f}%',
                    'streak': ai_pred['streak']
                })
            else:
                balance -= bet
                save_data()
                return jsonify({
                    'win': False,
                    'pred': ai_pred['result'],
                    'result': real_result,
                    'loss': f'-{bet:,}',
                    'balance': f'{balance:,}',
                    'winrate': f'{wins/len(history)*100:.1f}%',
                    'streak': ai_pred['streak']
                })
    
    return render_template('predict.html')

@app.route('/admin')
def admin():
    if not is_admin():
        flash('❌ Không có quyền Admin!')
        return redirect(url_for('login'))
    
    total_users = len(users)
    winrate = (wins / len(history) * 100) if history else 0
    
    stats = {
        'total_users': total_users,
        'active_users': len([u for u in users if users[u]['predictions'] > 0]),
        'history_count': len(history),
        'sunwin_balance': f'{balance:,} VNĐ',
        'sunwin_wins': wins,
        'sunwin_winrate': f'{winrate:.1f}%',
        'recent_users': sorted(users.items(), key=lambda x: x[1]['predictions'], reverse=True)[:10],
        'top_predictor': max(users.items(), key=lambda x: x[1]['predictions']) if users else None
    }
    
    return render_template('admin.html', stats=stats)

@app.route('/api/suntoolai')
def api_suntoolai():
    return jsonify({
        'status': 'active',
        'name': 'SunToolAI by mhwuan',
        'version': '2.0',
        'users': len(users),
        'history': len(history),
        'next_predict': suntoolai_predict()['result']
    })

# ==================== SUNTOOLAI AI ENGINE ====================

def suntoolai_predict():
    """🔥 SunToolAI Advanced Predict Engine"""
    global history
    
    if len(history) < 3:
        return {'result': 'Cần 3+ ván', 'confidence': '0%', 'streak': 0}
    
    recent = history[-15:]  # Analyze 15 games
    tai_count = recent.count('Tài')
    xiu_count = recent.count('Xỉu')
    
    # Streak detection
    streak = 1
    last_result = recent[-1]
    for i in range(2, len(recent)+1):
        if recent[-i] == last_result:
            streak += 1
        else:
            break
    
    # 🎯 SunToolAI Decision Matrix
    if streak >= 5:
        prediction = 'Xỉu' if last_result == 'Tài' else 'Tài'
        confidence = 96
    elif streak >= 3:
        prediction = 'Xỉu' if last_result == 'Tài' else 'Tài'
        confidence = 92
    elif tai_count >= 9:
        prediction = 'Xỉu'
        confidence = 90
    elif xiu_count >= 9:
        prediction = 'Tài'
        confidence = 90
    elif abs(tai_count - xiu_count) <= 2:
        # 50/50 -> Pattern break
        prediction = 'Tài' if recent[-2] == 'Xỉu' else 'Xỉu'
        confidence = 82
    else:
        prediction = 'Tài' if tai_count >= xiu_count else 'Xỉu'
        confidence = 85
    
    return {
        'result': prediction,
        'confidence': f'{confidence}%',
        'streak': streak,
        'tai': tai_count,
        'xiu': xiu_count,
        'analysis': f'Streak: {streak} | T:{tai_count} X:{xiu_count}'
    }

if __name__ == '__main__':
    load_data()
    print("""
🌟🌟🌟 SUNTOOLAI v2.0 BY MHWUAN 🌟🌟🌟
==================================================
📱 Web: http://localhost:5000
👑 Admin: admin123 / 123123
💾 Data: suntoolai_data.json (auto-save)
==================================================
    """)
    app.run(debug=False, host='0.0.0.0', port=5000)
