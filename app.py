from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os
import json
import random
from compiler import compile_code
from lexer import CompilerSyntaxError
from logger import log_attack

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



@app.route('/pipeline')
def pipeline_view():
    if not logged_in():
        return redirect(url_for('login'))
    return render_template('pipeline.html')

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
    
    file = request.files.get('file')
    code_content = request.form.get('code')
    
    if code_content is not None:
        path = os.path.join(UPLOAD_FOLDER, "temp_code.py")
        with open(path, "w", encoding="utf-8") as f:
            f.write(code_content)
    elif file:
        path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(path)
    else:
        return jsonify({"status": "error", "message": "No file or code provided"}), 400
    
    try:
        trace_data = compile_code(path)
    except CompilerSyntaxError as e:
        return jsonify({
            "status": "error",
            "message": f"{e.message} at line {e.line}"
        }), 400
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
        
    return jsonify({"status": "success", "trace": trace_data})

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


@app.route('/api/simulate', methods=['POST'])
def simulate_traffic():
    if not logged_in():
        return jsonify({"status": "unauthorized"}), 401
    
    attack_payloads = [
        "' OR '1'='1",
        "admin'--",
        "../../../../etc/passwd",
        "<script>alert(1)</script>",
        "UNION SELECT null, version()",
        "/windows/system32/cmd.exe",
        "1; DROP TABLE users",
        "admin' OR 1=1#"
    ]
    
    num_attacks = random.randint(2, 4)
    selected_attacks = random.sample(attack_payloads, num_attacks)
    
    for payload in selected_attacks:
        log_attack(payload)
        
    return jsonify({"status": "success", "count": num_attacks})

def is_suspicious(input_str):
    input_str_lower = input_str.lower()
    
    # SQL Injection patterns
    if any(x in input_str_lower for x in ["' or", "select ", "'--", "union", "drop table", "admin'"]):
        return True
    
    # Path Traversal patterns
    if any(x in input_str_lower for x in ["../", "..\\", "/etc/", "/windows/"]):
        return True
        
    # XSS or Command Injection patterns
    if any(x in input_str_lower for x in ["<script>", "alert(", "cmd.exe", "exec("]):
        return True
        
    return False

@app.route('/api/test_attack', methods=['POST'])
def test_attack():
    if not logged_in():
        return jsonify({"status": "unauthorized"}), 401
    
    data = request.get_json(silent=True) or {}
    user_input = data.get('input', '').strip()
    
    if user_input:
        if is_suspicious(user_input):
            log_attack(user_input)
            return jsonify({"status": "success", "message": "Suspicious command detected and logged."})
        else:
            return jsonify({"status": "success", "message": "No harm detected."})
    return jsonify({"status": "error", "message": "No input provided"}), 400

@app.route('/api/delete_log', methods=['POST'])
def delete_log():
    if not logged_in():
        return jsonify({"status": "unauthorized"}), 401
        
    data = request.get_json(silent=True) or {}
    target_time = data.get('time')
    target_input = data.get('input')
    
    if not target_time or not target_input:
        return jsonify({"status": "error", "message": "Missing log identifiers"}), 400
        
    LOG_FILE = "logs.json"
    try:
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            logs = json.load(f)
            
        # Filter out the matching log (returns all logs that DON'T match)
        updated_logs = [log for log in logs if not (log.get("time") == target_time and log.get("input") == target_input)]
        
        with open(LOG_FILE, 'w', encoding='utf-8') as f:
            json.dump(updated_logs, f, indent=4)
            
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# ─── RUN ─────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True, port=9876)
