from flask import Flask, request, jsonify
import requests
import threading
import time

app = Flask(__name__)

BOT_TOKEN = "7876168717:AAH7qxL3FEzBqS99_Lp1HSjL5GDC-hTZ78o"
CHAT_ID = "-1002502682234"
SNIPER_SECRET = "moonaccess123"

@app.route("/", methods=["GET"])
def home():
    return "🎯 Flask is up and running."

@app.route("/test", methods=["GET"])
def test():
    return jsonify({"status": "✅ THIS IS THE LIVE VERSION"}), 200

@app.route("/send", methods=["POST"])
def send_alert():
    try:
        data = request.get_json()
        if data.get("secret") != SNIPER_SECRET:
            return jsonify({"error": "Unauthorized"}), 403

        message = data.get("message", "⚠️ Default test message")
        response = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": message}
        )
        return jsonify({"status": "sent", "code": response.status_code}), 200
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

# ─── Background Posting: Automatically send a message to Telegram ───

def auto_post():
    # Wait a few seconds after startup
    time.sleep(5)
    while True:
        try:
            auto_message = "Automated message from bot."
            resp = requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                data={"chat_id": CHAT_ID, "text": auto_message}
            )
            print("Automated post status:", resp.status_code)
        except Exception as e:
            print("Error in auto_post:", e)
        # Adjust delay as needed (currently 60 seconds)
        time.sleep(60)

if __name__ == "__main__":
    # Start the auto-posting thread in the background.
    auto_thread = threading.Thread(target=auto_post, daemon=True)
    auto_thread.start()
    app.run(host="0.0.0.0", port=8000)
