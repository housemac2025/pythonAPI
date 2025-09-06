from flask import Flask, request, jsonify, make_response

app = Flask(__name__)
EXPECTED_TOKEN = "secret123"  # ここを好きに変える

def unauthorized():
    resp = make_response(jsonify({"error": "invalid_token"}), 401)
    resp.headers["WWW-Authenticate"] = 'Bearer realm="api", error="invalid_token"'
    return resp

def forbidden():
    return jsonify({"error": "insufficient_scope"}), 403

@app.route("/health")
def health():
    return {"status": "ok"}



@app.route("/secure")
def secure():
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return unauthorized()
    token = auth.split(" ", 1)[1].strip()
    if token != EXPECTED_TOKEN:
        return forbidden()
    return jsonify({"message": "Access granted", "user": "demo"})
    
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)