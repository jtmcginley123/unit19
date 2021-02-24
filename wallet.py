import subprocess
import json
from constants import *
import os

mnemonic = os.getenv('MNEMONIC', 'insert mnemonic here')

def derive_wallets (mnemonic, coin, numderive):

command = './derive -g --mnemonic="INSERT HERE" --cols=path,address,privkey,pubkey --format=json'

p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
output, err = p.communicate()
p_status = p.wait()

keys = json.loads(output)
print(keys)
