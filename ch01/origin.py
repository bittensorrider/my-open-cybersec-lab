from urllib.parse import urlsplit

def origin(url):
    p = urlsplit(url)
    port = p.port or (443 if p.scheme == "https" else 80)
    return (p.scheme, p.hostname, port)

base = "https://shop.example.com/page"
for t in ["https://shop.example.com/other", "http://shop.example.com/", "https://shop.example.com:8443/", "https://api.example.com/"]:
    print(t, "->", origin(t) == origin(base))
