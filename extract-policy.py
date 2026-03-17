import json
import requests

vault_addr = "http://127.0.0.1:8200"
vault_token = "YOUR_VAULT_TOKEN"
policy_name = "my-policy"

policy_text = r'''# 1. Admin permission to actually MOUNT/ENABLE the engine
# We use '*' because Vault checks the sys/mounts/ prefix
path "sys/mounts/*" {
  capabilities = ["read", "list"]
}

path "sys/mounts/*" {
  capabilities = ["read", "delete", "list"]
}

# 2. Data permission to USE the engine once it is mounted
# For KV-v2, you MUST grant access to 'data' and 'metadata' paths
path "kvp/*/data/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}
path "kvh/devteam/data/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}

path "kvp/*/metadata/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}

path "kvh/devteam/data/+" {
capabilities = ["create", "read" , "update", "list"]
}
'''

payload = {
    "policy": policy_text
}

# url = f"{vault_addr}/v1/sys/policies/acl/{policy_name}"
# headers = {
#     "X-Vault-Token": vault_token,
#     "Content-Type": "application/json",
# }

# response = requests.post(url, headers=headers, json=payload, timeout=30)

# print("Status:", response.status_code)
# try:
#     print(json.dumps(response.json(), indent=2))
# except ValueError:
#     print(response.text)
print(json.dumps(payload, indent=2))