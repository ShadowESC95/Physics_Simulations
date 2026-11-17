from web3 import Web3
import json

w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/YOUR_KEY'))
contract_address = "0x..."
abi = json.load(open("contracts/XiChiABI.json"))

def log_simulation(params, hash):
    contract = w3.eth.contract(address=contract_address, abi=abi)
    tx = contract.functions.logSimulation(
        params["kappa"], 
        params["steps"], 
        hash
    ).build_transaction({
        "gas": 100000,
        "nonce": w3.eth.get_transaction_count(w3.eth.defaultAccount)
    })
    signed = w3.eth.account.sign_transaction(tx, private_key)
    return w3.eth.send_raw_transaction(signed.rawTransaction)
