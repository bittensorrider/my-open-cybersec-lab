from urllib.parse import urlsplit, parse_qs

u = urlsplit('https://shop.example.com:8443/products/view?id=42&lang=ko#review')
print("Scheme:", u.scheme)
print("Host:", u.hostname)
print("Port:", u.port)
print("Path:", u.path)
print("Query:", u.query)
print("Fragment:", u.fragment)
print("Query params:", parse_qs(u.query))
