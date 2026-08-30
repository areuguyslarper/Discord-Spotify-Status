import spotipy
from spotipy.oauth2 import SpotifyOAuth

# --- WRİTE-YOUR-DETAİLS ---
SPOTIFY_CLIENT_ID = "YOUR-SPOTIFY-CLIENT-ID"
SPOTIFY_CLIENT_SECRET = "YOUR-SPOTIFY-SECRET-CLIENT-ID"
SPOTIFY_REDIRECT_URI = "http://127.0.0.1:8888/callback"
DISCORD_TOKEN = "YOUR-DISCORD-TOKEN"
CHECK_INTERVAL = 5

# Spotify Allower
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope="user-read-currently-playing",
    )
)

def update_discord_status(status_text):
    url = "https://discord.com/api/v9/users/@me/settings"
    headers = {
        "Authorization": DISCORD_TOKEN,
        "Content-Type": "application/json"
    }
    payload = {
        "custom_status": {
            "text": status_text,
            "emoji_name": "🎵"
        }
    }
    try:
        res = requests.patch(url, headers=headers, json=payload)
        if res.status_code == 200:
            return True
        else:
            print(f"[-] Discord Error ({res.status_code}): {res.text}")
            return False
    except Exception as err:
        print(f"[!] Network Error: {err}")
        return False

last_status = None
print("Spotify -> Discord its Now Working!")

while True:
    try:
        track = sp.current_user_playing_track()
        if track and track.get("is_playing"):
            song = track["item"]["name"]
            artist = track["item"]["artists"][0]["name"]
            status = f"{song} - {artist}"[:128]

            if status != last_status:
                if update_discord_status(status):
                    print(f"[+] Status Updated: {status}")
                    last_status = status
        else:
            if last_status is not None:
                if update_discord_status(""):
                    print("[*] Music is Stoped,Changed Status.")
                last_status = None
    except Exception as e:
        print(f"[!] Spotify Hapsu/Hata: {e}")

    time.sleep(CHECK_INTERVAL)

