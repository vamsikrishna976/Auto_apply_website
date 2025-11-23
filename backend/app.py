from flask import Flask, request, jsonify, send_from_directory
import os
from apply_jobs import apply_for_job, list_supported_sites
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__, static_folder="static_debug", static_url_path="/debug")

@app.route("/")
def index():
    return send_from_directory("../frontend", "index.html")

@app.route("/supported-sites")
def supported_sites():
    return jsonify({"sites": list_supported_sites()})

@app.route("/apply", methods=["POST"])
def apply():
    data = request.get_json() or {}
    site = data.get("site")
    keyword = data.get("keyword")
    location = data.get("location") or os.getenv("LOCATION", "Bangalore")
    max_applies = int(data.get("max_applies", 1))
    if site not in list_supported_sites():
        return jsonify({"ok": False, "error": "unsupported site"}), 400
    try:
        result = apply_for_job(site=site, keyword=keyword, location=location, max_applies=max_applies)
        return jsonify({"ok": True, "result": result})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route("/debug/naukri")
def debug_naukri():
    return send_from_directory(app.static_folder, "naukri_page.html")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
