# ch02 - Bypassing Access Control with HTTP Verb Tampering

If the server does not validate the request method properly, access control
that is enforced only on POST can be bypassed by simply changing the method
to GET (or HEAD).

| File | Description |
|---|---|
| `verb_tamper_vuln.py` | Vulnerable app (port 8000) |
| `verb_tamper_fixed.py` | Fixed app (port 8001) |
| `attack.py` | Attack reproduction script (standard library only) |

## Why the bypass works

Two mistakes have to be present at the same time:

1. The access check runs **only for POST** requests.
2. The handler **also accepts GET/HEAD** and reads parameters from the query
   string as well (`request.values`).

Flask automatically adds HEAD to any route that allows GET, and for a HEAD
request it runs the GET handler as usual and just drops the response body.
So the deletion still happens with HEAD.

## Running the lab

```bash
# from the repository root
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd ch02

# terminal 1
python3 verb_tamper_vuln.py
# terminal 2
python3 attack.py          # bypass succeeds

# fixed version
python3 verb_tamper_fixed.py
python3 attack.py 8001     # everything is blocked with 403
```

Or try it by hand with curl:

```bash
curl -i -X POST -d "username=alice" http://127.0.0.1:8000/admin/delete_user   # 403
curl -i "http://127.0.0.1:8000/admin/delete_user?username=alice"              # 200, deleted
curl -I "http://127.0.0.1:8000/admin/delete_user?username=bob"                # 200, deleted
```

Logged in as admin, deletion works normally on the fixed app:

```bash
curl -c cookies.txt -d "username=admin" http://127.0.0.1:8001/login
curl -b cookies.txt -X POST -d "username=alice" http://127.0.0.1:8001/admin/delete_user
```

## Defenses

- Apply access control per path/resource to **every method**, not per method (deny by default).
- Allow only the methods each handler needs; reject the rest with 405.
- Read input only from the intended source (`request.form`).
- Never perform state-changing actions on GET.
