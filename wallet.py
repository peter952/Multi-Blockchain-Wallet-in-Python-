
# In[1]:


# import libraries
import subprocess
import json
import os
from constants import *
from dotenv import load_dotenv
from web3 import Web3
from eth_account import Account
from bit import PrivateKeyTestnet
from bit.network import NetworkAPI
from web3.middleware import geth_poa_middleware
from web3.gas_strategies.time_based import medium_gas_price_strategy

load_dotenv()


# In[2]:


# import mnemonic from env
#filepath="env.bat"
#p = subprocess.Popen(filepath, shell=True, stdout = subprocess.PIPE)

#stdout, stderr = p.communicate()
#print (p.returncode) # is 0 if success
mnemonic = os.getenv('MNEMONIC')
print(mnemonic)


# In[3]:


# connect to local ETH/ geth
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
w3.eth.setGasPriceStrategy(medium_gas_price_strategy)


# In[4]:


# Define function to derive wallet
def derive_wallets(mnemonic, coin, numderive):
    command = f'php derive -g --mnemonic="{mnemonic}"  --numderive={numderive} --coin={coin} --cols=path,address,privkey,pubkey --format=json'

    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()

    keys = json.loads(output)
    return(keys)




# In[5]:


# Test the function derive_wallets
#print(derive_wallets(mnemonic, BTC, 3))


# In[6]:


#Setting dictionary of coins to be used in the wallet
coins = {"eth":derive_wallets(mnemonic, ETH, 3), "btc-test":derive_wallets(mnemonic, BTCTEST, 3)}
numderive = 3
print(coins["eth"][2]['privkey'])

# In[7]:


# 
keys = {}
for coin in coins:
    keys[coin]= derive_wallets(mnemonic, coin, numderive=3)


# In[8]:



eth_PrivateKey = keys["eth"][0]['privkey']
btc_PrivateKey = keys['btc-test'][0]['privkey']

print(json.dumps(eth_PrivateKey, indent=4, sort_keys=True))
print(json.dumps(btc_PrivateKey, indent=4, sort_keys=True))


# In[9]:


print(json.dumps(keys, indent=4, sort_keys=True))


# In[9]:


# create a function that convert the privkey string in a child key to an account object.
def priv_key_to_account(coin,priv_key):
    print(coin)
    print(priv_key)
    if coin == ETH:
        return Account.privateKeyToAccount(priv_key)
    elif coin == BTCTEST:
        return PrivateKeyTestnet(priv_key)


# In[10]:


def create_tx(coin,account, recipient, amount):
    if coin == ETH: 
        gasEstimate = w3.eth.estimateGas(
            {"from":eth_acc.address, "to":recipient, "value": amount}
        )
        return { 
            "from": eth_acc.address,
            "to": recipient,
            "value": amount,
            "gasPrice": w3.eth.gasPrice,
            "gas": gasEstimate,
            "nonce": w3.eth.getTransactionCount(eth_acc.address)
        }
    
    elif coin == BTCTEST:
        return PrivateKeyTestnet.prepare_transaction(account.address, [(recipient, amount, BTC)])


# In[11]:


# create a function to hold Ethereum 
eth_acc = priv_key_to_account(ETH, derive_wallets(mnemonic, ETH,5)[0]['privkey'])


# In[33]:


# create a function to send txn
def send_txn(coin,account,recipient, amount):
    txn = create_tx(coin, account, recipient, amount)
    if coin == ETH:
        signed_txn = eth_acc.sign_transaction(txn)
        result = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        print(result.hex())
        return result.hex()
    elif coin == BTCTEST:
        tx_btctest = create_tx(coin, account, recipient, amount)
        signed_txn = account.sign_transaction(txn)
        print(signed_txn)
        return NetworkAPI.broadcast_tx_testnet(signed_txn)


# ## BTC-TEST Transactions

# In[15]:


btc_acc = priv_key_to_account(BTCTEST,btc_PrivateKey)


# In[23]:


# create BTC transaction
create_tx(BTCTEST,btc_acc,"mznpUjPZkcYzNRMxFueSqV3ccMgkqFXQnG", 0.003)


# In[34]:


# Send BTC transaction
send_txn(BTCTEST,btc_acc,"mrJTjbtzBXidNXRZQfWMdMJuxAy22fPF6H", 0.003)


# ## ETH Transactions

# In[37]:


#connecting to HTTP with address pk
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545/0x30c2577db89760baa9ba4058b1033b9e103f287e5de1689e35833ee8e7a7c857"))


# In[38]:


# double check if  I am connected to blockchain. 
w3.isConnected()


# ## Check the Balance of the account with local mining blockchain

# In[39]:


#w3.eth.getBalance("0xd4348f16a6b5e0ADd7969D434C6DB44906d50d84")


# In[41]:


create_tx(ETH,eth_acc,"0xd4348f16a6b5e0ADd7969D434C6DB44906d50d84", 1000)


# In[42]:


send_txn(ETH, eth_acc,"0x9c2B3Ec7e8e4CC5B74738987d72a42f8208A38b4", 1000)


# ## Confirmation of 

# In[43]:


w3.eth.getBalance("0x9c2B3Ec7e8e4CC5B74738987d72a42f8208A38b4")
