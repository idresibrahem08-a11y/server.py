from datetime import datetime, timedelta
import json
import os
from flask import Flask, jsonify, request
import pytz

app = Flask(__name__)

KEYS_FILE = "keys.json"


# خوێندنەوەی کۆدەکان لە فایل
def load_keys():
  if not os.path.exists(KEYS_FILE):
    return {}
  with open(KEYS_FILE, "r") as f:
    try:
      return json.load(f)
    except:
      return {}


# پاشەکەوتکردنی کۆدەکان لە فایل
def save_keys(keys_data):
  with open(KEYS_FILE, "w") as f:
    json.dump(keys_data, f, indent=4)


@app.route("/verify", methods=["POST"])
def verify_key():
  data = request.json or {}
  user_key = data.get("key", "").strip()

  tz = pytz.timezone("Asia/Baghdad")
  now = datetime.now(tz)
  current_time = now.strftime("%Y-%m-%d %H:%M:%S")

  keys_data = load_keys()

  # پشکنینی ئەوەی ئایا کۆدەکە بوونی هەیە؟
  if user_key not in keys_data:
    return (
        jsonify({
            "status": "error",
            "message": "❌ Invalid License Key!",
            "time": current_time,
        }),
        401,
    )

  key_info = keys_data[user_key]
  exp_date_str = key_info.get("expiry_date")

  # پشکنینی بەرواری بەسەرچوونی کۆدەکە
  exp_date = datetime.strptime(exp_date_str, "%Y-%m-%d").date()
  if now.date() > exp_date:
    return (
        jsonify({
            "status": "expired",
            "message": (
                "🔒 Your license has expired! Contact @MRHEMO_GAIMING"
            ),
            "time": current_time,
        }),
        403,
    )

  # ئەگەر کۆدەکە ڕاست بوو و بەسەر نەچووبوو
  return jsonify({
      "status": "success",
      "message": "JOIN MY TELEGRAM",
      "link": "https://t.me/OFFICIAL_KURDVIPZONE",
      "time": current_time,
  })


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)
p