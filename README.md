# 🍯 Honeypot Compiler — Compiler Design & Security Pipeline

## Project Structure

```
honeypot/
├── app.py                  ← Flask backend (routes, auth, API)
├── compiler.py             ← Main Compiler Core (Lexer, Parser, AST, Codegen)
├── lexer.py                ← Phase 1: Lexical Analysis
├── parser.py               ← Phase 2: Syntax Analysis & AST Generation
├── semantic.py             ← Phase 3: Semantic Analysis & Symbol Tables
├── optimizer.py            ← Phase 4: AST Dead Code Elimination
├── transformer.py          ← Phase 5: Instrumentation (Honeypot Logic)
├── codegen.py              ← Phase 6: Code Generation
├── logger.py               ← Logs attack data to logs.json
├── logs.json               ← Auto-created, stores all attack logs
├── output_program.py       ← Auto-created after compilation
├── uploads/                ← Auto-created, stores uploaded files
└── templates/
    ├── login.html          ← Auth page (boot sequence + login form)
    ├── index.html          ← Compiler upload page
    ├── pipeline.html       ← Live pipeline showing all Compiler output steps
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
- Fully simulates a **compiler toolchain** implementing the following phases:
  1. **Lexical Analysis:** Tokenizes raw source code.
  2. **Parsing:** Implements a recursive descent parser to build an AST framework.
  3. **Semantic Analysis:** Extracts variables and creates a Symbol Table.
  4. **AST Optimization:** Eliminates dead code (DCE logic).
  5. **AST Transformation:** Walks the AST to instrument 'login' methods with honeypot captures.
  6. **Code Generation:** Flattens AST back to executable Python code.
- Captures the exact output of every distinct compilation phase.
- Seamless re-direction to the Pipeline to observe these steps dynamically.

### 🔍 Execution Pipeline Viewer (/pipeline)
- A dedicated diagnostic UI.
- Visually stepping through **Lexer** dumps, **AST structures**, **Symbol tables**, and **Final emitted code** in real-time.

### 📊 Dashboard (Attack Monitor)
- Live log table, auto-refreshes every 3s from `logs.json`.
- **Simulate Traffic:** A dedicated button to inject realistic randomized simulated attack payloads in the dashboard without manual terminal intervention.
- **Click any row** → detailed modal with:
  - Raw payload, source IP, classification
  - Step-by-step reasoning
  - Recommended mitigations
- **Log Management:** Delete logs directly from the modal view.
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

## How the Compiler Works

1. User uploads a source file (like the provided `example_login_script.py`).
2. `compiler.py` orchestrates the translation through 6 strict Compiler Phases.
3. Tokens, grammatically validated ASTs, and strict optimization metrics are generated.
4. During Phase 5 (Transformation), an implicit Honeypot Trap is woven into AST scope.
5. Code Generation builds an altered output variant.
6. The compiled results display securely in the dashboard.
7. Generating simulated traffic via the dashboard will populate the intrusion logs securely.

---

## Changing Credentials

Edit `app.py`, lines 14–15:
```python
VALID_USERNAME = "admin"        # ← change this
VALID_PASSWORD = "honeypot123"  # ← change this
```

---

*Built for college project — Honeypot Deception Engine v2.4*
