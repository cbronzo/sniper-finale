from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Your hardcoded credentials
BOT_TOKEN = "7876168717:AAH7qxL3FEzBqS99_Lp1HSjL5GDC-hTZ78o"
CHAT_ID = "-1002502682234"
SNIPER_SECRET = "moonaccess123"

# Home route for quick testing
@app.route("/", methods=["GET"])
def home():
    return "🎯 Flask is up and running."

# Manual test route
@app.route("/test", methods=["GET"])
def test():
    return jsonify({"status": "✅ THIS IS THE LIVE VERSION"}), 200

# Secure /send route (requires secret)
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

# NEW open-access /send-alert route (for GPT agent)
@app.route("/send-alert", methods=["POST"])
def send_alert_from_gpt():
    try:
        data = request.get_json()
        message = data.get("message")

        if not message:
            return jsonify({"error": "Missing message content"}), 400

        response = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data={
                "chat_id": CHAT_ID,
                "text": message,
                "parse_mode": "Markdown"
            }
        )

        if response.status_code == 200:
            return jsonify({"status": "sent"}), 200
        else:
            return jsonify({
                "error": "Failed to send message to Telegram",
                "details": response.text
            }), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Required to run on Railway
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
