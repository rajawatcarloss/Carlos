from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from config import Config
from database import db

app = Flask(__name__, template_folder='templates')
app.config.from_object(Config)
CORS(app)

@app.route('/')
def dashboard():
    stats = db.get_dashboard_stats()
    return render_template('dashboard.html', stats=stats)

@app.route('/accounts')
def accounts():
    all_accounts = db.get_all_accounts()
    accounts_list = [dict(acc) for acc in all_accounts]
    return render_template('accounts.html', accounts=accounts_list)

@app.route('/groups')
def groups():
    all_accounts = db.get_all_accounts()
    accounts_list = [dict(acc) for acc in all_accounts]
    return render_template('groups.html', accounts=accounts_list)

@app.route('/sender')
def sender():
    all_accounts = db.get_all_accounts()
    accounts_list = [dict(acc) for acc in all_accounts]
    return render_template('sender.html', accounts=accounts_list)

@app.route('/repeater')
def repeater():
    all_accounts = db.get_all_accounts()
    accounts_list = [dict(acc) for acc in all_accounts]
    return render_template('repeater.html', accounts=accounts_list)

@app.route('/logs')
def logs():
    return render_template('logs.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/api/dashboard/stats')
def get_dashboard_stats():
    stats = db.get_dashboard_stats()
    return jsonify(stats)

@app.route('/api/accounts')
def get_accounts():
    all_accounts = db.get_all_accounts()
    accounts_list = []
    for acc in all_accounts:
        accounts_list.append({
            'id': acc['id'],
            'name': acc['name'],
            'phone': acc['phone'],
            'user_id': acc['user_id'],
            'first_name': acc['first_name'],
            'last_name': acc['last_name'],
            'username': acc['username'],
            'is_active': acc['is_active']
        })
    return jsonify(accounts_list)

@app.route('/api/logs')
def get_logs():
    logs_list = db.get_logs()
    logs_data = []
    for log in logs_list:
        logs_data.append({
            'id': log['id'],
            'timestamp': log['timestamp'],
            'account_name': log['account_name'],
            'group_name': log['group_name'],
            'action': log['action'],
            'status': log['status'],
            'message': log['message']
        })
    return jsonify(logs_data)

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=Config.DEBUG, host='0.0.0.0', port=5000)
