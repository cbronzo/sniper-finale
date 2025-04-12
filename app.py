from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

BOT_TOKEN = "7876168717:AAEZG9J10w9HjyHLYAF4F25REgNS01KLZcc"
CHAT_ID = "-1002502682234"
SNIPER_SECRET = "moonaccess123"

@app.route("/", methods=["GET"])
def home():
    return "🎯 Docker-based Flask is running!"

@app.route("/test", methods=["GET"])
def test():
    return jsonify({"status": "✅ Docker version live"}), 200

@app.route("/send", methods=["POST"])
def send_alert():
    try:
        data = request.get_json()
        if data.get("secret") != SNIPER_SECRET:
            return jsonify({"error": "Unauthorized"}), 403

        message = data.get("message", "⚠️ Default test message")
        resp = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": message}
        )
        return jsonify({"status": "sent", "code": resp.status_code}), 200
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
