import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

DB_PATH = os.path.join(os.path.dirname(__file__), 'prompts.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Create tables if they don't exist
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT, 
                 credits INTEGER DEFAULT 20, is_admin BOOLEAN DEFAULT 0)''')
    c.execute('''CREATE TABLE IF NOT EXISTS prompts 
                 (id INTEGER PRIMARY KEY, user_id INTEGER, input1 TEXT, input2 TEXT, 
                 image BLOB, FOREIGN KEY(user_id) REFERENCES users(id))''')
    c.execute('''CREATE TABLE IF NOT EXISTS credit_requests
                 (id INTEGER PRIMARY KEY, user_id INTEGER, requested_amount INTEGER,
                 status TEXT DEFAULT 'pending', request_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                 FOREIGN KEY(user_id) REFERENCES users(id))''')
    
    # Ensure admin account exists with default credentials
    c.execute("SELECT * FROM users WHERE username = 'admin'")
    if not c.fetchone():
        c.execute("INSERT INTO users (username, password, credits, is_admin) VALUES (?, ?, ?, ?)", 
                 ('admin', generate_password_hash('123'), 999999, True))
    
    conn.commit()
    conn.close()

def get_user(username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()
    return user

def create_user(username, password):
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        # Hash the password before storing
        hashed_password = generate_password_hash(password)
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        if conn:
            conn.rollback()
        return False
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()

def save_prompt(user_id, input1, input2=None, image=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO prompts (user_id, input1, input2, image) VALUES (?, ?, ?, ?)", 
             (user_id, input1, input2, image))
    prompt_id = c.lastrowid
    print(f"Saved prompt {prompt_id} with user_id={user_id}, input1={input1[:10]}..., input2={input2[:10] if input2 else None}..., image ({len(image or b'')} bytes)")
    conn.commit()
    conn.close()
    return prompt_id

def get_prompt(prompt_id, user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT image FROM prompts WHERE id = ? AND user_id = ?",
             (prompt_id, user_id))
    result = c.fetchone()
    conn.close()
    if result:
        print(f"Retrieved image for prompt_id={prompt_id}, user_id={user_id}, size={len(result[0] or b'')} bytes")
        return result[0]
    return None

def get_user_credits(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT credits FROM users WHERE id = ?", (user_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else 0

def update_user_credits(user_id, credits):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE users SET credits = ? WHERE id = ?", (credits, user_id))
    conn.commit()
    conn.close()

def request_credits(user_id, amount):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO credit_requests (user_id, amount) VALUES (?, ?)",
             (user_id, amount))
    conn.commit()
    conn.close()

def get_credit_requests():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""SELECT cr.id, u.username, cr.amount, cr.status, cr.created_at 
                 FROM credit_requests cr 
                 JOIN users u ON cr.user_id = u.id 
                 ORDER BY cr.created_at DESC""")
    requests = c.fetchall()
    conn.close()
    return requests

def approve_credit_request(request_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT user_id, amount FROM credit_requests WHERE id = ?", (request_id,))
    request = c.fetchone()
    if request:
        user_id, amount = request
        current_credits = get_user_credits(user_id)
        c.execute("UPDATE users SET credits = ? WHERE id = ?", (current_credits + amount, user_id))
        c.execute("UPDATE credit_requests SET status = 'approved' WHERE id = ?", (request_id,))
        conn.commit()
    conn.close()
import sqlite3

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn