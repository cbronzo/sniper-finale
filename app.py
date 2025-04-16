import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "🎯 Flask is up and running."

@app.route("/gpt-relay", methods=["POST"])
def gpt_relay():
    try:
        data = request.get_json()
        print("Incoming request JSON:", data)

        if "message" not in data:
            print("Missing 'message' in data")
            return jsonify({"error": "Missing 'message' field"}), 400

        telegram_response = requests.post(
            f"https://api.telegram.org/bot{os.environ['BOT_TOKEN']}/sendMessage",
            json={
                "chat_id": os.environ["CHAT_ID"],
                "text": data["message"]
            }
        )

        print("Telegram API response code:", telegram_response.status_code)
        print("Telegram API response body:", telegram_response.text)

        if telegram_response.status_code == 200:
            return jsonify({"status": "relayed and sent"}), 200
        else:
            return jsonify({
                "status": "relay failed",
                "telegram_response": telegram_response.text
            }), 500

    except Exception as e:
        print("Exception occurred:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
