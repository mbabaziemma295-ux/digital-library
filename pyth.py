from flask import Flask, render_template, request, jsonify, redirect, url_for, session, send_from_directory, Response
import os
import urllib.request
import sqlite3
from datetime import timedelta

app = Flask(__name__, template_folder='.', static_folder='static')
app.secret_key = 'library2026secretkey'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True

# ── SQLite Config ─────────────────────────────────────────────────────────────
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'library.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id        INTEGER PRIMARY KEY AUTOINCREMENT,
        username  TEXT UNIQUE NOT NULL,
        password  TEXT NOT NULL,
        firstname TEXT,
        secondname TEXT,
        email     TEXT UNIQUE
    )''')
    # Books table
    c.execute('''CREATE TABLE IF NOT EXISTS books (
        id           INTEGER PRIMARY KEY AUTOINCREMENT,
        title        TEXT NOT NULL,
        author       TEXT,
        category     TEXT,
        description  TEXT,
        read_url     TEXT,
        download_url TEXT
    )''')
    # Downloads table
    c.execute('''CREATE TABLE IF NOT EXISTS downloads (
        id      INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        book_id INTEGER,
        ts      DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    # Insert sample books if empty
    c.execute("SELECT COUNT(*) FROM books")
    if c.fetchone()[0] == 0:
        books = [
            ("Pride and Prejudice",      "Jane Austen",      "Novel",      "A classic romance novel.",                         "https://www.gutenberg.org/files/1342/1342-h/1342-h.htm",   "https://www.gutenberg.org/ebooks/1342.epub.images"),
            ("Frankenstein",             "Mary Shelley",     "Novel",      "The story of the modern Prometheus.",               "https://www.gutenberg.org/files/84/84-h/84-h.htm",         "https://www.gutenberg.org/ebooks/84.epub.images"),
            ("The Great Gatsby",         "F. Scott Fitzgerald","Novel",    "Jazz Age decadence and the American Dream.",        "https://www.gutenberg.org/files/64317/64317-h/64317-h.htm","https://www.gutenberg.org/ebooks/64317.epub.images"),
            ("Moby Dick",                "Herman Melville",  "Novel",      "The obsessive quest of Captain Ahab.",              "https://www.gutenberg.org/files/2701/2701-h/2701-h.htm",   "https://www.gutenberg.org/ebooks/2701.epub.images"),
            ("The Adventures of Tom Sawyer","Mark Twain",    "Novel",      "Adventures of a young boy in Missouri.",            "https://www.gutenberg.org/files/74/74-h/74-h.htm",         "https://www.gutenberg.org/ebooks/74.epub.images"),
            ("A Tale of Two Cities",     "Charles Dickens",  "Novel",      "Set during the French Revolution.",                 "https://www.gutenberg.org/files/98/98-h/98-h.htm",         "https://www.gutenberg.org/ebooks/98.epub.images"),
            ("Jane Eyre",                "Charlotte Bronte", "Novel",      "A governess and her mysterious employer.",          "https://www.gutenberg.org/files/1260/1260-h/1260-h.htm",   "https://www.gutenberg.org/ebooks/1260.epub.images"),
            ("Dracula",                  "Bram Stoker",      "Novel",      "The iconic vampire horror story.",                  "https://www.gutenberg.org/files/345/345-h/345-h.htm",      "https://www.gutenberg.org/ebooks/345.epub.images"),
            ("The Picture of Dorian Gray","Oscar Wilde",     "Novel",      "A portrait ages while its subject stays young.",    "https://www.gutenberg.org/files/174/174-h/174-h.htm",      "https://www.gutenberg.org/ebooks/174.epub.images"),
            ("Wuthering Heights",        "Emily Bronte",     "Novel",      "A dark tale of love and revenge on the moors.",     "https://www.gutenberg.org/files/768/768-h/768-h.htm",      "https://www.gutenberg.org/ebooks/768.epub.images"),
            ("Think and Grow Rich",      "Napoleon Hill",    "Motivation", "Principles of personal success and wealth.",        "https://www.gutenberg.org/files/1232/1232-h/1232-h.htm",   "https://www.gutenberg.org/ebooks/1232.epub.images"),
            ("As a Man Thinketh",        "James Allen",      "Motivation", "The power of thought in shaping your life.",        "https://www.gutenberg.org/files/4507/4507-h/4507-h.htm",   "https://www.gutenberg.org/ebooks/4507.epub.images"),
            ("The Art of War",           "Sun Tzu",          "Motivation", "Ancient wisdom for modern strategy.",               "https://www.gutenberg.org/files/132/132-h/132-h.htm",      "https://www.gutenberg.org/ebooks/132.epub.images"),
            ("Meditations",              "Marcus Aurelius",  "Philosophy", "Stoic philosophy from a Roman emperor.",            "https://www.gutenberg.org/files/2680/2680-h/2680-h.htm",   "https://www.gutenberg.org/ebooks/2680.epub.images"),
            ("The Republic",             "Plato",            "Philosophy", "Plato's dialogue on justice and the ideal state.",  "https://www.gutenberg.org/files/1497/1497-h/1497-h.htm",   "https://www.gutenberg.org/ebooks/1497.epub.images"),
            ("Autobiography of Benjamin Franklin","Benjamin Franklin","Biography","Life story of one of America's founders.", "https://www.gutenberg.org/files/20203/20203-h/20203-h.htm","https://www.gutenberg.org/ebooks/20203.epub.images"),
            ("The Power of Now",         "Eckhart Tolle",    "Self-Help",  "Living in the present moment.",                     "https://www.gutenberg.org/files/21765/21765-h/21765-h.htm","https://www.gutenberg.org/ebooks/21765.epub.images"),
            ("Walden",                   "Henry David Thoreau","Self-Help","Simple living in natural surroundings.",            "https://www.gutenberg.org/files/205/205-h/205-h.htm",      "https://www.gutenberg.org/ebooks/205.epub.images"),
        ]
        c.executemany(
            "INSERT INTO books (title, author, category, description, read_url, download_url) VALUES (?,?,?,?,?,?)",
            books
        )
    conn.commit()
    conn.close()
    print("[DB] SQLite database ready →", DB_PATH)

# ── Images ────────────────────────────────────────────────────────────────────
@app.route('/images/<filename>')
def images(filename):
    return send_from_directory('.', filename)

# ── Welcome ───────────────────────────────────────────────────────────────────
@app.route('/')
def home():
    return render_template('wel.html')

# ── Auth ──────────────────────────────────────────────────────────────────────
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if 'username' in session and request.method == 'GET':
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE username=? AND password=?", (username, password)
        ).fetchone()
        conn.close()
        if user:
            session.permanent = True
            session['username']  = user['username']
            session['firstname'] = user['firstname'] or username
            return redirect(url_for('dashboard'))
        return render_template('signin.html', error=True)
    return render_template('signin.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'username' in session:
        return redirect(url_for('signin'))
    if request.method == 'POST':
        username         = request.form.get('username', '').strip()
        password         = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        firstname        = request.form.get('firstname', '').strip()
        secondname       = request.form.get('secondname', '').strip()
        email            = request.form.get('email', '').strip()

        if not firstname or not secondname:
            return render_template('register.html', error="Injiza amazina yose (First & Last name).")
        if not email or '@' not in email:
            return render_template('register.html', error="Injiza email ifite @.")
        if not username or ' ' in username:
            return render_template('register.html', error="Username ntagomba kugira utuzimu.")
        if len(password) < 6:
            return render_template('register.html', error="Password igomba kuba nibura inyuguti 6.")
        if password != confirm_password:
            return render_template('register.html', error="Passwords zitatanye — gerageza nanone.")

        conn = get_db()
        try:
            conn.execute(
                "INSERT INTO users (username, password, firstname, secondname, email) VALUES (?,?,?,?,?)",
                (username, password, firstname, secondname, email)
            )
            conn.commit()
            conn.close()
            return redirect(url_for('signin'))
        except sqlite3.IntegrityError:
            conn.close()
            return render_template('register.html', error="Username cyangwa email birasanzwe bifashwe.")
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# ── Dashboard ─────────────────────────────────────────────────────────────────
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('signin'))
    return render_template('dashboard.html', username=session.get('firstname', session['username']))

