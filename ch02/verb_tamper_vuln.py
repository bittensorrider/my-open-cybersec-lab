# VULNERABLE version: access control enforced only on POST can be bypassed
# by switching the request method to GET or HEAD.
# For lab use only - bind to 127.0.0.1.
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
    # BUG 1: the admin check runs only when the method is POST
    if request.path.startswith("/admin") and request.method == "POST":
        if session.get("role") != "admin":
            abort(403)


@app.route("/admin/delete_user", methods=["GET", "POST"])  # BUG 2: GET (and implicitly HEAD) accepted
def delete_user():
    # BUG 3: request.values merges query string (args) and form body (form)
    username = request.values.get("username")
    USERS.pop(username, None)
    return f"deleted {username}. remaining users: {list(USERS)}\n"


@app.route("/users")
def list_users():
    return f"{list(USERS)}\n"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
