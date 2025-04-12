from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHANNEL_ID")
SNIPER_SECRET = os.getenv("SNIPER_SECRET")

# 🔹 Root route to confirm Flask is live
@app.route("/", methods=["GET"])
def home():
    return "🎯 Flask is up and running."

# 🔹 Test route to confirm deployment
@app.route("/test", methods=["GET"])
def test():
    return jsonify({"status": "✅ THIS IS THE LIVE VERSION"}), 200

# 🔹 Main route for sniper alerts
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

# 🔹 Run on Railway's required host and port
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
