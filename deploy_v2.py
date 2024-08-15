# Used GUI of ganache

from solcx import compile_standard
import json
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file =  file.read()

# Compile the solidity code

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol":{"content": simple_storage_file}},
        "settings": {
            "outputSelection":{
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },

    solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# Get the Bytecode
bytecode = compiled_sol ["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]

# Get the ABI
abi = compiled_sol ["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# For connect to Ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
chain_id = 1337
my_address = "0x649b974da1eedEdc27ADfF23f0d43FE9D5C69477"
private_key = os.getenv("PRIVATE_KEY")

# Create a contract
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get the latest transaction
nonce = w3.eth.get_transaction_count(my_address)

# 1 Build a Transaction
# 2 Sign a Transaction
# 3 Send a Transaction

transaction = SimpleStorage.constructor().build_transaction(
    {"chainId":1337, "from":my_address, "nonce": nonce}
)

signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

print("Deploying Contract.....")
# Send signed Transaction
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
# Wait for reciept
tx_reciept = w3.eth.wait_for_transaction_receipt(tx_hash)

print("Deployeddd")
# When work with Contract
# 1 Contract Address
# 2 Contract ABI

simple_storage = w3.eth.contract(address=tx_reciept.contractAddress, abi=abi)

# Call -> Simulate making the call and getting a return value
# Tran -> Make a state change

print(simple_storage.functions.retrieve().call())

print("Updating Contract......")
store_transaction = simple_storage.functions.store(15).build_transaction({
    "chainId":chain_id, "from":my_address, "nonce":nonce + 1
})
signed_store_txn = w3.eth.account.sign_transaction(store_transaction, private_key=private_key)

send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_reciept = w3.eth.wait_for_transaction_receipt(send_store_tx)
print("Updatedddd")
print(simple_storage.functions.retrieve().call())