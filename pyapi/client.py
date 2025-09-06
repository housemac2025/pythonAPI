import requests

BASE = "http://127.0.0.1:5000"
TOKEN_OK = "secret123"      # 正しい
TOKEN_NG = "totally-wrong"  # 間違い
"""
# 認証不要エンドポイント
print("GET /health ->", requests.get(f"{BASE}/health").json())

# 認証ヘッダなし（401）
r = requests.get(f"{BASE}/secure")
print("GET /secure (no auth) ->", r.status_code, r.text)

# 間違いトークン（403）
r = requests.get(f"{BASE}/secure", headers={"Authorization": f"Bearer {TOKEN_NG}"})
print("GET /secure (bad token) ->", r.status_code, r.text)

# 正しいトークン（200）
r = requests.get(f"{BASE}/secure", headers={"Authorization": f"Bearer {TOKEN_OK}"})
print("GET /secure (good token) ->", r.status_code, r.json())

"""

r = requests.get(f"{BASE}/health")
print(r)