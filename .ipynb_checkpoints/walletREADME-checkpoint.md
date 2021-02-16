# Multi-Blockchain Wallet

![](Images/newtons-coin-cradle.jpg)




## Dependencies
PHP must be installed on your operating system (any version, 5 or 7). Don't worry, you will not need to know any PHP.

* You will need to clone the hd-wallet-derive tool.

* bit Python Bitcoin library.

* web3.py Python Ethereum library.

## hd-wallet-derive Installation

Execute the following steps:

* Navigate to the Github website for the hd-wallet-derive library and scroll down to the installation instructions.

* Next, open a terminal and execute the following commands. If you are using Windows, you will need to open the git-bash GUI via C:\Program Files\Git\bin\bash.exe directly to enable something called tty mode that makes the terminal more compatible with Unix systems. Once installed, you may move back to using the usual git-bash terminal.
```
git clone https://github.com/dan-da/hd-wallet-derive
cd hd-wallet-derive
php -r "readfile('https://getcomposer.org/installer');" | php
php -d pcre.jit=0 composer.phar install
```

## hd-wallet-derive Execution

* Using a command line navigate to your hd-wallet-derive folder.
* Run command to generate private keys

```
./derive -g --mnemonic="mnemonic-phrase-here" --cols=path,address,privkey,pubkey --format=json
```

![](images/homework13.PNG) 

Wallet.py files runs all the functions which interact with hd-wallet-derive using the command line. The function below calls out the dictionary of coins with addresses and privkeys.

```def derive_wallets(mnemonic, coin, numderive):
    command = f'php derive -g --mnemonic="{mnemonic}"  --numderive={numderive} --coin={coin} --cols=path,address,privkey,pubkey --format=json'

    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()

    keys = json.loads(output)
    return(keys)
  ```

![](images/homework7.PNG) 

To transfer money from one account to another you will need to run send_tx functions.

```
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
```

Could not get eth transaction done. Had an error.

![](images/homework15.PNG) 