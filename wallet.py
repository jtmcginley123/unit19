import subprocess
import json
from dotenv import load_dotenv
import os
from web3 import Web3
from constants import *
from eth_account import Account
from bit import *
from bit.network import NetworkAPI

load_dotenv()

mnemonic = os.getenv('MNEMONIC')
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

private_key = os.getenv("PRIVATE_KEY")

def derive_wallets(mnemonic, numderive, coin):
    command = './derive -g --mnemonic="{mnemonic}" --numderive="{numderive}" --coin="{coin}" --cols=path,address,privkey,pubkey --format=json'
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()

keys = json.loads(output)
print(keys)

coins = {'eth':derive_wallets(mnemonic=mnemonic, coin=ETH, numderive=3), 'btc-test':derive_wallets(mnemonic=mnemonic,coin=BTCTEST,numderive=3)}

eth_privatekey = coins['eth'][0]['privkey']
btc_privatekey = coins['btc-test']['privkey']

def priv_key_to_account (coin, priv_key):
    if coin == ETH:
        return Account.privateKeyToAccount(priv_key)
    if coin == BTCTEST:
        return PrivateKeyTestnet(priv_key)


def create_tx (coin, account, to, amount):
    if coin == 'ETH':
        gasEstimate = w3.eth.estimateGas({
            "to": to,
            "from": account.address,
            "value": amount
        })
        return {
            "to": to,
            "from": account.address,
            "value": amount,
            "gas": gasEstimate,
            "gasPrice": w3.eth.gasPrice,
            "nonce": w3.eth.getTransaction,
            "chainID": w3.net.chainID
        }

    if coin == 'BTCTEST':
        return PrivateKeyTestnet.prepare_transaction(account.address, [(to, amount, BTC)])

    if coin != 'ETH' or  'BTCTEST':
        result = "Please choose ETH or BTCTEST"
        return result

def send_tx (coin, account, to, amount):
    if coin == 'ETH':
        raw_tx_eth = create_tx(coin, account, to, amount)
        sign_tx_eth = account.sign_transaction(raw_tx_eth)
        result = w3.eth.sendRawTransaction(sign_tx_eth.rawTransaction)
        return result

    if coin == 'BTCTEST':
        raw_tx_btctest = create_tx(coin, account, to, amount)
        sign_tx_btctest = account.sign_transaction(raw_tx_btctest)
        return NetworkAPI.broadcast_tx_testnet(sign_tx_btctest)
        
