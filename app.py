from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from config import Config
from database import db
from telethon_handler import telethon_handler
import asyncio
import threading

app = Flask(__name__, template_folder='templates')
app.config.from_object(Config)
CORS(app)

# Helper to run async functions
def run_async(coro):
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(coro)
        loop.close()
        return result
    except Exception as e:
        print(f"Async error: {str(e)}")
        return {'status': 'error', 'message': str(e)}

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    accounts = db.get_all_accounts()
    return render_template('dashboard.html', accounts=accounts)

@app.route('/send-message')
def send_message_page():
    accounts = db.get_all_accounts()
    return render_template('send-message.html', accounts=accounts)

@app.route('/logs')
def logs_page():
    return render_template('logs.html')

# API Routes
@app.route('/api/login', methods=['POST'])
def api_login():
    try:
        data = request.json
        name = data.get('name')
        phone = data.get('phone')
        
        if not name or not phone:
            return jsonify({'status': 'error', 'message': 'Name and phone required'}), 400
        
        result = run_async(telethon_handler.login(name, phone))
        return jsonify(result)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/verify-code', methods=['POST'])
def api_verify_code():
    try:
        data = request.json
        name = data.get('name')
        phone = data.get('phone')
        code = data.get('code')
        password = data.get('password')
        
        if not name or not phone or not code:
            return jsonify({'status': 'error', 'message': 'Missing fields'}), 400
        
        result = run_async(telethon_handler.verify_code(name, phone, code, password))
        
        if result['status'] == 'success':
            db.add_account(
                name=name,
                phone=phone,
                user_id=result['user_id'],
                first_name=result.get('first_name', ''),
                last_name=result.get('last_name', ''),
                username=result.get('username', '')
            )
            db.add_log(name, None, 'login', 'success', f'User {result.get("first_name", "")} logged in')
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/accounts', methods=['GET'])
def api_get_accounts():
    try:
        accounts = db.get_all_accounts()
        return jsonify(accounts)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/delete-account', methods=['POST'])
def api_delete_account():
    try:
        data = request.json
        account_id = data.get('account_id')
        
        account = None
        for acc in db.get_all_accounts():
            if acc['id'] == account_id:
                account = acc
                break
        
        if not account:
            return jsonify({'status': 'error', 'message': 'Account not found'}), 404
        
        db.delete_account(account_id)
        db.add_log(account['name'], None, 'logout', 'success', 'Account deleted')
        
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/groups/<int:account_id>', methods=['GET'])
def api_get_groups(account_id):
    try:
        account = None
        for acc in db.get_all_accounts():
            if acc['id'] == account_id:
                account = acc
                break
        
        if not account:
            return jsonify({'status': 'error', 'message': 'Account not found'}), 404
        
        result = run_async(telethon_handler.get_groups(account['name'], account['phone']))
        
        if result['status'] == 'success':
            for group in result['groups']:
                db.add_group(account_id, group['id'], group['name'])
            db.add_log(account['name'], None, 'load_groups', 'success', f'Loaded {len(result["groups"])} groups')
        
        db_groups = db.get_groups(account_id)
        return jsonify({'status': 'success', 'groups': db_groups})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/toggle-group', methods=['POST'])
def api_toggle_group():
    try:
        data = request.json
        group_id = data.get('group_id')
        is_selected = data.get('is_selected')
        
        db.toggle_group(group_id, is_selected)
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/send-to-all', methods=['POST'])
def api_send_to_all():
    try:
        data = request.json
        account_id = data.get('account_id')
        message_text = data.get('message')
        delay = data.get('delay', 1)
        
        if not account_id or not message_text:
            return jsonify({'status': 'error', 'message': 'Missing fields'}), 400
        
        result = run_async(telethon_handler.send_to_all_groups(account_id, message_text, delay))
        return jsonify(result)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/logs', methods=['GET'])
def api_get_logs():
    try:
        logs = db.get_logs()
        return jsonify(logs)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 Telegram Manager Starting...")
    print("="*50)
    print(f"API_ID: {Config.API_ID}")
    print(f"API_HASH: {Config.API_HASH[:10]}...")
    print("\n📱 Open: http://localhost:5000")
    print("="*50 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
