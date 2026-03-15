from flask import Flask, render_template, request, jsonify, redirect, url_for, session, send_from_directory
import os

app = Flask(__name__, template_folder='.', static_folder='static')
app.secret_key = 'library2026secretkey'

users = {}

# ── Images ───────────────────────────────────────────────────────────────────
@app.route('/images/<filename>')
def images(filename):
    return send_from_directory('.', filename)

# ── Welcome page (no login needed) ───────────────────────────────────────────
@app.route('/')
def home():
    return render_template('wel.html')

# ── Auth ─────────────────────────────────────────────────────────────────────
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        if username in users and users[username]['password'] == password:
            session['username'] = username
            session['firstname'] = users[username].get('firstname', username)
            return redirect(url_for('dashboard'))
        return render_template('signin.html', error=True)
    return render_template('signin.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        if not username or not password:
            return render_template('register.html', error="Injiza username na password.")
        if username in users:
            return render_template('register.html', error="Username irashobora gukoreshwa.")
        users[username] = {
            'firstname':  request.form.get('firstname', ''),
            'secondname': request.form.get('secondname', ''),
            'email':      request.form.get('email', ''),
            'password':   password
        }
        return redirect(url_for('signin'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# ── Dashboard (login required) ────────────────────────────────────────────────
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('signin'))
    return render_template('dashboard.html', username=session.get('firstname', session['username']))

# ── Library main page (login required) ───────────────────────────────────────
@app.route('/library')
def index():
    if 'username' not in session:
        return redirect(url_for('signin'))
    return render_template('index.html')

# ── Subject pages (login required) ───────────────────────────────────────────
@app.route('/library/<filename>')
def library(filename):
    if 'username' not in session:
        return redirect(url_for('signin'))
    library_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'library')
    filepath = os.path.join(library_folder, filename)
    if os.path.exists(filepath):
        return send_from_directory(library_folder, filename)
    root_folder = os.path.dirname(os.path.abspath(__file__))
    root_path = os.path.join(root_folder, filename)
    if os.path.exists(root_path):
        return send_from_directory(root_folder, filename)
    return f"<h2 style='font-family:sans-serif;padding:40px'>❌ '{filename}' not found.<br><br><a href='/dashboard'>← Dashboard</a></h2>", 404

# ── Contact ───────────────────────────────────────────────────────────────────
@app.route('/submit-form', methods=['POST'])
def submit_form():
    name    = request.form.get('name', 'Anonymous')
    email   = request.form.get('email', '')
    message = request.form.get('message', '')
    print(f"[Mail] {name} <{email}>: {message}")
    return "Thank you! We will get back to you soon.", 200

@app.route('/api/books')
def get_books():
    return jsonify({"status": "ok", "message": "Digital Library API running!"})

# ── Run ───────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print("=" * 50)
    print("  📚  Digital Library — Flask Server")
    print("  URL : http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, port=5000)