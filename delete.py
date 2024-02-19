import re
import sys
import requests

instance = "ussr.rumiserver.com"
token = "UNfPvFLq6QNRL3kD"
usernames = []
if len(sys.argv) == 2:
    mode = sys.argv[1]
else:
    print("deleteかsuspendで選べ")
    exit(1)

if mode == "delete":
    print("削除するユーザーの名前を書き込んでください")
elif mode == "suspend":
    print("凍結するユーザーの名前を書き込んでください")
else:
    print("deleteかsuspendで選べ")
    exit(1)
while True:
    user = input()
    if user == "":
        break
    else:
        # 分解
        match = re.findall(r'@[a-zA-Z0-9.-_]+', user)
        if len(match) == 1:
            username = match[0][1:]
            host = None
        elif len(match) == 2:
            username = match[0][1:]
            host = match[1][1:]
        else:
            print("間違った値が入力されたかも")
            exit(1)
        # ID取得
        data = {
            "host": host,
            "i": token,
            "username": username
        }
        r = requests.post(f"https://{instance}/api/users/show", headers={"Content-Type": "application/json"}, json=data)
        if r.status_code == 200:
            id = r.json()['id']
            data = {
                "i": token,
                "userId": id
            }
            if mode == "delete":
                # 殺害
                r = requests.post(f"https://{instance}/api/admin/delete-account", headers={"Content-Type": "application/json"}, json=data)
                print(f"{user}の削除に成功しました")
            elif mode == "suspend":
                # 凍結
                r = requests.post(f"https://{instance}/api/admin/suspend-user", headers={"Content-Type": "application/json"}, json=data)
                print(f"{user}の凍結に成功しました")
        else:
            print("ユーザーが存在しないかも")
            continue
