from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.roblox.com",
}

ALLOWED_DOMAINS = [
    "catalog.roblox.com",
    "thumbnails.roblox.com",
    "www.roblox.com",
    "economy.roblox.com",
]

def is_allowed(url):
    from urllib.parse import urlparse
    host = urlparse(url).netloc
    return any(host == d or host.endswith("." + d) for d in ALLOWED_DOMAINS)

@app.route("/")
def index():
    html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "roblox-asset-finder.html")
    return send_file(html_path)

@app.route("/proxy")
def proxy():
    url = request.args.get("url", "")
    if not url:
        return jsonify({"error": "Missing url"}), 400
    if not is_allowed(url):
        return jsonify({"error": "Domain not allowed"}), 403
    try:
        resp = requests.get(url, headers=HEADERS, timeout=8)
        return jsonify(resp.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 502

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
