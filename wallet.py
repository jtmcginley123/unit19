import subprocess
import json
from constants import *
import os
from dotenv import load_dotenv
from web3 import Web3
from eth_account import Account
from bit import Key
from bit import PrivateKeyTestnet
from bit import wif_to_key
from bit.network import NetworkAPI
from web3.middleware import geth_poa_middleware

load_dotenv()

mnemonic = os.getenv('MNEMONIC')
privkey = os.getenv('PRIVATE_KEY')
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
print(mnemonic)

w3.middleware_onion.inject(geth_poa_middleware, layer=0)

def derive_wallets(mnemonic, numderive, coin):
    command = './derive -g --mnemonic="'+str(mnemonic)+'" --numderive='+str(numderive)+' --coin='+str(coin)+' --format=json'
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()
    keys = json.loads(output)
    print(keys)
    return json.loads(output)
    
coins = {'eth': derive_wallets(mnemonic=mnemonic, numderive=3, coin=ETH), 'btc-test' : derive_wallets(mnemonic=mnemonic, numderive=3, coin=BTCTEST)}

def priv_key_to_account (coin, priv_key):
    if coin == ETH:
        return w3.eth.accounts.privateKeyToAccount(priv_key)
    elif coin == BTCTEST:
        return PrivateKeyTestnet(priv_key)

eth_privatekey = coins['eth'][0]['privkey']
btc_privatekey = coins['btc-test'][0]['privkey']

def create_tx (coin, account, to, amount):
    if coin == ETH:
        gasEstimate = w3.eth.estimateGas({
            "from": account.address,
            "to": to,
            "value": amount
        })
        return {
            "from": account.address,
            "to": to,
            "value": amount,
            "gas": gasEstimate,
            "gasPrice": w3.eth.gasPrice,
            "nonce": w3.eth.getTransaction,
            "chainID": w3.net.chainID
        }

    elif coin == BTCTEST:
        return PrivateKeyTestnet.prepare_transaction(account.address, [(to, amount, BTC)])

def send_tx (coin, account, to, amount):
    if coin == ETH:
        raw_tx_eth = create_tx(coin, account, to, amount)
        sign_tx_eth = account.sign_transaction(raw_tx_eth)
        result = w3.eth.sendRawTransaction(sign_tx_eth.rawTransaction)
        return result

    elif coin == BTCTEST:
        raw_tx_btctest = create_tx(coin, account, to, amount)
        sign_tx_btctest = account.sign_transaction(raw_tx_btctest)
        return NetworkAPI.broadcast_tx_testnet(sign_tx_btctest)