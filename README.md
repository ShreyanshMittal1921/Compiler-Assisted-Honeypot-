# 🍯 Honeypot Compiler — Setup & Documentation

## Project Structure

```
honeypot/
├── app.py                  ← Flask backend (routes, auth, API)
├── compiler.py             ← Compiles uploaded Python files
├── honeypot_engine.py      ← Injects honeypot traps into code
├── logger.py               ← Logs attack data to logs.json
├── logs.json               ← Auto-created, stores all attack logs
├── output_program.py       ← Auto-created after compilation
├── uploads/                ← Auto-created, stores uploaded files
└── templates/
    ├── login.html          ← Auth page (boot sequence + login form)
    ├── index.html          ← Compiler upload page
    ├── dashboard.html      ← Live attack monitor + detail modal
    ├── analytics.html      ← Charts, heatmap, payload rankings
    └── threat-map.html     ← Animated live global threat map
```

---

## Quick Start

### 1. Install dependencies
```bash
pip install flask
```

### 2. Run the server
```bash
python app.py
```

### 3. Open in browser
```
http://127.0.0.1:5000
```

---

## Login Credentials

| Field    | Value          |
|----------|----------------|
| Username | `admin`        |
| Password | `honeypot123`  |

> **Where is login data stored?**
> Credentials are hardcoded in `app.py` (lines 14–15).
> On successful login, Flask stores the username in a **server-side session cookie**
> (signed with `app.secret_key`). No database needed. The session lasts until
> the user clicks **Sign Out** or the browser closes.

---

## Navigation Flow

```
Login ──► Compiler ──► (upload .py file)
                │
                ▼
           Dashboard  ←──► Analytics
                │
                ▼
           Threat Map
```

Every page has:
- **Top nav bar** with links to all pages
- **Active page** highlighted in red
- **Operator name** displayed (pulled from session)
- **⏻ SIGN OUT** button on every page

---

## Features

### 🔐 Login Page
- Animated terminal boot sequence on load
- Flask session-based authentication
- Wrong credentials → error message

### ⚙️ Compiler
- Upload any `.py` file
- Animated multi-step progress bar
- Redirects to Dashboard after compile
- Honeypot traps injected around `login` calls

### 📊 Dashboard (Attack Monitor)
- Live log table, auto-refreshes every 3s from `/logs`
- **Click any row** → detailed modal with:
  - Raw payload, source IP, classification
  - Step-by-step reasoning
  - Recommended mitigations
- Filter by SQL / Path / Suspicious
- Export logs as CSV
- **Stealth mode** toggle (dims UI)

### 📈 Analytics
- 24h frequency line chart (Chart.js)
- Attack type donut chart
- Hourly heatmap
- Top payloads ranking bar
- Time filter: 1H / 6H / 24H / 7D

### 🗺️ Threat Map
- Animated SVG world map
- Live attack arcs from source → honeypot
- Real-time feed sidebar with IP + type
- Top source countries ranked

---

## How the Honeypot Works

1. User uploads a `.py` source file
2. `compiler.py` reads it line by line
3. `honeypot_engine.py` detects any line containing `"login"`
4. A trap is injected after that line — it captures user input
5. `logger.py` saves the captured data to `logs.json`
6. Dashboard reads `logs.json` every 3 seconds and displays attacks

---

## Changing Credentials

Edit `app.py`, lines 14–15:
```python
VALID_USERNAME = "admin"        # ← change this
VALID_PASSWORD = "honeypot123"  # ← change this
```

---

*Built for college project — Honeypot Deception Engine v2.4*
