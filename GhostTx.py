import requests
import time
from colorama import Fore, Style

API_URL = "https://mempool.space/api/v1/address/{}/txs/mempool"

def fetch_mempool_tx(address):
    try:
        response = requests.get(API_URL.format(address))
        if response.status_code == 200:
            return response.json()
        else:
            print(Fore.RED + f"Failed to fetch mempool data: {response.status_code}" + Style.RESET_ALL)
            return []
    except Exception as e:
        print(Fore.RED + f"Error: {e}" + Style.RESET_ALL)
        return []

def watch_address(address, poll_interval=15):
    print(Fore.CYAN + f"Watching mempool for address {address} every {poll_interval}s..." + Style.RESET_ALL)
    seen_txids = set()

    while True:
        txs = fetch_mempool_tx(address)
        for tx in txs:
            txid = tx.get("txid")
            if txid not in seen_txids:
                seen_txids.add(txid)
                value = sum([v["value"] for v in tx["vout"] if address in v.get("scriptpubkey_address", "")]) / 1e8
                print(Fore.GREEN + f"[NEW TX] {txid} --> +{value} BTC" + Style.RESET_ALL)
        time.sleep(poll_interval)
