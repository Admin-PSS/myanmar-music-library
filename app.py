#!/usr/bin/env python3
"""Flask web server for the Myanmar Music Library browser."""

import json
import threading
import webbrowser
from pathlib import Path

from flask import Flask, jsonify, render_template

app = Flask(__name__)
ALBUMS_JSON = Path(__file__).parent / "albums.json"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/albums")
def albums():
    if not ALBUMS_JSON.exists():
        return jsonify([])
    data = json.loads(ALBUMS_JSON.read_text(encoding="utf-8"))
    return jsonify(data)


if __name__ == "__main__":
    threading.Timer(1.0, lambda: webbrowser.open("http://localhost:5000")).start()
    print("Opening http://localhost:5000 …  (Ctrl+C to stop)")
    app.run(port=5000, debug=False)
