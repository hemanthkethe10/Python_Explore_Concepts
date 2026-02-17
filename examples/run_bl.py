import requests

url = "https://staging-flows.backflipt.com/api/v1.1/tenants/backflipt.com/apps/secureFileRoutingPortalAlpha/operation/testsession/execute"

payload = {"data": {}}
headers = {
    "accept": "application/json",
    "Content-Type": "application/json",
    "x-api-key": "20f54cf9-a937-42e5-8a23-7e09b550cf04",
    "x-tenant-id": "backflipt.com"
}
session = requests.Session()

session.cookies.set(
    "session-64a797a05dcdd59488b02f1d",
    "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJwcmluY2lwYWwiOnsiaWQiOiIxMTNkZjA2Yy0yOTM1LTRhMWYtYTNkZC0wY2E3ZTE0ZGEwNmEiLCJ1c2VyTmFtZSI6ImhlbWFudGhrZXRoZUBiYWNrZmxpcHQuY29tIiwibmFtZSI6IkhlbWFudGggS2V0aGUifSwic3ViIjoic2Vzc2lvbi02NGE3OTdhMDVkY2RkNTk0ODhiMDJmMWQiLCJpYXQiOjE3NDEyNDU2MTUsImV4cCI6MTc0MTMzMjAxNX0.YTF47BEM8zSGQ_J9JR4wOLCiv3YaxeyQU8xMS048bHF8cUO-xmtDaB4r7K003j91NY0CdjieF4yHkPjBtlblCg"
)
response = session.post(url, headers=headers, json=payload)

print(response.text)