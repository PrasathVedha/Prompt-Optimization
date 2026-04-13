from flask import Flask, request, jsonify, render_template, send_file, session, redirect, url_for, Response, flash
from database.database import (init_db, get_user, create_user, save_prompt, get_prompt,
                              get_user_credits, update_user_credits, request_credits,
                              get_credit_requests, approve_credit_request)
from enhance_prompt import enhance_prompt_initial, enhance_prompt_with_style, enhance_prompt_final
from generate_images import generate_image
from werkzeug.security import check_password_hash, generate_password_hash
from io import BytesIO
from waitress import serve
from routes.user_routes import user_bp
from routes.admin_routes import admin_bp
from database.database import init_db, get_db
from functools import wraps
import os
import socket
os.environ["HF_HOME"] = "E:/cap/Stable-Diffusion-Project/TEXT-TO-IMAGE-GENERATION/huggingface"

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Generate a secure random key

# Register blueprints
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(admin_bp, url_prefix='/admin')

# Ensure profile photos directory exists
os.makedirs(os.path.join('static', 'profile_photos'), exist_ok=True)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    if 'user_id' in session:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT is_admin FROM users WHERE id = ?', (session['user_id'],))
        user = cursor.fetchone()
        
        if user and user[0]:
            return redirect(url_for('admin_dashboard'))
        return redirect(url_for('user.dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT id, username, password, is_admin FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        
        if user is None:
            flash('Invalid username or password')
            return render_template('login.html')
            
        user_id, db_username, hashed_password, is_admin = user
        
        # Special handling for admin user
        if db_username == 'admin':
            if password == '123':
                session['user_id'] = user_id
                return redirect(url_for('admin.dashboard'))
            else:
                flash('Invalid admin credentials')
                return render_template('login.html')
        
        # Regular user authentication
        if check_password_hash(hashed_password, password):
            session['user_id'] = user_id
            return redirect(url_for('user.dashboard'))
        
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if get_user(username):
            flash('Username already exists')
            return redirect(url_for('register'))
        
        if create_user(username, password):
            flash('Registration successful! Please login.')
            return redirect(url_for('login'))
        else:
            flash('Registration failed. Please try again.')
            return redirect(url_for('register'))
    return render_template('register.html')

@app.route('/generate', methods=['POST'])
def generate():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user_credits = get_user_credits(session['user_id'])
    if user_credits <= 0:
        return jsonify({'error': 'Insufficient credits'}), 403
    
    prompt = request.json.get('prompt')
    style = request.json.get('style')
    if not prompt:
        return jsonify({'error': 'No prompt provided'}), 400
    
    try:
        # Step 1: Initial prompt enhancement
        enhanced_prompt = enhance_prompt_initial(prompt)
        print("Step 1 - Initial enhancement:", enhanced_prompt)
        
        # Step 2: Add style and enhance
        styled_prompt = enhance_prompt_with_style(enhanced_prompt, style)
        print("Step 2 - Style enhancement:", styled_prompt)
        
        # Step 3: Final enhancement for image generation
        final_prompt = enhance_prompt_final(styled_prompt)
        print("Step 3 - Final enhancement:", final_prompt)
        
        # Generate image with the final prompt
        if style and style != 'none':
            from generate_images import generate_image_with_style
            image_bytes = generate_image_with_style(final_prompt, style)
        else:
            image_bytes = generate_image(final_prompt)
        
        # Save the prompt and update credits
        prompt_id = save_prompt(session['user_id'], prompt, final_prompt, image_bytes)
        update_user_credits(session['user_id'], user_credits - 1)
        print(f"Generated and saved prompt ID: {prompt_id} for user_id: {session['user_id']}")
        return jsonify({'message': 'Image generated successfully', 'prompt_id': prompt_id})
    except Exception as e:
        print(f"Error in generate: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/output/<prompt_id>')
def get_output(prompt_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    image_bytes = get_prompt(prompt_id, session['user_id'])
    if image_bytes:
        print(f"Returning image for prompt_id: {prompt_id}, user_id: {session['user_id']}")
        return Response(image_bytes, mimetype='image/jpeg')
    print(f"No image found for prompt_id: {prompt_id}, user_id: {session['user_id']}")
    return jsonify({'error': 'Image not ready'}), 404

@app.route('/request-credits', methods=['POST'])
def request_more_credits():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    amount = request.json.get('amount')
    if not amount or not isinstance(amount, int) or amount <= 0:
        return jsonify({'error': 'Invalid credit amount'}), 400
    
    request_credits(session['user_id'], amount)
    return jsonify({'message': 'Credit request submitted successfully'})

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    from waitress import serve
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    port = 5000
    print(' * Starting production server...')
    print(f' * Local URL: http://localhost:{port}')
    print(f' * Network URL: http://{local_ip}:{port}')
    serve(app, host='0.0.0.0', port=port)

