from flask import Flask, request, jsonify, redirect
import sqlite3
import hashlib
import base64
import time

app = Flask(__name__)

# Initialize Database
def init_db():
    conn = sqlite3.connect("urls.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS urls 
                 (short TEXT PRIMARY KEY, long TEXT, created_at INTEGER, expires_at INTEGER, access_count INTEGER DEFAULT 0)''')
    conn.commit()
    conn.close()

init_db()

# Function to generate short URL
def generate_short_url(long_url):
    hash_obj = hashlib.md5(long_url.encode())
    return base64.urlsafe_b64encode(hash_obj.digest())[:6].decode()

# API to Shorten URL
@app.route("/shorten", methods=["POST"])
def shorten_url():
    data = request.get_json()
    long_url = data.get("long_url")
    expires_in = data.get("expires_in", None)  # Optional expiration in seconds
    
    if not long_url:
        return jsonify({"error": "Missing long_url"}), 400
    
    short_url = generate_short_url(long_url)
    expires_at = int(time.time()) + expires_in if expires_in else None
    
    conn = sqlite3.connect("urls.db")
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO urls (short, long, created_at, expires_at) VALUES (?, ?, ?, ?)", 
              (short_url, long_url, int(time.time()), expires_at))
    conn.commit()
    conn.close()
    
    return jsonify({"short_url": short_url, "expires_at": expires_at})

# API to Retrieve Original URL
@app.route("/expand/<short_url>", methods=["GET"])
def expand_url(short_url):
    conn = sqlite3.connect("urls.db")
    c = conn.cursor()
    c.execute("SELECT long, expires_at, access_count FROM urls WHERE short=?", (short_url,))
    row = c.fetchone()
    conn.close()

    if not row:
        return jsonify({"error": "Short URL not found"}), 404

    long_url, expires_at, access_count = row
    if expires_at and time.time() > expires_at:
        return jsonify({"error": "URL expired"}), 410

    # Increment access count
    conn = sqlite3.connect("urls.db")
    c = conn.cursor()
    c.execute("UPDATE urls SET access_count = access_count + 1 WHERE short=?", (short_url,))
    conn.commit()
    conn.close()

    return redirect(long_url, code=302)

# API to Track Usage Statistics
@app.route("/stats/<short_url>", methods=["GET"])
def url_stats(short_url):
    conn = sqlite3.connect("urls.db")
    c = conn.cursor()
    c.execute("SELECT long, access_count FROM urls WHERE short=?", (short_url,))
    row = c.fetchone()
    conn.close()

    if not row:
        return jsonify({"error": "Short URL not found"}), 404

    return jsonify({"long_url": row[0], "access_count": row[1]})

if __name__ == "__main__":
    app.run(debug=True)
