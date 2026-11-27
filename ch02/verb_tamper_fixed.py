# FIXED version: access control applies regardless of method,
# and each handler accepts only the methods it needs.
from flask import Flask, request, session, abort

app = Flask(__name__)
app.secret_key = "lab-only"

USERS = {"alice": "user", "bob": "user", "admin": "admin"}


@app.route("/login", methods=["POST"])
def login():
    name = request.form.get("username", "")
    if name not in USERS:
        abort(401)
    session["user"] = name
    session["role"] = USERS[name]
    return f"logged in as {name} (role={USERS[name]})\n"


@app.before_request
def admin_guard():
    # FIX 1: check every request to /admin, whatever the method (deny by default)
    if request.path.startswith("/admin") and session.get("role") != "admin":
        abort(403)


@app.route("/admin/delete_user", methods=["POST"])  # FIX 2: POST only, anything else gets 405
def delete_user():
    # FIX 3: read input from the form body only
    username = request.form.get("username")
    USERS.pop(username, None)
    return f"deleted {username}. remaining users: {list(USERS)}\n"


@app.route("/users")
def list_users():
    return f"{list(USERS)}\n"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8001)
