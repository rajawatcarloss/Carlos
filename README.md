# Telegram Manager - Web Application

**A professional Flask web application to manage multiple Telegram accounts and send messages to multiple groups.**

## Features

✅ **Account Management**
- Add unlimited Telegram accounts
- Phone number + OTP authentication
- Support for 2FA passwords
- Auto-reconnect sessions
- Delete accounts

✅ **Groups Management**
- Load groups from Telegram
- Search and filter groups
- Select/deselect groups
- Bulk operations

✅ **Message Sender**
- Send text messages to multiple groups
- Send from one or multiple accounts
- Random delay option
- Batch sending

✅ **Repeater**
- Automatic message repetition
- Configurable interval
- Account rotation
- Start/Pause/Resume/Stop control

✅ **Dashboard**
- Real-time statistics
- Active accounts display
- Auto-refresh every 10 seconds

✅ **Modern UI**
- Bootstrap 5 responsive design
- Professional color scheme
- Mobile-friendly

## Quick Start

### Installation

```bash
# 1. Clone repository
git clone https://github.com/rajawatcarloss/Carlos.git
cd Carlos

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup .env file
# Edit .env and add your API credentials from https://my.telegram.org
API_ID=your_api_id
API_HASH=your_api_hash

# 5. Run the application
python app.py

# 6. Open in browser
# http://localhost:5000
```

## Get Telegram API Credentials

1. Go to https://my.telegram.org
2. Login with your phone number
3. Click on "API development tools"
4. Copy your **API_ID** and **API_HASH**
5. Paste them in `.env` file

## Project Structure

```
Carlos/
├── app.py
├── config.py
├── database.py
├── requirements.txt
├── .env
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── accounts.html
│   ├── groups.html
│   ├── sender.html
│   ├── repeater.html
│   ├── logs.html
│   ├── settings.html
│   ├── 404.html
│   └── 500.html
└── README.md
```

## Technologies

- Flask 2.3.3
- Bootstrap 5
- SQLite
- Telethon 1.31.1

## License

MIT License
