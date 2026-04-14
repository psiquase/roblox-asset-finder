"""
Roblox Asset Finder — Local Proxy Server (v2)
==============================================
Resolve o problema de CORS e também serve o HTML diretamente.

INSTALAÇÃO:
  pip install flask flask-cors requests

USO:
  1. Coloque este arquivo na mesma pasta que o roblox-asset-finder.html
  2. python proxy.py
  3. Abra http://localhost:8080 no browser (NAO abra o HTML direto)
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

ROBLOSECURITY = "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_CAEaAhADIhsKBGR1aWQSEzQ4MDMwNjgzNzYyNzQwNTM4MDMoAw.sA3qsj-4UPxEc1AtVXCTr77X3GHFfsroG8eQBFjjPE8RegzBuO3FRrJUcH2zlLY7crqERp1OY4ZGCNdKoeVJ1mucAZrpGkP_yVq-e8a0H_sybqrS7ErPNPBko_xCW5hjoPPEBGpSeiTvjutldELYEaYtL65z_x4KMt_vgmGc8U8FbmWqE0EInFWNSlMdonAAWexl4wNjt3dKjKNMoFfNhRL6YnAzmclCRPuFszHxCtJfgNpWXvH_TlW37wPbANlXw7I4R-LwqEKj0G_b437rbidufVwg9P__5PP41HQGwZm8vrZUr0cg3B3vXR-6xY_amzdjPhFtoMf8SldjPh8g73VPezXZ1N073vgwTv25CRRbPViuk6FDMzVHj8O4FmF85JEhcT0kuXrmfNkdKtwod2YC-g8xF3HEX17Fm-of_VJHh7WYv8GFbDajpqqiyagqi8Hc2tNsbFmY36wnR8vFlbiKFqxMRpzCynlnFfdswd-2HiYkeU5y97eODpch3F0tToU1OsugtNXUOl6R8u_88XNNRWnW1MFnDLwUwmmUObuk6ZRFMVcE9NUSj3xSCHxtD448ZWF6sWynx6VpBE3L1_gJ_2kNvNN55kMvxz6MIYeotxGkFyVm0fajUwAq6BmzdGSbHwBlxj7H3DG5UPMWwQiaKb02K2bnJPFjAb5F2tVjJd11SKCvrLb1fPUJlXyMHjaAYCGlyS69vW0ht2wgTgEBQ7IQIVPxp6CCZDviVXHzVbbtTxhHsuzELpLyceVX8HGoLf4LSkRwXek_CijHPeioj_6fv0WtLvF7pxWiq3blM"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.roblox.com",
    "Cookie": f".ROBLOSECURITY={ROBLOSECURITY}",
}

ALLOWED_DOMAINS = [
    "catalog.roblox.com",
    "thumbnails.roblox.com",
    "www.roblox.com",
    "economy.roblox.com",
    "apis.roblox.com",
]


def is_allowed(url: str) -> bool:
    from urllib.parse import urlparse
    host = urlparse(url).netloc
    return any(host == d or host.endswith("." + d) for d in ALLOWED_DOMAINS)


@app.route("/")
def index():
    html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "roblox-asset-finder.html")
    if os.path.exists(html_path):
        return send_file(html_path)
    return "<h2>Coloque o arquivo roblox-asset-finder.html na mesma pasta que proxy.py</h2>", 404

@app.route("/<path:filename>")
def serve_file(filename):
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    if os.path.exists(file_path):
        return send_file(file_path)
    return f"<h2>File not found: {filename}</h2>", 404


@app.route("/proxy")
def proxy():
    url = request.args.get("url", "")
    if not url:
        return jsonify({"error": "Missing url parameter"}), 400
    if not is_allowed(url):
        return jsonify({"error": "Domain not allowed"}), 403
    try:
        resp = requests.get(url, headers=HEADERS, timeout=8)
        data = resp.json()
        return jsonify(data)
    except requests.exceptions.Timeout:
        return jsonify({"error": "Roblox API timeout"}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Request failed: {e}"}), 502
    except ValueError:
        return jsonify({"error": "Invalid JSON response"}), 502


@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/debug")
def debug():
    url = "https://catalog.roblox.com/v1/search/items/details?keyword=sad&limit=5&salesTypeFilter=1&sortType=0"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=8)
        return jsonify({"status_code": resp.status_code, "raw": resp.json()})
    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    print("\n Roblox Asset Finder - Proxy Server v2")
    print("=" * 45)
    print("-> Abra no browser: http://localhost:8080")
    print("-> NAO abra o HTML direto como arquivo!")
    print("-> Pressione Ctrl+C para parar\n")
    app.run(host="0.0.0.0", port=8080, debug=False)
