from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os
import json
from compiler import compile_code

app = Flask(__name__)

# ─── SECRET KEY (used to sign session cookies) ───────────────────────────────
# Change this to something secret before real deployment!
app.secret_key = "honeypot_secret_key_change_this"

UPLOAD_FOLDER = "uploads"
LOG_FILE      = "logs.json"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ─── HARDCODED CREDENTIALS ───────────────────────────────────────────────────
# Username & password stored right here in the code (plain-text for demo).
# In a real project you would hash passwords with bcrypt and store in a DB.
VALID_USERNAME = "admin"
VALID_PASSWORD = "honeypot123"

# ─── AUTH HELPER ─────────────────────────────────────────────────────────────
def logged_in():
    return session.get("user") is not None


# ─── ROUTES ──────────────────────────────────────────────────────────────────

@app.route('/')
def home():
    if not logged_in():
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if not logged_in():
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/analytics')
def analytics():
    if not logged_in():
        return redirect(url_for('login'))
    return render_template('analytics.html')

@app.route('/threat-map')
def threat_map():
    if not logged_in():
        return redirect(url_for('login'))
    return render_template('threat-map.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Already logged in → skip to dashboard
    if logged_in():
        return redirect(url_for('dashboard'))

    error = None
    if request.method == 'POST':
        data     = request.get_json(silent=True) or {}
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()

        if username == VALID_USERNAME and password == VALID_PASSWORD:
            session['user'] = username          # ← this is where login is "stored"
            return jsonify({"status": "ok"})
        else:
            return jsonify({"status": "error", "message": "Invalid credentials"}), 401

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# ─── API ──────────────────────────────────────────────────────────────────────

@app.route('/compile', methods=['POST'])
def compile_file():
    if not logged_in():
        return jsonify({"status": "unauthorized"}), 401
    file = request.files['file']
    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)
    compile_code(path)
    return jsonify({"status": "success"})

@app.route('/logs')
def get_logs():
    if not logged_in():
        return jsonify({"status": "unauthorized"}), 401
    try:
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            logs = json.load(f)
    except:
        logs = []
    return jsonify(logs)

@app.route('/whoami')
def whoami():
    """Returns the currently logged-in username — used by the frontend."""
    if logged_in():
        return jsonify({"user": session['user']})
    return jsonify({"user": None}), 401


# ─── RUN ─────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True)
