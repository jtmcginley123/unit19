import subprocess
import json
from constants import *
import os



command = './derive -g --mnemonic="decide wage cotton law laundry renew practice olympic sound spread target gap" --cols=path,address,privkey,pubkey --format=json'

p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
output, err = p.communicate()
p_status = p.wait()

keys = json.loads(output)
print(keys)
