import http.client

conn = http.client.HTTPConnection("52.4.57.36:8080")

payload = ""

headers = {
    'ApiKey': "i847r3fkaitemp_keyuxhy4723r42r"
    }

conn.request("GET", "/v1/mappings", payload, headers)

res = conn.getresponse()
data = res.read()