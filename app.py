from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

@app.route("/", methods=["GET"])
def home():
    return "🎯 Sniper Relay is live on Railway."

@app.route("/gpt-relay", methods=["POST"])
def gpt_relay():
    try:
        data = request.get_json()
        message = data.get("message", "⚠️ No message content received.")

        if not message:
            return jsonify({"error": "Missing message"}), 400

        telegram_response = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={"chat_id": CHAT_ID, "text": message}
        )

        if telegram_response.status_code == 200:
            return jsonify({"status": "✅ Sent to Telegram"}), 200
        else:
            return jsonify({
                "status": "❌ Telegram send failed",
                "response": telegram_response.text
            }), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)  # ✅ correct