# ── Library ───────────────────────────────────────────────────────────────────
@app.route('/library')
def index():
    if 'username' not in session:
        return redirect(url_for('signin'))
    return render_template('index.html')

@app.route('/api/books')
def api_books():
    if 'username' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    conn = get_db()
    category = request.args.get('category', '')
    search   = request.args.get('search', '')
    if category and category != 'All':
        books = conn.execute("SELECT * FROM books WHERE category=? ORDER BY title", (category,)).fetchall()
    elif search:
        books = conn.execute(
            "SELECT * FROM books WHERE title LIKE ? OR author LIKE ?",
            (f'%{search}%', f'%{search}%')
        ).fetchall()
    else:
        books = conn.execute("SELECT * FROM books ORDER BY category, title").fetchall()
    conn.close()
    return jsonify([dict(b) for b in books])

# ── Proxy Download ────────────────────────────────────────────────────────────
@app.route('/proxy-download')
def proxy_download():
    if not session.get('username'):
        return redirect(url_for('signin'))
    url   = request.args.get('url', '')
    title = request.args.get('title', 'book')
    if not url or 'gutenberg.org' not in url:
        return "Invalid URL", 400
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
        ext      = 'epub' if 'epub' in url else 'txt'
        filename = f"{title}.{ext}"
        mimetype = 'application/epub+zip' if ext == 'epub' else 'text/plain'
        return Response(data, mimetype=mimetype,
                        headers={'Content-Disposition': f'attachment; filename="{filename}"',
                                 'Content-Length': str(len(data))})
    except Exception as e:
        print(f"[Download Error] {e}")
        return redirect(url)

# ── Download via DB ───────────────────────────────────────────────────────────
@app.route('/download/<int:book_id>')
def download_book(book_id):
    if 'username' not in session:
        return redirect(url_for('signin'))
    conn = get_db()
    book = conn.execute("SELECT * FROM books WHERE id=?", (book_id,)).fetchone()
    conn.close()
    if book:
        return redirect(book['download_url'] or book['read_url'] or '/library')
    return redirect(url_for('index'))

# ── Subject pages ─────────────────────────────────────────────────────────────
@app.route('/library/<filename>')
def library(filename):
    if 'username' not in session:
        return redirect(url_for('signin'))
    library_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'library')
    if os.path.exists(os.path.join(library_folder, filename)):
        return send_from_directory(library_folder, filename)
    root_folder = os.path.dirname(os.path.abspath(__file__))
    if os.path.exists(os.path.join(root_folder, filename)):
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

# ── Run ───────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    init_db()
    print("=" * 50)
    print("  📚  Digital Library — Flask + SQLite")
    print("  URL : http://localhost:5000")
    print("=" * 50)
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))