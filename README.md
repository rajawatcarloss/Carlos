# 🚀 Telegram Manager - Complete Application

**Professional Telegram Multi-Account Manager with Web Interface**

## ✨ Features

✅ **Multi-Account Login**
- Real Telegram OTP authentication
- 2FA password support
- Multiple accounts simultaneously
- Auto session management

✅ **Group Management**
- Load all groups/channels from Telegram
- Select/deselect groups
- Bulk select/deselect
- Search groups

✅ **Message Sender**
- Send messages to multiple groups at once
- Configurable delay between messages
- Real-time sending status
- Error logging

✅ **Activity Logs**
- Real-time log viewer
- Search functionality
- Status tracking
- Message history

✅ **Professional UI**
- Modern Bootstrap 5 design
- Responsive mobile-friendly
- Real-time updates
- Smooth animations

## 🚀 Quick Start

### 1. Get Telegram API Credentials

1. Visit: https://my.telegram.org
2. Login with your phone
3. Go to "API development tools"
4. Copy **API_ID** and **API_HASH**

### 2. Installation

```bash
# Clone repository
git clone https://github.com/rajawatcarloss/Carlos.git
cd Carlos

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure

Edit `.env` file:
```
API_ID=12345678
API_HASH=your_hash_here_from_telegram_org
```

### 4. Run

```bash
python app.py
```

**Open browser:** http://localhost:5000

## 📖 Usage

### Step 1: Login to Telegram
- Go to home page
- Enter account name and phone number
- Receive OTP on Telegram
- Enter OTP code
- If 2FA enabled, enter password
- Account added!

### Step 2: Select Groups
- Go to "Accounts" page
- Click "Select Groups" on account
- Click "Reload Groups" to load from Telegram
- Select groups you want to message

### Step 3: Send Messages
- Go to "Send Message" page
- Select account
- Select groups
- Enter message
- Set delay (seconds between messages)
- Click "Send to All Selected Groups"

### Step 4: Monitor Logs
- Go to "Logs" page
- View all activities
- Search logs

## 📁 Project Structure

```
Carlos/
├── app.py                    # Main Flask application
├── config.py                 # Configuration
├── database.py               # Database operations
├── telethon_handler.py       # Telegram API handler
├── requirements.txt          # Dependencies
├── .env                      # API credentials
└── templates/
    ├── base.html             # Base template
    ├── login.html            # Login page
    ├── dashboard.html        # Accounts page
    ├── send-message.html     # Send message page
    ├── logs.html             # Logs page
    ├── 404.html              # 404 page
    └── 500.html              # 500 page
```

## ⚙️ Technologies

- **Backend:** Flask 2.3.3
- **Telegram:** Telethon 1.31.1
- **Database:** SQLite
- **Frontend:** Bootstrap 5, jQuery
- **Language:** Python 3.7+

## 📝 API Endpoints

- `POST /api/login` - Start login process
- `POST /api/verify-code` - Verify OTP
- `GET /api/accounts` - Get all accounts
- `POST /api/delete-account` - Delete account
- `GET /api/groups/<id>` - Get groups for account
- `POST /api/toggle-group` - Toggle group selection
- `POST /api/send-to-all` - Send message to all selected groups
- `GET /api/logs` - Get activity logs

## 🐛 Troubleshooting

### "Invalid API ID/HASH"
- Make sure you got correct credentials from https://my.telegram.org
- Double-check in .env file
- Restart app

### "Connection Error"
- Check internet connection
- Telegram might be blocking requests from your region

### "OTP Not Received"
- Wait a few seconds
- Check Telegram app for code
- Try logging in again

## 📞 Support

For issues, check logs page or restart application.

---

**Developed for efficient multi-account Telegram management** 🚀
