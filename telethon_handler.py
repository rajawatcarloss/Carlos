import asyncio
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from config import Config
from database import db
import os

class TelethonHandler:
    def __init__(self):
        self.clients = {}
        self.sessions_path = Config.SESSIONS_PATH
    
    def get_session_file(self, name):
        return os.path.join(self.sessions_path, name)
    
    async def login(self, name, phone):
        """Login to Telegram with phone number"""
        try:
            session_file = self.get_session_file(name)
            client = TelegramClient(session_file, Config.API_ID, Config.API_HASH)
            
            await client.connect()
            
            if not await client.is_user_authorized():
                await client.send_code_request(phone)
                return {'status': 'code_sent', 'phone': phone, 'session_name': name}
            else:
                me = await client.get_me()
                return {'status': 'already_login', 'user_id': me.id, 'name': me.first_name}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    async def verify_code(self, name, phone, code, password=None):
        """Verify OTP code"""
        try:
            session_file = self.get_session_file(name)
            client = TelegramClient(session_file, Config.API_ID, Config.API_HASH)
            
            await client.connect()
            
            try:
                me = await client.sign_in(phone, code)
            except SessionPasswordNeededError:
                if not password:
                    return {'status': 'password_needed'}
                me = await client.sign_in(password=password)
            
            self.clients[name] = client
            
            return {
                'status': 'success',
                'user_id': me.id,
                'first_name': me.first_name,
                'last_name': me.last_name,
                'username': me.username
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    async def get_groups(self, name):
        """Get all groups/channels for account"""
        try:
            session_file = self.get_session_file(name)
            client = TelegramClient(session_file, Config.API_ID, Config.API_HASH)
            
            await client.connect()
            
            if not await client.is_user_authorized():
                return {'status': 'error', 'message': 'Not logged in'}
            
            dialogs = await client.get_dialogs()
            groups = []
            
            for dialog in dialogs:
                if dialog.is_group or dialog.is_channel:
                    groups.append({
                        'id': dialog.id,
                        'name': dialog.name,
                        'type': 'channel' if dialog.is_channel else 'group'
                    })
            
            await client.disconnect()
            return {'status': 'success', 'groups': groups}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    async def send_message(self, name, group_id, message_text):
        """Send message to group"""
        try:
            session_file = self.get_session_file(name)
            client = TelegramClient(session_file, Config.API_ID, Config.API_HASH)
            
            await client.connect()
            
            if not await client.is_user_authorized():
                return {'status': 'error', 'message': 'Not logged in'}
            
            await client.send_message(group_id, message_text)
            await client.disconnect()
            
            return {'status': 'success'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    async def send_to_all_groups(self, account_id, message_text, delay=1):
        """Send message to all selected groups"""
        try:
            account = None
            for acc in db.get_all_accounts():
                if acc['id'] == account_id:
                    account = acc
                    break
            
            if not account:
                return {'status': 'error', 'message': 'Account not found'}
            
            session_file = self.get_session_file(account['name'])
            client = TelegramClient(session_file, Config.API_ID, Config.API_HASH)
            
            await client.connect()
            
            if not await client.is_user_authorized():
                return {'status': 'error', 'message': 'Not logged in'}
            
            groups = db.get_groups(account_id)
            sent_count = 0
            
            for group in groups:
                if group['is_selected']:
                    try:
                        await client.send_message(group['group_id'], message_text)
                        db.add_log(account['name'], group['group_name'], 'send_message', 'success', message_text[:50])
                        sent_count += 1
                        await asyncio.sleep(delay)
                    except Exception as e:
                        db.add_log(account['name'], group['group_name'], 'send_message', 'error', str(e))
            
            await client.disconnect()
            
            return {'status': 'success', 'sent_count': sent_count}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

telethon_handler = TelethonHandler()
