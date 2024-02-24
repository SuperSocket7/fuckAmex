import re
import sys
import requests

instance = "ussr.rumiserver.com"
token = "とーくん"
usernames = []
if len(sys.argv) == 2:
    mode = sys.argv[1]
    instance_block_flag = False
elif len(sys.argv) == 3:
    mode = sys.argv[1]
    instance_block_flag = sys.argv[2]
else:
    print("deleteかsuspendで選べ")
    exit(1)

if mode == "delete":
    print("[ INFO ] 削除するユーザーの名前を書き込んでください")
elif mode == "suspend":
    print("[ INFO ] 凍結するユーザーの名前を書き込んでください")
else:
    print("[\x1b[31mFAILED\x1b[0m] deleteかsuspendで選べ")
    exit(1)
while True:
    user = input()
    if user == "":
        continue
    # 分解
    match = re.findall(r'@[a-zA-Z0-9._-]+', user)
    if len(match) == 1:
        username = match[0][1:]
        host = None
    elif len(match) == 2:
        username = match[0][1:]
        host = match[1][1:]
    else:
        print("[\x1b[31mFAILED\x1b[0m] 間違った値が入力されたかも")
        continue
    while True:
        # ID取得
        data = {
            "host": host,
            "i": token,
            "username": username
        }
        r = requests.post(f"https://{instance}/api/users/show", headers={"Content-Type": "application/json"}, json=data)
        if r.status_code == 200:
            id = r.json()['id']
            host = r.json()['host']
            data = {
                "i": token,
                "userId": id
            }
            if mode == "delete":
                # 殺害
                r = requests.post(f"https://{instance}/api/admin/delete-account", headers={"Content-Type": "application/json"}, json=data)
                print(f"[  \x1b[32mOK\x1b[0m  ] {user}の削除に成功しました")
            elif mode == "suspend":
                # 凍結
                r = requests.post(f"https://{instance}/api/admin/suspend-user", headers={"Content-Type": "application/json"}, json=data)
                print(f"[  \x1b[32mOK\x1b[0m  ] {user}の凍結に成功しました")
            break
        elif r.status_code == 429:
            continue
        else:
            print("[\x1b[31mFAILED\x1b[0m] ユーザーが存在しないかも")
            break
    if instance_block_flag == "enable" and host != None:
        # インスタンスブロック
        data = {
            "allowPartial": True,
            "blocked": True,
            "i": token,
            "limit": 100
        }
        r = requests.post(f"https://{instance}/api/federation/instances", headers={'Content-Type': 'application/json'}, json=data)
        blocked_instances = r.json()
        block_list = []
        for blocked_instance in blocked_instances:
            block_list.append(blocked_instance['host'])
        block_list.append(host)
        data = {
            "blockedHosts": block_list,
            "i": token
        }
        requests.post(f"https://{instance}/api/admin/update-meta", headers={'Content-Type': 'application/json'}, json=data)
        print(f"[  \x1b[32mOK\x1b[0m  ] {host}のインスタンスブロックに成功しました")
